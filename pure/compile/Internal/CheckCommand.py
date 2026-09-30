import sys
from typing import List

from ..Compile import Compile
from ...component.Registry import Registry
from .ArtifactCompiler import ArtifactCompiler
from .ContractChecker import ContractChecker
from .Finding import Finding
from .UnitLoader import UnitLoader
from .UnitFinder import UnitFinder
from .CallSites import CallSites
from .FunctionFinder import FunctionFinder
from .RootSlots import RootSlots


class CheckCommand:
    # purephp lists props/render; class_name and class_ are the spellings
    # purepy's Call exposes for class(), which is a Python keyword.
    CALL_METHODS = ["props", "render", "class_name", "class_", "style"]

    USAGE = """Pure contract checker.

Usage:
  pure check <path>... [--strict]

Checks every *.cmp.py unit: the slots its template reads against the
keys its prepare() hook returns — with the declarations on a parameter
and on the hook verified against the signature and the template — or,
for a unit without prepare(), against the props its call sites bind.
The hook's parameter types are checked against the slot kinds.
Also checks the fluent calls in every file: a `.prop(...)` the target
does not accept is an error. Reports a slot that one template uses as
both a scalar and a scope, and checks *.shape.py templates for the
same conflict. Directories are searched recursively.

  --strict     exit 1 on warnings too
  -h, --help   show this help
  --           treat every later argument as a path

This is not `pure compile --check`, which reports stale artifacts.

Exit codes:
  0  no error (and no warning under --strict)
  1  the run found errors, or a file could not be read
  2  the command line was wrong
"""

    def __init__(self, units=None):
        self.loader = UnitLoader(units)
        self.checker = ContractChecker()

    def run(self, argv: List[str], stdout=None, stderr=None) -> int:
        stdout = stdout or sys.stdout
        stderr = stderr or sys.stderr
        arguments = argv[1:]
        paths = []
        strict = False
        literal = False

        for argument in arguments:
            if literal:
                paths.append(argument)
                continue

            if argument == "--":
                literal = True
                continue

            if argument == "--strict":
                strict = True
                continue

            if argument in ("-h", "--help"):
                stdout.write(self.USAGE)
                return 0

            if argument.startswith("-"):
                stderr.write(f"pure: unknown option '{argument}'.\n\n{self.USAGE}")
                return 2

            paths.append(argument)

        if not paths:
            stderr.write(
                "pure: check needs at least one file or directory." f"\n\n{self.USAGE}"
            )
            return 2

        files = []
        failed = 0

        for path in paths:
            try:
                for file in UnitFinder.discover(path):
                    files.append(file)
            except Exception as error:
                failed += 1
                stderr.write(f"pure: {error}\n")

        checked = 0
        # purephp passes these by reference; Python ints are immutable, so the
        # counters are lists that the report helpers can mutate.
        errors = [0]
        warnings = [0]
        notes = [0]

        loaded = {}
        trees = {}

        for file in files:
            try:
                loaded[file] = self.loader.units_of(file)
                for name, unit in (loaded[file] or {}).items():
                    shape = Compile.toShape(unit["factory"]())
                    if shape is None:
                        raise Exception(
                            f"component '{name}': the factory must return a tag tree or Shape"  # noqa: E501
                        )
                    trees[name] = shape.tree()
            except Exception as error:
                failed += 1
                if file in loaded:
                    del loaded[file]
                stderr.write(f"pure: {error}\n")

        for file in files:
            try:
                units = loaded.get(file)

                if units is None:
                    checked += 1
                    shape = ArtifactCompiler.load(file)
                    findings = self.checker.check(None, shape.tree(), None, None)
                    self._report(
                        stdout, stderr, file, None, findings, errors, warnings, notes
                    )
                else:
                    if not units:
                        raise Exception(
                            "no component unit is registered here; `pure check` skips the file."  # noqa: E501
                        )

                    attribute_findings = self._attribute_findings(file)

                    for name, unit in units.items():
                        checked += 1
                        prepare = Registry.prepare(name)
                        findings = self.checker.check(
                            name,
                            trees[name],
                            FunctionFinder.of(name, file) if prepare is None else None,
                            prepare,
                        )
                        findings.extend(attribute_findings)
                        self._report(
                            stdout,
                            stderr,
                            file,
                            name,
                            findings,
                            errors,
                            warnings,
                            notes,
                        )

                    self._report_call_sites(
                        stdout, stderr, file, errors, warnings, notes, trees
                    )
            except Exception as error:
                failed += 1
                stderr.write(f"pure: {file}: {error}\n")

        summary = (
            f"checked {checked} unit(s): {errors[0]} error(s), "
            f"{warnings[0]} warning(s)"
        )

        if notes[0] > 0:
            summary += f", {notes[0]} note(s)"

        stdout.write(summary + ".\n")

        if failed > 0 or errors[0] > 0 or (strict and warnings[0] > 0):
            return 1

        return 0

    def _diagnostic(
        self, stdout, stderr, file, level, message, errors, warnings, notes, line=None
    ):
        """Write one diagnostic as a `file:line: level: message` line.

        An error and a warning go to stderr, so `2>/dev/null` leaves only the
        results; an info note is a result and stays on stdout. The line is there
        when the finding has one, so an editor or CI can jump to it.
        """
        stream = stderr if level in ("error", "warning") else stdout
        where = file if line is None else "{}:{}".format(file, line)
        stream.write(f"{where}: {level}: {message}\n")

        if level == "error":
            errors[0] += 1
        elif level == "warning":
            warnings[0] += 1
        else:
            notes[0] += 1

    def _report(self, stdout, stderr, file, name, findings, errors, warnings, notes):
        label = f"{file} (shape)" if name is None else f"component '{name}' -> {file}"

        if not findings:
            stdout.write(f"ok: {label}\n")
            return

        # The file is already the diagnostic's subject, so the message names the
        # unit instead of repeating where it was found.
        subject = "" if name is None else f"component '{name}': "

        for finding in findings:
            self._diagnostic(
                stdout,
                stderr,
                file,
                finding.level,
                subject + finding.message,
                errors,
                warnings,
                notes,
            )

    def _report_call_sites(self, stdout, stderr, file, errors, warnings, notes, trees):
        for site in CallSites.of(file, Registry.names()):
            if site["dynamic"]:
                continue

            expected = self._expected_props(site["name"])
            if expected is None:
                continue

            deprecated = self._deprecated_props(site["name"])

            for prop, line in site["props"].items():
                if prop in expected or prop in self.CALL_METHODS:
                    if prop in deprecated:
                        self._diagnostic(
                            stdout,
                            stderr,
                            file,
                            "warning",
                            f"component '{site['name']}': the call binds '{prop}', which is deprecated: {deprecated[prop]}",  # noqa: E501
                            errors,
                            warnings,
                            notes,
                            line,
                        )
                    continue

                if prop == "children":
                    self._diagnostic(
                        stdout,
                        stderr,
                        file,
                        "error",
                        f"component '{site['name']}': pass children to the call itself, e.g. {site['name']}(children)",  # noqa: E501
                        errors,
                        warnings,
                        notes,
                        line,
                    )
                    continue

                from ...core.Suggestion import Suggestion

                nearest = Suggestion.nearest(prop, expected)
                hint = f" (did you mean '{nearest}'?)" if nearest else ""
                self._diagnostic(
                    stdout,
                    stderr,
                    file,
                    "error",
                    f"component '{site['name']}': the call binds '{prop}', which the target does not accept{hint}",  # noqa: E501
                    errors,
                    warnings,
                    notes,
                    line,
                )

            tree = trees.get(site["name"])
            if tree is None:
                continue

            slots = self._prop_slots(site["name"])
            for prop, items in site["items"].items():
                self._report_items(
                    stdout,
                    stderr,
                    file,
                    site["name"],
                    prop,
                    items,
                    tree,
                    slots.get(prop, prop),
                    errors,
                    warnings,
                    notes,
                )

    def _report_items(
        self,
        stdout,
        stderr,
        file,
        name,
        prop,
        items,
        tree,
        slot,
        errors,
        warnings,
        notes,
    ):
        contract = RootSlots.itemSlots(tree, slot)
        if not contract:
            return

        read = list(contract.keys())

        for index, keys in enumerate(items):
            for key in keys:
                if key in contract:
                    continue
                from ...core.Suggestion import Suggestion

                nearest = Suggestion.nearest(key, read)
                hint = f" (did you mean '{nearest}'?)" if nearest else ""
                self._diagnostic(
                    stdout,
                    stderr,
                    file,
                    "error",
                    f"component '{name}': item {index + 1} of '{prop}' binds '{key}', which the item shape of slot '{slot}' does not read{hint}",  # noqa: E501
                    errors,
                    warnings,
                    notes,
                )

            for key, info in contract.items():
                if not info.get("required", True) or key in keys:
                    continue
                self._diagnostic(
                    stdout,
                    stderr,
                    file,
                    "error",
                    f"component '{name}': item {index + 1} of '{prop}' does not provide '{key}', which the item shape of slot '{slot}' requires",  # noqa: E501
                    errors,
                    warnings,
                    notes,
                )

    def _expected_props(self, name):
        prepare = Registry.prepare(name)

        if prepare is not None:
            return [p.name for p in self.__parameters(prepare)]

        return Registry.slots(name)

    def __parameters(self, prepare):
        import inspect

        try:
            return list(inspect.signature(prepare).parameters.values())
        except (TypeError, ValueError):
            return []

    def __declaration(self, parameter):
        """The Prop a parameter declares, or None.

        purephp reads the #[Prop] attribute; in Python a declaration is the
        parameter's annotation or its default, so both are accepted.
        """
        from ...component.Prop import Prop

        for candidate in (parameter.annotation, parameter.default):
            if isinstance(candidate, Prop):
                return candidate

        return None

    def _deprecated_props(self, name):
        prepare = Registry.prepare(name)

        if prepare is None:
            return {}

        deprecated = {}

        for parameter in self.__parameters(prepare):
            declaration = self.__declaration(parameter)

            if declaration is not None and declaration.deprecated:
                deprecated[parameter.name] = declaration.deprecated

        return deprecated

    def _prop_slots(self, name):
        prepare = Registry.prepare(name)

        if prepare is None:
            return {}

        slots = {}

        for parameter in self.__parameters(prepare):
            declaration = self.__declaration(parameter)
            slots[parameter.name] = (
                declaration.slot if declaration else None
            ) or parameter.name

        return slots

    def _attribute_findings(self, file):
        templates = FunctionFinder.attributed(file, "Template")
        findings = []
        for template in templates:
            import inspect

            try:
                sig = inspect.signature(template)
                if sig.return_annotation is not inspect.Signature.empty:
                    ret = sig.return_annotation
                    if not (
                        hasattr(ret, "__name__") and ret.__name__ in ("Shape", "Tag")
                    ):
                        findings.append(
                            Finding.error(
                                f"#[Template] function {template.__name__}() must declare a return type of Shape or a tag, got {ret}"  # noqa: E501
                            )
                        )
            except (ValueError, TypeError):
                pass
        return findings
