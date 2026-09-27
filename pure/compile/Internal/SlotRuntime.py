from typing import Any, Iterable

from ...core.Escaper import Escaper


class SlotRuntime:
    @staticmethod
    def text(value: Any, path: str) -> str:
        if isinstance(value, (int, float, str, bool)):
            return Escaper.text(str(value))
        return Escaper.text(SlotRuntime._stringify(value, path))

    @staticmethod
    def raw(value: Any, path: str) -> str:
        if value is None or isinstance(value, (int, float, str, bool)):
            return str(value)

        if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
            out = ""
            for index, item in enumerate(value):
                out += SlotRuntime._stringify(item, path + "[" + str(index) + "]")
            return out

        return SlotRuntime._stringify(value, path)

    @staticmethod
    def attr_open(name: str, value: Any, path: str) -> str:
        if value is None:
            return ""

        if isinstance(value, bool):
            return Escaper.attribute(name, name) if value else ""

        if isinstance(value, (int, float, str)):
            return Escaper.attribute(name, str(value))

        return Escaper.attribute(name, SlotRuntime._stringify(value, path))

    @staticmethod
    def scope(value: Any, path: str) -> dict:
        if not isinstance(value, dict):
            raise TypeError(
                "slot '{}' must be an array, {} given.".format(
                    path, SlotRuntime._type_name(value)
                )
            )
        return value

    @staticmethod
    def items(value: Any, path: str) -> Iterable:
        if not isinstance(value, (list, tuple)):
            raise TypeError(
                "slot '{}' must be iterable, {} given.".format(
                    path, SlotRuntime._type_name(value)
                )
            )
        return value

    @staticmethod
    def _stringify(value: Any, path: str) -> str:
        if value is None:
            return ""

        if isinstance(value, (int, float, str, bool)):
            return str(value)

        if isinstance(value, (list, tuple, dict, set)):
            raise TypeError(
                "slot '{}' must be stringable, {} given.".format(
                    path, SlotRuntime._type_name(value)
                )
            )

        return str(value)

    @staticmethod
    def _type_name(value: Any) -> str:
        return type(value).__name__
