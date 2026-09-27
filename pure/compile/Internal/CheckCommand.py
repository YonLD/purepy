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

This is not `pure compile --check`, which reports stale artifacts.
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

        for argument in arguments:
            if argument == "--strict":
                strict = True
            elif argument in ("-h", "--help"):
                stdout.write(self.USAGE)
                return 0
            elif argument.startswith("-"):
                stderr.write(f"pure: unknown option '{argument}'\n\n{self.USAGE}")
                return 1
            else:
                paths.append(argument)

        if not paths:
            stderr.write(
                f"pure: check needs at least one file or directory\n\n{self.USAGE}"
            )
            return 1

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
                    self._report(stdout, file, None, findings, errors, warnings)
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
                        self._report(stdout, file, name, findings, errors, warnings)

                    self._report_call_sites(stdout, file, errors, warnings, trees)
            except Exception as error:
                failed += 1
                stderr.write(f"pure: {file}: {error}\n")

        stdout.write(
            f"checked {checked} unit(s): {errors[0]} error(s), {warnings[0]} warning(s).\n"  # noqa: E501
        )

        if failed > 0 or errors[0] > 0 or (strict and warnings[0] > 0):
            return 1

        return 0

    def _report(self, stdout, file, name, findings, errors, warnings):
        label = f"{file} (shape)" if name is None else f"component '{name}' -> {file}"

        if not findings:
            stdout.write(f"ok: {label}\n")
            return

        for finding in findings:
            stdout.write(f"{finding.level}: {label}: {finding.message}\n")
            if finding.level == "error":
                errors[0] += 1
            elif finding.level == "warning":
                warnings[0] += 1

    def _report_call_sites(self, stdout, file, errors, warnings, trees):
        for site in CallSites.of(file, Registry.names()):
            if site["dynamic"]:
                continue

            expected = self._expected_props(site["name"])
            if expected is None:
                continue

            deprecated = self._deprecated_props(site["name"])

            for prop in site["props"]:
                if prop in expected or prop in self.CALL_METHODS:
                    if prop in deprecated:
                        stdout.write(
                            f"warning: {file}: component '{site['name']}': the call binds '{prop}', which is deprecated: {deprecated[prop]}\n"  # noqa: E501
                        )
                        warnings[0] += 1
                    continue

                if prop == "children":
                    stdout.write(
                        f"error: {file}: component '{site['name']}': pass children to the call itself, e.g. {site['name']}(children)\n"  # noqa: E501
                    )
                    errors += 1
                    continue

                from ...core.Suggestion import Suggestion

                nearest = Suggestion.nearest(prop, expected)
                hint = f" (did you mean '{nearest}'?)" if nearest else ""
                stdout.write(
                    f"error: {file}: component '{site['name']}': the call binds '{prop}', which the target does not accept{hint}\n"  # noqa: E501
                )
                errors[0] += 1

            tree = trees.get(site["name"])
            if tree is None:
                continue

            slots = self._prop_slots(site["name"])
            for prop, items in site["items"].items():
                self._report_items(
                    stdout,
                    file,
                    site["name"],
                    prop,
                    items,
                    tree,
                    slots.get(prop, prop),
                    errors,
                )

    def _report_items(self, stdout, file, name, prop, items, tree, slot, errors):
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
                stdout.write(
                    f"error: {file}: component '{name}': item {index + 1} of '{prop}' binds '{key}', which the item shape of slot '{slot}' does not read{hint}\n"  # noqa: E501
                )
                errors[0] += 1

            for key, info in contract.items():
                if not info.get("required", True) or key in keys:
                    continue
                stdout.write(
                    f"error: {file}: component '{name}': item {index + 1} of '{prop}' does not provide '{key}', which the item shape of slot '{slot}' requires\n"  # noqa: E501
                )
                errors[0] += 1

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
