from collections.abc import Iterable, Mapping
from typing import Any

from ...core.Escaper import Escaper


class SlotRuntime:
    @staticmethod
    def text(value: Any, path: str) -> str:
        if isinstance(value, (int, float, str, bool)):
            return Escaper.text(Escaper.to_string(value))
        return Escaper.text(SlotRuntime._stringify(value, path))

    @staticmethod
    def raw(value: Any, path: str) -> str:
        if value is None or isinstance(value, (int, float, str, bool)):
            return Escaper.to_string(value)

        if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
            out = ""
            for index, item in enumerate(value):
                out += SlotRuntime._stringify(
                    item, path + "[" + Escaper.to_string(index) + "]"
                )
            return out

        return SlotRuntime._stringify(value, path)

    @staticmethod
    def attr_open(name: str, value: Any, path: str) -> str:
        if value is None:
            return ""

        if isinstance(value, bool):
            return Escaper.attribute(name, name) if value else ""

        if isinstance(value, (int, float, str)):
            return Escaper.attribute(name, Escaper.to_string(value))

        return Escaper.attribute(name, SlotRuntime._stringify(value, path))

    @staticmethod
    def scope(value: Any, path: str, hint: str = "") -> dict:
        """Ensure a child component value is a mapping usable as a data scope.

        The hint is a compiled constant naming what the scope expects, appended
        to the message of a rejected value; a generated renderer passes it for
        the items of a list slot, whose shape decides whether a value can stand
        in for the scope at all.
        """
        if not isinstance(value, dict):
            raise TypeError(
                "slot '{}' must be an array, {} given.{}".format(
                    path, SlotRuntime._type_name(value), hint
                )
            )
        return value

    @staticmethod
    def items(value: Any, path: str) -> Iterable:
        """Ensure a list slot value is iterable, the way purephp's foreach reads it.

        `is_iterable()` accepts any array or Traversable, not just a list, so a
        mapping and a generator are as acceptable here as a tuple. A mapping
        yields its values rather than its keys, because that is what iterating
        the equivalent PHP array does.
        """
        if isinstance(value, Mapping):
            return value.values()

        if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
            return value

        raise TypeError(
            "slot '{}' must be iterable, {} given.".format(
                path, SlotRuntime._type_name(value)
            )
        )

    @staticmethod
    def _stringify(value: Any, path: str) -> str:
        if value is None:
            return ""

        if isinstance(value, (int, float, str, bool)):
            return Escaper.to_string(value)

        if isinstance(value, (list, tuple, dict, set)):
            raise TypeError(
                "slot '{}' must be stringable, {} given.".format(
                    path, SlotRuntime._type_name(value)
                )
            )

        return Escaper.to_string(value)

    @staticmethod
    def _type_name(value: Any) -> str:
        return Escaper.debug_type(value)
