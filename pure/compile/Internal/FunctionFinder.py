import inspect
import os
import sys
from typing import Any, Dict, List, Optional

from ..Template import Template


class FunctionFinder:
    _by_file: Optional[Dict[str, List]] = None
    _scanned = -1

    @staticmethod
    def of(short_name: str, file: str):
        position = short_name.rfind("\\")
        if position != -1:
            short_name = short_name[position + 1 :]

        path = os.path.realpath(file) or file

        for function in FunctionFinder.__functions_by_file().get(path, []):
            name = function.__name__
            if name.lower() != short_name.lower():
                continue

            if FunctionFinder.__has_attribute(function, Template):
                continue

            return function

        return None

    @staticmethod
    def attributed(file: str, attribute) -> List:
        path = os.path.realpath(file) or file
        found = []

        for function in FunctionFinder.__functions_by_file().get(path, []):
            if FunctionFinder.__has_attribute(function, attribute):
                found.append(function)

        return found

    @staticmethod
    def __functions_by_file() -> Dict[str, List]:
        functions: List[Any] = FunctionFinder.__all_functions()

        if FunctionFinder._by_file is not None and FunctionFinder._scanned == len(
            functions
        ):
            return FunctionFinder._by_file

        FunctionFinder._scanned = len(functions)
        FunctionFinder._by_file = {}

        for func in functions:
            source = inspect.getsourcefile(func)
            if source is None:
                continue
            path = os.path.realpath(source) or source
            FunctionFinder._by_file.setdefault(path, []).append(func)

        return FunctionFinder._by_file

    @staticmethod
    def __all_functions() -> List:
        functions: List[Any] = []
        for module in list(sys.modules.values()):
            if module is None:
                continue
            try:
                functions.extend(
                    f for _, f in inspect.getmembers(module, inspect.isfunction)
                )
            except Exception:
                continue
        return functions

    @staticmethod
    def __has_attribute(function, attribute) -> bool:
        name = attribute if isinstance(attribute, str) else attribute.__name__

        markers = getattr(function, "__pure_attributes__", None)
        if markers and name in markers:
            return True

        if isinstance(attribute, str):
            return False

        for value in getattr(function, "__dict__", {}).values():
            if isinstance(value, attribute):
                return True

        return False
