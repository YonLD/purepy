import importlib.util
import os
import sys
from types import ModuleType
from typing import Optional


def load_module(path: str, name: Optional[str] = None) -> ModuleType:
    """Load a `*.cmp.py` or `*.shape.py` file by path and return the module.

    PHP `require`s a unit file and gets its functions back; Python has no
    equivalent, because a module whose name contains a dot (`Card.cmp.py`)
    cannot be imported by name. This is the language-level stand-in:

        Card = load_module('components/Card.cmp.py').Card

    The module is registered in `sys.modules` under `name` so a file that is
    loaded twice is only executed once, as `require` would.
    """
    resolved = os.path.realpath(path)

    if not os.path.isfile(resolved):
        raise ValueError("'{}' does not exist.".format(path))

    key = name or "purepy.unit." + os.path.splitext(os.path.basename(resolved))[0]

    if key in sys.modules:
        return sys.modules[key]

    spec = importlib.util.spec_from_file_location(key, resolved)

    if spec is None or spec.loader is None:
        raise ValueError("'{}' is not a loadable Python module.".format(path))

    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module

    try:
        spec.loader.exec_module(module)
    except Exception:
        del sys.modules[key]
        raise

    return module
