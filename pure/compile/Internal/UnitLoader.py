import contextlib
import importlib.util
import io
import os
import sys
from typing import Any, Callable, Dict, Optional


class UnitLoader:
    def __init__(self, units: Optional[Callable] = None):
        self._units: Optional[Callable[[str], Optional[Dict[str, Any]]]] = units

    def units_of(self, file: str) -> Optional[Dict]:
        if not file.endswith(".cmp.py"):
            return None

        if self._units is None:
            raise RuntimeError(
                "unit files need the component registry; run `pure compile` through the CLI."  # noqa: E501
            )

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            module_name = "pure_unit_" + os.path.basename(file).replace(".", "_")
            spec = importlib.util.spec_from_file_location(module_name, file)

            if spec is None or spec.loader is None:
                raise ValueError("'{}' is not an importable unit file.".format(file))

            mod = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = mod
            spec.loader.exec_module(mod)

        return self._units(file)
