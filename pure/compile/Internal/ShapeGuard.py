import inspect
from typing import Dict

from ...core.DevMode import DevMode


class ShapeGuard:
    _THRESHOLD = 20
    _calls: Dict[str, int] = {}

    _RESERVED = {
        "this",
        "globals",
        "data",
        "kind",
        "_get",
        "_post",
        "_server",
        "_cookie",
        "_files",
        "_env",
        "_session",
        "_request",
    }

    @staticmethod
    def check() -> None:
        if not ShapeGuard._enabled():
            return

        frame = inspect.currentframe()
        if frame is None or frame.f_back is None or frame.f_back.f_back is None:
            return
        caller = frame.f_back.f_back
        file = caller.f_code.co_filename
        line = caller.f_lineno
        key = "{}:{}".format(file, line)

        count = ShapeGuard._calls.get(key, 0) + 1
        ShapeGuard._calls[key] = count

        if count == ShapeGuard._THRESHOLD:
            DevMode.warn(
                key,
                "Compile.shape() was called {} times from {}; "
                "build shapes once per process and memoize them "
                "(_shape = _shape or Compile.shape(...)).".format(count, key),
            )

    @staticmethod
    def _enabled() -> bool:
        # Same guard shape as the other call sites: an explicit
        # `Compile.guard(...)` wins, and only an unset switch consults (and
        # then caches) the environment.
        return DevMode.enabled if DevMode.enabled is not None else DevMode.resolve()
