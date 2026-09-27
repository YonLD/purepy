from ...core.Tag import Tag
from ...core.Slot import Slot
from ...core.SlotKind import SlotKind
from ...core.Raw import Raw
from ...core.Markup import Markup
from ...core.ShapeContract import ShapeContract
from .CompileException import CompileException
from .ShapeVisitor import ShapeVisitor


class ShapeWalker:
    def __init__(self, visitor: ShapeVisitor):
        self._visitor = visitor

    def walk(self, tree: Tag) -> None:
        self._tag(tree, "")

    def _tag(self, tag: Tag, path: str) -> None:
        export = tag.export()

        if not self._visitor.tag_open(tag, path, export):
            return

        for key, value in export["attrs"].items():
            name = value.name if isinstance(value, Slot) else str(key)
            self._visitor.attribute(str(key), value, self._slot_path(path, name))

        if export["selfClose"]:
            self._visitor.tag_self_close()
            return

        self._visitor.content_start()

        for child in export["children"]:
            if isinstance(child, Tag):
                self._tag(child, path)
                continue

            if isinstance(child, Raw):
                self._visitor.raw(child)
                continue

            if isinstance(child, Markup):
                raise CompileException.markup_in_shape(type(child).__name__)

            if isinstance(child, Slot):
                self._slot(child, path)
                continue

            self._visitor.text(str(child))

        self._visitor.tag_close(export["tagName"])

    def _slot(self, slot: Slot, path: str) -> None:
        slot_path = self._slot_path(path, slot.name)

        self._visitor.slot_enter(slot, slot_path)

        if slot.kind == SlotKind.Child:
            self._tag(self._shape_tree(slot.shape, slot_path), slot_path)
        elif slot.kind == SlotKind.Each:
            self._tag(self._shape_tree(slot.shape, slot_path), slot_path + "[]")
        elif slot.kind == SlotKind.If:
            self._visitor.slot_branch(0)
            self._tag(self._shape_tree(slot.shape, slot_path), slot_path)
            if slot.else_shape is not None:
                self._visitor.slot_branch(1)
                self._tag(slot.else_shape.tree(), slot_path)

        self._visitor.slot_leave(slot, slot_path)

    @staticmethod
    def _shape_tree(shape: ShapeContract, slot_path: str) -> Tag:
        if shape is None:
            raise CompileException.missing_shape(slot_path)
        return shape.tree()

    @staticmethod
    def _slot_path(path: str, name: str) -> str:
        return name if path == "" else path + "." + name
