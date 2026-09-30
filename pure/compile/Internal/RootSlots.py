from typing import Dict, List, Optional

from ...core.ShapeContract import ShapeContract
from ...core.Slot import Slot
from ...core.SlotKind import SlotKind
from ...core.Tag import Tag


class RootSlots:
    def __init__(self, slots: List[str]):
        self.slots = slots

    @staticmethod
    def of(tree: Tag) -> List[str]:
        return list(RootSlots.manifest(tree).keys())

    @staticmethod
    def manifest(tree: Tag) -> Dict[str, Dict]:
        slots: Dict[str, Dict] = {}
        RootSlots.__collect(tree, slots)
        return slots

    @staticmethod
    def itemSlots(tree: Tag, slot: str) -> Dict[str, Dict]:
        items: Dict[str, Dict] = {}

        for shape in RootSlots.__itemShapes(tree, slot):
            for name, info in RootSlots.manifest(shape.tree()).items():
                entry = items.get(name)
                if entry is None:
                    entry = {"required": False, "kinds": {}}
                    items[name] = entry

                entry["required"] = entry["required"] or info["required"]

                for kind in info["kinds"]:
                    entry["kinds"][kind] = True

        return items

    @staticmethod
    def itemManifest(shape: Optional[ShapeContract]) -> Dict[str, Dict]:
        """The item scope manifest of a list slot: what each item supplies.

        Every consumer of an item shape goes through this one analysis, so
        asking several questions of the same shape costs a single walk of it.
        A list slot with no shape has an empty manifest.
        """
        return {} if shape is None else RootSlots.manifest(shape.tree())

    @staticmethod
    def itemKey(manifest: Dict[str, Dict]) -> Optional[str]:
        """The single key an item shape renders, when one value stands for a
        whole item scope.

        An item shape that reads exactly one key as a value or raw slot binds
        that key directly, so a scalar item can stand in for it: a list of
        strings renders a list of strings, and the caller does not wrap every
        item in a one-key map. The name is None when the shape reads several
        keys, reads its only key as a nested scope (a child or list slot needs a
        real mapping or iterable), or reads no key at all -- there an item is a
        scope of its own.
        """
        if len(manifest) != 1:
            return None

        name = next(iter(manifest))
        kinds = manifest[name]["kinds"]

        # Reading the key as a nested scope as well means the item has to stay a
        # scope of its own, so a scalar cannot stand in for it even though the
        # shape renders that same key as a value.
        if SlotKind.Child.name in kinds or SlotKind.Each.name in kinds:
            return None

        # A condition is a truthiness read, not a rendered value: binding a
        # scalar to it would pick a branch per item, which the shape never
        # asked for.
        if SlotKind.Value.name in kinds or SlotKind.Raw.name in kinds:
            return name

        return None

    @staticmethod
    def itemHint(manifest: Dict[str, Dict]) -> str:
        """The message suffix naming the keys an item shape reads, for a list
        item that is not a scope.

        The suffix is a compiled constant, so it costs nothing on the path where
        the item is a scope: only the raise in SlotRuntime.scope() reads it.
        """
        slots = list(manifest)

        if not slots:
            return (
                " The item shape of this slot reads no slots, "
                "so each item must be an empty array."
            )

        quoted = ["'{}'".format(name) for name in slots]
        last = quoted.pop()
        listed = ", ".join(quoted) + (" and " if quoted else "") + last

        return (
            " The item shape of this slot reads {}, "
            "so each item must be an array.".format(listed)
        )

    @staticmethod
    def __collect(tag: Tag, slots: Dict[str, Dict]) -> None:
        export = tag.export()

        for value in export["attrs"].values():
            if isinstance(value, Slot):
                RootSlots.__add(slots, value)

        if export["selfClose"]:
            return

        for child in export["children"]:
            if isinstance(child, Tag):
                RootSlots.__collect(child, slots)
                continue

            if not isinstance(child, Slot):
                continue

            RootSlots.__add(slots, child)

            if child.kind in (SlotKind.Child, SlotKind.Each):
                continue

            if child.kind == SlotKind.If:
                if child.shape is not None:
                    RootSlots.__collect(child.shape.tree(), slots)

                if child.else_shape is not None:
                    RootSlots.__collect(child.else_shape.tree(), slots)

    @staticmethod
    def __itemShapes(tree: Tag, slot: str) -> List[ShapeContract]:
        shapes: List[ShapeContract] = []
        export = tree.export()

        if export["selfClose"]:
            return shapes

        for child in export["children"]:
            if isinstance(child, Tag):
                shapes.extend(RootSlots.__itemShapes(child, slot))
                continue

            if (
                isinstance(child, Slot)
                and child.kind == SlotKind.Each
                and child.name == slot
                and child.shape is not None
            ):
                shapes.append(child.shape)

        return shapes

    @staticmethod
    def __add(slots: Dict[str, Dict], slot: Slot) -> None:
        entry = slots.get(slot.name)
        if entry is None:
            entry = {"required": False, "kinds": {}}
            slots[slot.name] = entry

        entry["required"] = entry["required"] or slot.is_required
        entry["kinds"][slot.kind.name] = True
