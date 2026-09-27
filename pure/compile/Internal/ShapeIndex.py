import hashlib
import sys
from typing import Any, Dict, List

from ..Compile import Compile
from ...core.Raw import Raw
from ...core.Slot import Slot
from ...core.Tag import Tag
from .ShapeVisitor import ShapeVisitor
from .ShapeWalker import ShapeWalker


class ShapeIndex(ShapeVisitor):
    """The structural fingerprint of a shape.

    The fingerprint is derived through the same ShapeWalker the code generator
    uses, so both see an identical traversal: the same tags, attributes, slots
    and branch labels in the same order. Slot paths, the required flag and the
    default are part of the fingerprint, so two shapes that differ only in how a
    slot is bound never share a cache entry.
    """

    def __init__(self):
        self._parts: List[str] = []
        self._id: str = ""

    @staticmethod
    def of(tree: Tag) -> "ShapeIndex":
        index = ShapeIndex()
        ShapeWalker(index).walk(tree)

        salt = "{}\x00{}.{}".format(
            Compile.CACHE_VERSION, sys.version_info[0], sys.version_info[1]
        )
        index._id = hashlib.sha1(
            ("\x00".join(index._parts) + "\x00" + salt).encode()
        ).hexdigest()

        return index

    def id(self) -> str:
        return self._id

    # --- ShapeVisitor -----------------------------------------------------

    def tag_open(self, tag: Tag, path: str, export: Dict[str, Any]) -> bool:
        self._parts.append("<" + export["tagName"])
        self._parts.append("selfClose:" + ("1" if export["selfClose"] else "0"))
        return True

    def attribute(self, key: str, value, slot_path: str) -> None:
        if isinstance(value, Slot):
            self._parts.append(
                "attr:" + key + "=" + self._describe_slot(value, slot_path)
            )
        else:
            self._parts.append("attr:" + key + "=" + str(value))

    def tag_self_close(self) -> None:
        pass

    def content_start(self) -> None:
        pass

    def tag_close(self, tag_name: str) -> None:
        self._parts.append("</" + tag_name)

    def text(self, text: str) -> None:
        self._parts.append("text:" + text)

    def raw(self, raw: Raw) -> None:
        self._parts.append("raw:" + str(raw))

    def slot_enter(self, slot: Slot, slot_path: str) -> None:
        self._parts.append(self._describe_slot(slot, slot_path))

    def slot_branch(self, label) -> None:
        self._parts.append("branch:" + str(label))

    def slot_leave(self, slot: Slot, slot_path: str) -> None:
        pass

    @staticmethod
    def _describe_slot(slot: Slot, slot_path: str) -> str:
        default = "N" if slot.default_value is None else repr(slot.default_value)

        return "slot:{}:{}:required:{}:default:{}".format(
            slot.kind.name, slot_path, "1" if slot.is_required else "0", default
        )
