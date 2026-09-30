from typing import Dict

from ...core.Slot import Slot
from ...core.SlotKind import SlotKind
from ...core.Tag import Tag
from .RootSlots import RootSlots


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
                continue

            # Both branches of a condition render into the current scope, so
            # the keys they read are read by this one too. Without this a slot
            # that only appears inside an `if` would have no parameter and the
            # view would raise on it.
            if isinstance(child, Slot) and child.kind == SlotKind.If:
                if child.shape is not None:
                    ScopeTypes.__collect(child.shape.tree(), types)

                if child.else_shape is not None:
                    ScopeTypes.__collect(child.else_shape.tree(), types)

    @staticmethod
    def __type_of(slot: Slot) -> str:
        if slot.kind == SlotKind.Each:
            return "Iterable[{}]".format(ScopeTypes.__item_type(slot))

        if slot.kind == SlotKind.Child:
            return "Dict[str, Any]"

        if slot.kind == SlotKind.If:
            # A condition is read for truthiness, so its value is whatever the
            # caller passes rather than text.
            return "Any"

        if slot.kind == SlotKind.Raw:
            return "Union[Iterable[Any], str, int, float, None]"

        if slot.default_value is not None:
            return "str"

        return "Optional[str]"

    @staticmethod
    def __item_type(slot: Slot) -> str:
        """The type of one item of a list slot.

        An item shape that renders one key also accepts a scalar, which stands
        in for the whole item scope, so a plain view binds it the same way the
        runtime does.
        """
        item = "Dict[str, Any]"

        if RootSlots.itemKey(RootSlots.itemManifest(slot.shape)) is None:
            return item

        return "Union[{}, str]".format(item)

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
        from .PlainGenerator import PlainGenerator

        types = ScopeTypes.of(tree)
        params = []
        needs_data = False

        for key in sorted(types):
            # A slot whose name cannot be an ordinary local reads a `data` offset
            # instead, so it takes no parameter of its own. The plain view makes
            # the same decision, and one function keeps the two from disagreeing
            # on a name like `out`, which the view itself owns.
            if PlainGenerator.local(key) is None:
                needs_data = True
                continue

            params.append("{}: {} = None".format(ScopeTypes.parameter(key), types[key]))

        if needs_data:
            # The offsets share one mapping, the way purephp's extract() hands
            # the whole view data to the template.
            params.append("data: Optional[Dict[str, Any]] = None")

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
