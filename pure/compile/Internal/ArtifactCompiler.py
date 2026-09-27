import contextlib
import importlib.util
import io
import os
import sys
import tempfile
from typing import Dict, List, Optional, TypedDict

from ...core.Tag import Tag
from ..Compile import Compile
from ..Renderer import Renderer
from ..Shape import Shape
from .PlainGenerator import PlainGenerator
from .RootSlots import RootSlots
from .ScopeTypes import ScopeTypes
from .ShapeIndex import ShapeIndex
from .CodeGenerator import HELPERS
from .TemplateGenerator import TemplateGenerator


class ArtifactCompiler:
    SUFFIX = ".shape.py"

    UNIT_SUFFIXES = [".shape.py", ".cmp.py"]

    @staticmethod
    def build(shape_file: str, plain: bool = False) -> str:
        sources = ArtifactCompiler.buildAll(shape_file, plain)
        built = sources["plain"] if plain else sources["artifact"]

        return built if built is not None else ""

    @staticmethod
    def buildAll(shape_file: str, plain: bool = False) -> "Project":
        return ArtifactCompiler.buildUnit(
            shape_file, ArtifactCompiler.load(shape_file), plain
        )

    @staticmethod
    def buildUnit(unit_file: str, shape: Shape, plain: bool = False) -> "Project":
        return ArtifactCompiler.__project(unit_file, shape, plain)

    @staticmethod
    def write(shape_file: str, plain: bool = False) -> str:
        return ArtifactCompiler.writeAll(shape_file, plain)["artifact"]

    @staticmethod
    def writeChanged(shape_file: str, plain: bool = False) -> Dict:
        return ArtifactCompiler.writeUnit(
            shape_file, ArtifactCompiler.load(shape_file), plain
        )

    @staticmethod
    def writeUnit(unit_file: str, shape: Shape, plain: bool = False) -> Dict:
        project = ArtifactCompiler.__project(unit_file, shape, plain)
        artifact = ArtifactCompiler.artifactPath(unit_file)
        plain_file = ArtifactCompiler.plainPath(unit_file) if plain else None

        artifact_written = ArtifactCompiler.__write_if_changed(
            artifact, project["artifact"], unit_file, project["id"], "artifact"
        )
        plain_written = False

        if plain_file is not None and project["plain"] is not None:
            plain_written = ArtifactCompiler.__write_if_changed(
                plain_file, project["plain"], unit_file, project["id"], "plain view"
            )

        return {
            "artifact": artifact,
            "plain": plain_file,
            "artifactWritten": artifact_written,
            "plainWritten": plain_written,
        }

    @staticmethod
    def writeAll(shape_file: str, plain: bool = False) -> "Project":
        project = ArtifactCompiler.__project(
            shape_file, ArtifactCompiler.load(shape_file), plain
        )
        artifact = ArtifactCompiler.artifactPath(shape_file)
        plain_file = ArtifactCompiler.plainPath(shape_file) if plain else None

        ArtifactCompiler.__write_file(
            artifact, project["artifact"], shape_file, project["id"], "artifact"
        )

        if plain_file is not None and project["plain"] is not None:
            ArtifactCompiler.__write_file(
                plain_file, project["plain"], shape_file, project["id"], "plain view"
            )

        return {"artifact": artifact, "plain": plain_file, "id": project["id"]}

    @staticmethod
    def artifactPath(shape_file: str) -> str:
        return ArtifactCompiler.__sibling(shape_file, ".pure.py")

    @staticmethod
    def plainPath(shape_file: str) -> str:
        return ArtifactCompiler.__sibling(shape_file, ".plain.py")

    @staticmethod
    def __sibling(unit_file: str, suffix: str) -> str:
        for unit_suffix in ArtifactCompiler.UNIT_SUFFIXES:
            if unit_file.endswith(unit_suffix):
                return unit_file[: -len(unit_suffix)] + suffix

        suffixes = " or ".join("*" + s for s in ArtifactCompiler.UNIT_SUFFIXES)
        raise ValueError("'{}' is not a {} file.".format(unit_file, suffixes))

    @staticmethod
    def __project(unit_file: str, shape: Shape, plain: bool) -> "Project":
        tree = shape.tree()
        id = ShapeIndex.of(tree).id()

        return {
            "artifact": ArtifactCompiler.__artifactFile(unit_file, tree, id),
            "plain": (
                ArtifactCompiler.__plainFile(unit_file, tree, id) if plain else None
            ),
            "id": id,
        }

    @staticmethod
    def __artifactFile(shape_file: str, tree: Tag, id: str) -> str:
        source = TemplateGenerator.source(tree)
        py_version = "{}.{}".format(sys.version_info[0], sys.version_info[1])

        artifact = "# Compiled from {}, do not edit.\n".format(
            os.path.basename(shape_file)
        )
        artifact += "# Run `pure compile` to rebuild after changing the shape.\n"
        artifact += "# purepy-shape id={} v={} py={}\n\n".format(
            id, Compile.CACHE_VERSION, py_version
        )
        artifact += "from pure.compile.Compile import Compile\n"
        artifact += "from pure.compile.Renderer import Renderer\n"

        for imp in TemplateGenerator.imports(source):
            artifact += imp + "\n"

        artifact += "\nif {} != Compile.CACHE_VERSION:\n".format(Compile.CACHE_VERSION)
        artifact += "    raise RuntimeError('stale purepy artifact: generated for cache version {}; run `pure compile` to rebuild')\n\n".format(  # noqa: E501
            Compile.CACHE_VERSION
        )
        artifact += HELPERS + "\n\n"

        artifact += source + "\n\n"
        artifact += "renderer = Renderer(\n"
        artifact += "    pure_body,\n"
        artifact += "    {},\n".format(repr(id))
        artifact += "    {}\n".format(ArtifactCompiler.__slotList(RootSlots.of(tree)))
        artifact += ")\n"

        return artifact

    @staticmethod
    def __slotList(slots: List[str]) -> str:
        items = [repr(slot) for slot in slots]
        inline = "[" + ", ".join(items) + "]"

        if len(inline) <= 100:
            return inline

        return "[\n        " + ",\n        ".join(items) + "\n    ]"

    @staticmethod
    def __plainFile(shape_file: str, tree: Tag, id: str) -> str:
        py_version = "{}.{}".format(sys.version_info[0], sys.version_info[1])

        file = "# Compiled from {}, do not edit.\n".format(os.path.basename(shape_file))
        file += "# Plain view: render it with the view data extracted into locals; no library\n"  # noqa: E501
        file += "# is needed at load time. Root slots become the local variables of the view\n"  # noqa: E501
        file += (
            "# and carry type annotations derived from the shape, so static analyzers\n"
        )
        file += "# can follow them without an exclusion.\n"
        file += "# Run `pure compile --plain` to rebuild after changing the shape.\n"
        file += "# purepy-shape id={} v={} py={}\n\n".format(
            id, Compile.CACHE_VERSION, py_version
        )

        annotation = ScopeTypes.docblock(tree)

        if annotation:
            file += annotation + "\n"

        return file + PlainGenerator.view(tree)

    @staticmethod
    def __write_if_changed(
        path: str,
        contents: str,
        shape_file: Optional[str],
        id: Optional[str],
        kind: str,
    ) -> bool:
        if os.path.isfile(path):
            try:
                with open(path, "r") as f:
                    if f.read() == contents:
                        return False
            except OSError:
                pass

        ArtifactCompiler.__write_file(path, contents, shape_file, id, kind)

        return True

    @staticmethod
    def __write_file(
        path: str,
        contents: str,
        shape_file: Optional[str],
        id: Optional[str],
        kind: str,
    ) -> None:
        temporary = None

        try:
            dir_name = os.path.dirname(path)
            fd, temporary = tempfile.mkstemp(
                prefix="pure-artifact-", suffix=".py", dir=dir_name
            )

            with os.fdopen(fd, "w") as f:
                f.write(contents)

            if kind == "artifact":
                ArtifactCompiler.__verify(temporary, shape_file, id)
            else:
                ArtifactCompiler.__verifyPlain(temporary, shape_file, id)

            os.chmod(temporary, 0o644)

            os.rename(temporary, path)
        except Exception:
            if temporary is not None:
                try:
                    os.unlink(temporary)
                except OSError:
                    pass
            raise

    @staticmethod
    def loadRenderer(artifact_file: str):
        """Load a compiled *.pure.py artifact and return its Renderer.

        A shape file exposes `shape()`; an artifact exposes `renderer`, which
        is what the registry serves instead of recompiling the unit.
        """
        if not os.path.isfile(artifact_file):
            return None

        name = "purepy.artifact." + os.path.basename(artifact_file).replace(".", "_")

        spec = importlib.util.spec_from_file_location(name, artifact_file)

        if spec is None or spec.loader is None:
            return None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(module, "renderer", None)

    @staticmethod
    def load(shape_file: str) -> Shape:
        if not os.path.isfile(shape_file):
            raise ValueError("'{}' does not exist.".format(shape_file))

        buffer = io.StringIO()

        try:
            with contextlib.redirect_stdout(buffer):
                spec = importlib.util.spec_from_file_location("pure_shape", shape_file)

                if spec is None or spec.loader is None:
                    raise ValueError(
                        "'{}' is not an importable file.".format(shape_file)
                    )

                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                result = getattr(mod, "shape", None)

                # A module cannot return a value, so the shape is the `shape`
                # attribute. A factory (`shape()` or a `@Template` function) is
                # called; a `Shape` is not, even though it is callable, because
                # calling it would render with no data.
                if callable(result) and not isinstance(result, (Shape, Tag)):
                    result = result()
        except Exception as error:
            raise ValueError(
                "'{}' could not be loaded: {}".format(shape_file, error)
            ) from error

        shape = Compile.toShape(result)

        if shape is None:
            raise ValueError(
                "'{}' must return a tag tree or pure.compile.Shape, got {}.".format(
                    shape_file, type(result).__name__
                )
            )

        return shape

    @staticmethod
    def __verify(temporary: str, shape_file: Optional[str], id: Optional[str]) -> None:
        try:
            spec = importlib.util.spec_from_file_location("pure_artifact", temporary)

            if spec is None or spec.loader is None:
                raise ValueError("'{}' is not an importable file.".format(temporary))

            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            renderer = getattr(mod, "renderer", None)
        except Exception as error:
            raise ValueError(
                "the artifact for '{}' failed to load: {}".format(shape_file, error)
            ) from error

        if not isinstance(renderer, Renderer) or renderer.shape_id != id:
            raise ValueError(
                "the artifact for '{}' did not load as its compiled renderer.".format(
                    shape_file
                )
            )

    @staticmethod
    def __verifyPlain(
        temporary: str, shape_file: Optional[str], id: Optional[str]
    ) -> None:
        with open(temporary, "r") as f:
            source = f.read()

        if ("# purepy-shape id=" + (id or "") + " ") not in source:
            raise ValueError(
                "the plain view for '{}' did not keep its fingerprint.".format(
                    shape_file
                )
            )

        try:
            compile(source, temporary, "exec")
        except SyntaxError as error:
            raise ValueError(
                "the plain view for '{}' is not valid Python: {}".format(
                    shape_file, error
                )
            ) from error


class Project(TypedDict):
    """The generated sources for one unit: the artifact always, the plain view
    only when it was asked for."""

    artifact: str
    plain: Optional[str]
    id: str
