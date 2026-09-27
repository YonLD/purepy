import sys
from typing import Dict, List, Tuple

from ..Compile import Compile
from .ArtifactCompiler import ArtifactCompiler
from .UnitLoader import UnitLoader
from .UnitFinder import UnitFinder
from .FunctionFinder import FunctionFinder


class ArtifactCommand:
    USAGE = """Pure shape compiler.

Commands:
  pure compile <path>...   write *.pure.py artifacts (and --plain views)
  pure check <path>...     check component contracts (slots, bindings)
  pure -v, --version       print the version

Run `pure check --help` for the contract checks.

Usage:
  pure compile <path>... [--check] [--plain] [--list]

Compiles every *.shape.py file that returns a tag tree or a Shape and
every *.cmp.py unit that registers a component into a sibling
*.pure.py artifact. Directories are searched recursively.

  --check      report stale or missing files without writing (exit 1)
  --plain      also write a *.plain.py view: markup and native Python that
               renders without purepy installed
  --list       print the components and shape files found, without compiling
  -h, --help   show this help

A *.cmp.py unit registers exactly one component with
register(); compiling it requires the file, so run the compiler
through bin/pure, which wires the registry.
"""

    def __init__(self, units=None):
        self.loader = UnitLoader(units)

    def run(self, argv: List[str], stdout=None, stderr=None) -> int:
        stdout = stdout or sys.stdout
        stderr = stderr or sys.stderr

        arguments = list(argv)
        command = arguments[0] if arguments else None
        arguments = arguments[1:]

        if command is None:
            stderr.write(self.USAGE)
            return 1

        if command in ("-h", "--help"):
            stdout.write(self.USAGE)
            return 0

        if command != "compile":
            stderr.write(f"pure: unknown command '{command}'.\n\n{self.USAGE}")
            return 1

        check = False
        plain = False
        list_only = False
        paths = []

        for argument in arguments:
            if argument == "--check":
                check = True
            elif argument == "--plain":
                plain = True
            elif argument == "--list":
                list_only = True
            elif argument in ("-h", "--help"):
                stdout.write(self.USAGE)
                return 0
            elif argument.startswith("-"):
                stderr.write(f"pure: unknown option '{argument}'.\n")
                return 1
            else:
                paths.append(argument)

        if not paths:
            stderr.write(
                f"pure: compile needs at least one file or directory.\n\n{self.USAGE}"
            )
            return 1

        failed = 0
        # purephp passes the stale count by reference; Python ints are
        # immutable, so it is a list the helper can mutate.
        stale = [0]
        files = []

        for path in paths:
            try:
                for file in UnitFinder.discover(path):
                    files.append(file)
            except Exception as error:
                failed += 1
                stderr.write(f"pure: {error}\n")

        files, collisions = self._without_collisions(files, stderr)
        failed += collisions

        for file in files:
            try:
                units = self.loader.units_of(file)

                if list_only:
                    self._print_list(stdout, file, units)
                    continue

                if units is None:
                    self._compile(file, None, check, plain, stdout, stale)
                    continue

                if not units:
                    raise Exception(
                        "no component unit is registered here; call register() in the file."  # noqa: E501
                    )

                if len(units) > 1:
                    raise Exception(
                        f"{len(units)} component units are registered here; a unit file registers one component."  # noqa: E501
                    )

                result = next(iter(units.values()))["factory"]()
                shape = Compile.toShape(result)

                if shape is None:
                    raise Exception(
                        f"the unit factory must return a tag tree or Shape, got {type(result).__name__}."  # noqa: E501
                    )

                self._compile(file, shape, check, plain, stdout, stale)
            except Exception as error:
                failed += 1
                stderr.write(f"pure: {file}: {error}\n")

        if stale[0] > 0:
            stderr.write(f"pure: {stale[0]} artifact(s) need recompiling.\n")

        return 1 if (failed > 0 or stale[0] > 0) else 0

    def _without_collisions(self, files, stderr) -> Tuple[List[str], int]:
        """Drop the files that fight over one artifact, and report how many
        pairs collided so the caller can fail the run."""
        claimed: Dict[str, str] = {}
        dropped = set()
        collisions = 0

        for file in files:
            target = ArtifactCompiler.artifactPath(file)
            owner = claimed.get(target)

            if owner is None:
                claimed[target] = file
                continue

            if owner == file:
                continue

            dropped.add(owner)
            dropped.add(file)
            collisions += 1
            stderr.write(
                f"pure: '{target}' is claimed by both '{owner}' and '{file}'; one file per artifact name.\n"  # noqa: E501
            )

        return [f for f in files if f not in dropped], collisions

    def _compile(self, file, shape, check, plain, stdout, stale):
        if check:
            if shape is None:
                sources = ArtifactCompiler.buildAll(file, plain)
            else:
                sources = ArtifactCompiler.buildUnit(file, shape, plain)

            targets = {ArtifactCompiler.artifactPath(file): sources["artifact"]}
            if sources.get("plain") is not None:
                targets[ArtifactCompiler.plainPath(file)] = sources["plain"]

            for target, expected in targets.items():
                try:
                    with open(target, "r") as f:
                        current = f.read()
                except FileNotFoundError:
                    current = None

                if current is None:
                    stale[0] += 1
                    stdout.write(f"missing: {target}\n")
                elif current == expected:
                    stdout.write(f"up to date: {target}\n")
                else:
                    stale[0] += 1
                    stdout.write(f"stale: {target}\n")

            return

        if shape is None:
            written = ArtifactCompiler.writeChanged(file, plain)
        else:
            written = ArtifactCompiler.writeUnit(file, shape, plain)

        if not written["artifactWritten"] and not written["plainWritten"]:
            stdout.write(f"unchanged: {file}\n")
            return

        targets = written["artifact"]
        if written.get("plain"):
            targets += f", {written['plain']}"
        stdout.write(f"compiled: {file} -> {targets}\n")

    def _print_list(self, stdout, file, units):
        if units is None:
            stdout.write(f"{file} (shape)\n")
        else:
            for name in units:
                stdout.write(f"{name} -> {file} (component)\n")

        for template in FunctionFinder.attributed(file, "Template"):
            stdout.write(f"{template.__name__} -> {file} (template)\n")
