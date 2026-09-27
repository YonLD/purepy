import keyword
from typing import Dict

from ...core.Slot import Slot
from ...core.SlotKind import SlotKind
from ...core.Tag import Tag


class ScopeTypes:
    """The Python type of every root slot of a tree.

    The compiled renderer takes a plain dict, so these types are only useful to
    a reader: a plain view binds the root slots to annotated parameters, so a
    static analyzer can follow them without an exclusion.
    """

    @staticmethod
    def of(tree: Tag) -> Dict[str, str]:
        types: Dict[str, str] = {}
        ScopeTypes.__collect(tree, types)
        return types

    @staticmethod
    def __collect(tag: Tag, types: Dict[str, str]) -> None:
        for child in tag.get_children():
            if isinstance(child, Slot) and child.name not in types:
                types[child.name] = ScopeTypes.__type_of(child)

        for value in tag.get_attrs().values():
            if isinstance(value, Slot) and value.name not in types:
                types[value.name] = ScopeTypes.__type_of(value)

        for child in tag.get_children():
            if isinstance(child, Tag):
                ScopeTypes.__collect(child, types)

    @staticmethod
    def __type_of(slot: Slot) -> str:
        if slot.kind == SlotKind.Each:
            return "Iterable[Dict[str, Any]]"

        if slot.kind == SlotKind.Child:
            return "Dict[str, Any]"

        if slot.default_value is not None:
            return "str"

        return "Optional[str]"

    @staticmethod
    def parameter(name: str) -> str:
        """A valid Python identifier for a slot name.

        A slot may be named after a keyword (`class`, `type`, `for`); a plain
        view binds root slots to parameters, so those take a trailing
        underscore, matching the `class_()` convention of the tag API.
        """
        import keyword

        if (
            keyword.iskeyword(name)
            or not name.isidentifier()
            or keyword.issoftkeyword(name)
        ):
            return name + "_"

        return name

    @staticmethod
    def signature(tree: Tag, name: str = "view") -> str:
        types = ScopeTypes.of(tree)
        params = []

        for key in sorted(types):
            # A slot whose name cannot be a parameter reads a `data` offset
            # instead, so it takes no parameter of its own.
            if not key.isidentifier() or keyword.iskeyword(key):
                continue

            params.append("{}: {} = None".format(ScopeTypes.parameter(key), types[key]))

        if not params:
            return "def {}() -> str:".format(name)

        return "def {}({}) -> str:".format(name, ", ".join(params))

    @staticmethod
    def docblock(tree: Tag) -> str:
        types = ScopeTypes.of(tree)

        if not types:
            return ""

        lines = ["# view data:"]

        for key in sorted(types):
            lines.append("#   {}: {}".format(key, types[key]))

        return "\n".join(lines)
