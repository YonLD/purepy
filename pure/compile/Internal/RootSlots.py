from typing import Dict, List

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
