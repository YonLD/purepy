from typing import Any, Callable, Dict, List, Optional

from ..compile.Compile import Compile
from ..compile.Renderer import Renderer
from ..compile.Shape import Shape


class Registry:
    _units: Dict[str, Dict[str, Any]] = {}
    _files: Dict[str, str] = {}
    _keys: Dict[str, str] = {}
    _binders: Dict[str, Callable] = {}
    _renderers: Dict[str, Any] = {}
    _shapes: Dict[str, Shape] = {}

    @staticmethod
    def register(
        name: str,
        file: str,
        factory: Callable,
        override: bool = False,
        prepare: Optional[Callable] = None,
    ):
        if not name:
            raise Exception("component name must not be empty.")

        import os

        if not os.path.isfile(file):
            raise Exception("component unit file '{}' does not exist.".format(file))

        registered = Registry._units.get(name)
        if registered and registered["file"] == file:
            return

        if registered and not override:
            raise Exception(
                "component '{}' is already registered by '{}'; pass override=True to replace it.".format(  # noqa: E501
                    name, registered["file"]
                )
            )

        owner = Registry._files.get(file)
        if owner and owner != name and not override:
            raise Exception(
                "'{}' is already registered as '{}'; a unit file registers one component.".format(  # noqa: E501
                    file, owner
                )
            )

        if registered:
            del Registry._files[registered["file"]]
            Registry._forget(name)

        if owner and owner != name:
            del Registry._units[owner]
            Registry._forget(owner)

        Registry._units[name] = {"file": file, "factory": factory, "prepare": prepare}
        Registry._files[file] = name
        Registry._keys = {}

    @staticmethod
    def prepare(name: str):
        unit = Registry._units.get(name)
        return unit.get("prepare") if unit else None

    @staticmethod
    def slots(name_or_path: str):
        key = Registry._key(name_or_path)

        if key not in Registry._renderers:
            Registry._binder(name_or_path)

        renderer = Registry._renderers.get(key)
        if renderer is not None:
            return renderer.slots
        return None

    @staticmethod
    def component(name_or_path: str) -> Callable[[Dict[str, Any]], str]:
        return Registry._binder(name_or_path)

    @staticmethod
    def names() -> List[str]:
        return list(Registry._units.keys())

    @staticmethod
    def unitsFor(file: str) -> Dict[str, Dict[str, Any]]:
        units = {}
        for name, unit in Registry._units.items():
            if unit["file"] == file:
                units[name] = {"factory": unit["factory"]}
        return units

    @staticmethod
    def reset():
        Registry._units = {}
        Registry._files = {}
        Registry._keys = {}
        Registry._binders = {}
        Registry._renderers = {}
        Registry._shapes = {}

    @staticmethod
    def _binder(name_or_path: str) -> Callable:
        key = Registry._key(name_or_path)
        if key in Registry._binders:
            return Registry._binders[key]

        if key in Registry._units:
            renderer = Registry._unit_renderer(key)
        else:
            renderer = Registry._template_renderer(name_or_path)

        Registry._renderers[key] = renderer

        def binder(data: Dict[str, Any]) -> str:
            return renderer.render(data)

        Registry._binders[key] = binder
        return binder

    @staticmethod
    def _unit_renderer(name: str) -> Renderer:

        unit = Registry._units[name]

        # The precompiled artifact when it is fresh; the compiled shape otherwise.
        return Registry._fresh_artifact(unit["file"]) or Registry._shape(name).compile()

    @staticmethod
    def _fresh_artifact(file: str) -> Optional[Renderer]:
        """Load the unit's artifact when it exists and is not older than the source.

        An artifact that does not yield a Renderer is an error, not a stale
        artifact: the file was compiled by another version of the code.
        """
        import os

        from ..compile.Internal.ArtifactCompiler import ArtifactCompiler

        if not os.path.isfile(file) or not file.endswith((".cmp.py", ".shape.py")):
            return None

        artifact = ArtifactCompiler.artifactPath(file)

        if not os.path.isfile(artifact):
            return None

        if os.path.getmtime(artifact) < os.path.getmtime(file):
            return None

        try:
            renderer = ArtifactCompiler.loadRenderer(artifact)
        except Exception:
            return None

        if not isinstance(renderer, Renderer):
            raise Exception(
                "component artifact '{}' must return a Renderer; run `pure compile`.".format(  # noqa: E501
                    artifact
                )
            )

        return renderer

    @staticmethod
    def _template_renderer(shape_file: str) -> Renderer:
        import os
        import importlib.util

        if shape_file.endswith(".cmp.py"):
            raise Exception(
                "'{}' is a component unit and has no fresh artifact.".format(shape_file)
            )

        if not os.path.isfile(shape_file):
            raise Exception(
                "component template '{}' does not exist.".format(shape_file)
            )

        spec = importlib.util.spec_from_file_location("shape", shape_file)

        if spec is None or spec.loader is None:
            raise Exception("'{}' is not an importable file.".format(shape_file))

        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result = mod.shape() if hasattr(mod, "shape") else None
        shape = Compile.toShape(result)
        if shape is None:
            raise Exception(
                "template '{}' must return a tag tree or Shape.".format(shape_file)
            )
        return shape.compile()

    @staticmethod
    def _shape(name: str) -> Shape:
        if name in Registry._shapes:
            return Registry._shapes[name]
        unit = Registry._units[name]
        result = unit["factory"]()
        shape = Compile.toShape(result)
        if shape is None:
            raise Exception(
                "component '{}' factory must return a tag tree or Shape.".format(name)
            )
        Registry._shapes[name] = shape
        return shape

    @staticmethod
    def _key(name_or_path: str) -> str:
        if name_or_path in Registry._units:
            return name_or_path
        if name_or_path in Registry._keys:
            return Registry._keys[name_or_path]
        if "/" in name_or_path or "\\" in name_or_path or name_or_path.endswith(".py"):
            import os

            path = os.path.realpath(name_or_path) or name_or_path
            key = Registry._files.get(path, "path:" + path)
            Registry._keys[name_or_path] = key
            return key
        raise Exception(
            "unknown component '{}'; known components: {}".format(
                name_or_path, ", ".join(Registry._units.keys()) or "none"
            )
        )

    @staticmethod
    def _forget(name: str):
        Registry._binders.pop(name, None)
        Registry._renderers.pop(name, None)
        Registry._shapes.pop(name, None)
