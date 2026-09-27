from typing import Any, List, Optional

from ...core.Tag import Tag
from ...core.Slot import Slot
from ...core.SlotKind import SlotKind
from ...core.Escaper import Escaper
from ...core.Raw import Raw
from ...core.Markup import Markup
from ..Renderer import Renderer
from .ShapeIndex import ShapeIndex
from .RootSlots import RootSlots

HELPERS = """def _req(value, path, scope, required, default):
    if value is None:
        if required:
            raise MissingSlotException.for_path(path, scope)
        return default
    return value
"""

IMPORTS = (
    "from pure.compile.Internal.SlotRuntime import SlotRuntime\n"
    "from pure.core.MissingSlotException import MissingSlotException\n"
    "from pure.core.Escaper import Escaper\n"
)

PREAMBLE = IMPORTS + "\n" + HELPERS


class CodeGenerator:
    @staticmethod
    def imports() -> List[str]:
        return IMPORTS.strip().split("\n")

    @staticmethod
    def function(name: str, tree: Tag) -> str:
        """A module-level `def name(data):` renderer body for a tree."""
        body = CodeGenerator.__node(tree, "data", "", 1, [1])
        lines = ["def {}(data):".format(name), "    out = []"]
        lines.extend(body)
        lines.append("    return ''.join(out)")
        return "\n".join(lines) + "\n"

    @staticmethod
    def source(tree: Tag) -> str:
        """The complete generated module for a tree, without evaluating it.

        `fromSource()` feeds this back in, so the source has to stand on its
        own: the runtime prelude the renderer needs comes with it.
        """
        return PREAMBLE + "\n" + CodeGenerator.function("render", tree)

    @staticmethod
    def fromSource(source: str, id: str, slots: Optional[RootSlots] = None) -> Renderer:
        """Build a renderer from generated source, without walking the shape again."""
        return Renderer(source, id, slots)

    @staticmethod
    def compile(tree: Tag, index: ShapeIndex, slots: List[str]) -> Renderer:
        body = CodeGenerator.__node(tree, "data", "", 1, [1])
        lines = ["def render(data):", "    out = []"]
        lines.extend(body)
        lines.append("    return ''.join(out)")
        return Renderer(PREAMBLE + "\n" + "\n".join(lines) + "\n", index.id(), slots)

    @staticmethod
    def __indent(depth: int) -> str:
        return "    " * depth

    @staticmethod
    def __node(
        tag: Tag, scope: str, path: str, depth: int, counter: List[int]
    ) -> List[str]:
        pad = CodeGenerator.__indent(depth)
        out = [pad + "out.append('<' + {} )".format(repr(tag.get_tag_name()))]

        for key, value in tag.get_attrs().items():
            if isinstance(value, Slot):
                out.extend(CodeGenerator.__attr(key, value, scope, path, depth))
            else:
                out.append(
                    pad
                    + "out.append(' ' + {!r} + '=\"' + {!r} + '\"')".format(
                        key, Escaper.attr(str(value))
                    )
                )

        if tag.get_self_close():
            out.append(pad + "out.append(' />')")
            return out

        out.append(pad + "out.append('>')")
        for child in tag.get_children():
            out.extend(CodeGenerator.__child(child, scope, path, depth, counter))
        out.append(pad + "out.append('</' + {} + '>')".format(repr(tag.get_tag_name())))
        return out

    @staticmethod
    def __attr(key: str, slot: Slot, scope: str, path: str, depth: int) -> List[str]:
        pad = CodeGenerator.__indent(depth)
        slot_path = CodeGenerator.__join(path, slot.name)
        required = bool(slot.is_required)
        default = repr(slot.default_value)
        return [
            pad
            + "out.append(SlotRuntime.attr_open({0!r}, _req({1}.get({2!r}), {3!r}, {1}, {4}, {5}), {3!r}))".format(  # noqa: E501
                key, scope, slot.name, slot_path, required, default
            )
        ]

    @staticmethod
    def __child(
        child: Any, scope: str, path: str, depth: int, counter: List[int]
    ) -> List[str]:
        pad = CodeGenerator.__indent(depth)

        if isinstance(child, Tag):
            return CodeGenerator.__node(child, scope, path, depth, counter)

        if isinstance(child, Raw):
            return [pad + "out.append({})".format(repr(str(child)))]

        if isinstance(child, Markup):
            return [pad + "out.append(str({}))".format(repr(str(child)))]

        if isinstance(child, Slot):
            return CodeGenerator.__slot(child, scope, path, depth, counter)

        return [pad + "out.append({})".format(repr(Escaper.text(str(child))))]

    @staticmethod
    def __slot(
        slot: Slot, scope: str, path: str, depth: int, counter: List[int]
    ) -> List[str]:
        pad = CodeGenerator.__indent(depth)
        slot_path = CodeGenerator.__join(path, slot.name)
        required = bool(slot.is_required)
        default = repr(slot.default_value)

        if slot.kind == SlotKind.Value:
            return [
                pad
                + "out.append(SlotRuntime.text(_req({0}.get({1!r}), {2!r}, {0}, {3}, {4}), {2!r}))".format(  # noqa: E501
                    scope, slot.name, slot_path, required, default
                )
            ]

        if slot.kind == SlotKind.Raw:
            return [
                pad
                + "out.append(SlotRuntime.raw(_req({0}.get({1!r}), {2!r}, {0}, {3}, {4}), {2!r}))".format(  # noqa: E501
                    scope, slot.name, slot_path, required, default
                )
            ]

        if slot.kind == SlotKind.Child:
            return CodeGenerator.__scoped(slot, scope, path, depth, counter, "scope")

        if slot.kind == SlotKind.Each:
            return CodeGenerator.__scoped(slot, scope, path, depth, counter, "items")

        if slot.kind == SlotKind.If:
            return CodeGenerator.__conditional(slot, scope, path, depth, counter)

        return []

    @staticmethod
    def __scoped(
        slot: Slot, scope: str, path: str, depth: int, counter: List[int], helper: str
    ) -> List[str]:
        pad = CodeGenerator.__indent(depth)
        slot_path = CodeGenerator.__join(path, slot.name)
        index = counter[0]
        counter[0] += 1

        if helper == "scope":
            inner = "v{}".format(index)
            out = [
                pad
                + "if _req({0}.get({1!r}), {2!r}, {0}, True, None) is None:".format(
                    scope, slot.name, slot_path
                ),
                CodeGenerator.__indent(depth + 1)
                + "raise MissingSlotException.for_path({0!r}, {1})".format(
                    slot_path, scope
                ),
                pad
                + "{0} = SlotRuntime.scope({1}.get({2!r}), {3!r})".format(
                    inner, scope, slot.name, slot_path
                ),
            ]
        else:
            inner = "i{}".format(index)
            out = [
                pad
                + "if _req({0}.get({1!r}), {2!r}, {0}, True, None) is None:".format(
                    scope, slot.name, slot_path
                ),
                CodeGenerator.__indent(depth + 1)
                + "raise MissingSlotException.for_path({0!r}, {1})".format(
                    slot_path, scope
                ),
                pad
                + "for _slot in SlotRuntime.items(_req({0}.get({1!r}), {2!r}, {0}, True, None), {2!r}):".format(  # noqa: E501
                    scope, slot.name, slot_path
                ),
                CodeGenerator.__indent(depth + 1) + "{0} = _slot".format(inner),
            ]

        if slot.shape is not None:
            # A child scope is a plain binding, so its body sits at this level;
            # an each() loop introduced a block, so its body is one level in.
            body_depth = depth if helper == "scope" else depth + 1
            out.extend(
                CodeGenerator.__node(
                    slot.shape.tree(), inner, slot_path, body_depth, counter
                )
            )

        return out

    @staticmethod
    def __conditional(
        slot: Slot, scope: str, path: str, depth: int, counter: List[int]
    ) -> List[str]:
        pad = CodeGenerator.__indent(depth)
        slot_path = CodeGenerator.__join(path, slot.name)
        out = [pad + "if {0}.get({1!r}):".format(scope, slot.name)]

        if slot.shape is not None:
            out.extend(
                CodeGenerator.__node(
                    slot.shape.tree(), scope, slot_path, depth + 1, counter
                )
            )
        else:
            out.append(CodeGenerator.__indent(depth + 1) + "pass")

        if slot.else_shape is not None:
            out.append(pad + "else:")
            out.extend(
                CodeGenerator.__node(
                    slot.else_shape.tree(), scope, slot_path, depth + 1, counter
                )
            )

        return out

    @staticmethod
    def __join(path: str, name: str) -> str:
        return "{}.{}".format(path, name) if path else name
