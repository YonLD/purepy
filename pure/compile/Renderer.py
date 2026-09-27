from typing import Any, Callable, Dict, Optional, cast

from ..core.DevMode import DevMode
from ..core.Suggestion import Suggestion


class Renderer:
    def __init__(self, source, shape_id: str, slots):
        # `source` is either the generated source (compiled on first use) or an
        # already-built render callable, as an artifact loads it.
        self.source = source if isinstance(source, str) else None
        self._render_fn: Optional[Callable[[Dict[str, Any]], str]] = (
            None if isinstance(source, str) else source
        )
        self.shape_id = shape_id
        self.slots = slots

    @property
    def id(self) -> str:
        """The structure fingerprint shared by the shape and its cached renderer."""
        return self.shape_id

    def _compile(self) -> Callable[[Dict[str, Any]], str]:
        if self._render_fn is None:
            namespace: Dict[str, Any] = {}

            if self.source is None:
                raise ValueError("renderer has neither source nor a compiled function")

            exec(self.source, namespace)
            self._render_fn = cast(Callable[[Dict[str, Any]], str], namespace["render"])
        return self._render_fn

    def render(self, data: Dict[str, Any]) -> str:
        if self.slots is not None and (
            DevMode.enabled if DevMode.enabled is not None else DevMode.resolve()
        ):
            self._warn_unknown_keys(data)

        return self._compile()(data)

    def _warn_unknown_keys(self, data: Dict[str, Any]) -> None:
        fresh = []

        for key in data:
            key = str(key)
            if key in self.slots:
                continue
            if DevMode.mark("data:{}:{}".format(self.shape_id, key)):
                fresh.append(key)

        if not fresh:
            return

        reported = []
        for key in fresh:
            nearest = Suggestion.nearest(key, self.slots)
            reported.append(
                "'{}'".format(key)
                if nearest is None
                else "'{}' (did you mean '{}'?)".format(key, nearest)
            )

        DevMode.emit(
            "unknown data {} {}; the template reads: {}."
            " Extra data is ignored, so a misspelled key renders as if absent;"
            " disable this warning with Compile.guard(False).".format(
                "key" if len(fresh) == 1 else "keys",
                ", ".join(reported),
                ", ".join(self.slots),
            )
        )

    def save(self, path: str, data: Dict[str, Any], header: str = ""):
        rendered = self.render(data)
        with open(path, "w") as f:
            f.write(header + rendered)
