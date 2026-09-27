import re
from typing import Any, List, Optional

from ...core.Tag import Tag
from ...core.Slot import Slot
from ...core.SlotKind import SlotKind
from ...core.Escaper import Escaper
from .CompileException import CompileException
from .ScopeTypes import ScopeTypes

# Slot names the plain view reserves for itself: the ones ScopeTypes would
# otherwise bind as a local, plus the loop counters the generator emits.
RESERVED = frozenset({"self", "globals", "data", "kind", "out", "view"})

_AUTO_LOCAL = re.compile(r"^(item|v|kind)\d+$")

PRELUDE = '''from html import escape as _escape
from typing import Any, Dict, Iterable, List, Optional


def _text(value):
    """Escape a value for a text position, like the compiled renderer."""
    return '' if value is None else _escape(str(value), quote=False)


def _attr(name, value):
    """Build one name="value" chunk, omitted for a null value."""
    if value is None or value is False:
        return ''
    if value is True:
        return ' ' + name + '="' + name + '"'
    return ' ' + name + '="' + _escape(str(value), quote=True) + '"'


def _raw(value):
    """Join an iterable verbatim, like the compiled renderer."""
    if value is None:
        return ''
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return ''.join('' if v is None else str(v) for v in value)
    return str(value)
'''


class PlainGenerator:
    """Generates a plain Python view: a template with no library dependency.

    The view is called by unpacking the view data into its parameters, so a
    root slot reads as an ordinary local and a nested slot as the dict it lives
    in:

        html = view(**data)

    Values are escaped the way the compiled renderer escapes them, so a plain
    view renders byte-identical output for ordinary data. The strict slot
    semantics (MissingSlotException, per-element validation) belong to the
    compiled renderer and are not part of a plain view: a missing slot is a
    missing argument, a null attribute prints no attribute at all.
    """

    @staticmethod
    def view(tree: Tag) -> str:
        counter = [0]
        body = PlainGenerator.__node(tree, "", "", 1, counter)
        lines = [ScopeTypes.signature(tree), "    out = []"]

        # A document root keeps its own header, as purephp's plain view does;
        # in Python it has to be emitted by the function, not written above it.
        if tree.isDocumentRoot():
            lines.append("    out.append({})".format(repr(tree.documentHeader())))

        lines.extend(body)
        lines.append("    return ''.join(out)")

        return PRELUDE + "\n" + "\n".join(lines) + "\n"

    @staticmethod
    def __indent(depth: int) -> str:
        return "    " * depth

    @staticmethod
    def __access(scope: str, name: str) -> str:
        # A root slot is a parameter of the view, under its sanitized name. A
        # name that cannot be an identifier at all (`user-name`) is not a
        # parameter: it stays an offset of the view data.
        if scope == "" and PlainGenerator.local(name) is not None:
            return ScopeTypes.parameter(name)

        target = "data" if scope == "" else scope

        return "{}.get({})".format(target, repr(name))

    @staticmethod
    def local(name: str) -> Optional[str]:
        """The local variable a root slot binds to, or None when the slot name
        cannot be an ordinary view parameter.

        Shared with ScopeTypes, which decides whether a type annotation names a
        local or a `data` offset.
        """
        import keyword

        if (
            not name.isidentifier()
            or keyword.iskeyword(name)
            or keyword.issoftkeyword(name)
        ):
            return None

        lower = name.lower()

        if lower in RESERVED or lower.startswith("pure") or _AUTO_LOCAL.match(lower):
            return None

        return name

    @staticmethod
    def attribute(
        key: str, value, slot_path: str, scope: str = "", depth: int = 0
    ) -> List[str]:
        """The lines writing one attribute.

        The name stays markup and the value is an echo, the way a hand-written
        view writes it. A slot in attribute position has to be a value slot;
        anything else would silently lose its shape, so it is rejected the same
        way the compiled renderer rejects it.
        """
        pad = PlainGenerator.__indent(depth)

        if not isinstance(value, Slot):
            return [pad + "out.append(_attr({0!r}, {1!r}))".format(key, str(value))]

        if value.kind != SlotKind.Value:
            raise CompileException.slot_in_attribute_position(value.kind, slot_path)

        return [
            pad
            + "out.append(_attr({0!r}, {1}))".format(
                key, PlainGenerator.__access(scope, value.name)
            )
        ]

    @staticmethod
    def __node(
        tag: Tag, scope: str, path: str, depth: int, counter: List[int]
    ) -> List[str]:
        pad = PlainGenerator.__indent(depth)
        out = [pad + "out.append({})".format(repr("<" + tag.get_tag_name()))]

        for key, value in tag.get_attrs().items():
            name = value.name if isinstance(value, Slot) else str(key)
            slot_path = name if path == "" else path + "." + name
            out.extend(
                PlainGenerator.attribute(str(key), value, slot_path, scope, depth)
            )

        if tag.get_self_close():
            out.append(pad + "out.append({})".format(repr(" />")))
            return out

        out.append(pad + "out.append({})".format(repr(">")))
        for child in tag.get_children():
            out.extend(PlainGenerator.__child(child, scope, path, depth, counter))
        out.append(pad + "out.append({})".format(repr("</" + tag.get_tag_name() + ">")))
        return out

    @staticmethod
    def __child(
        child: Any, scope: str, path: str, depth: int, counter: List[int]
    ) -> List[str]:
        pad = PlainGenerator.__indent(depth)

        if isinstance(child, Tag):
            return PlainGenerator.__node(child, scope, path, depth, counter)

        if isinstance(child, Slot):
            return PlainGenerator.__slot(child, scope, path, depth, counter)

        return [pad + "out.append({})".format(repr(Escaper.text(str(child))))]

    @staticmethod
    def __slot(
        slot: Slot, scope: str, path: str, depth: int, counter: List[int]
    ) -> List[str]:
        pad = PlainGenerator.__indent(depth)
        access = PlainGenerator.__access(scope, slot.name)

        if slot.kind == SlotKind.Value:
            return [pad + "out.append(_text({}))".format(access)]

        if slot.kind == SlotKind.Raw:
            return [pad + "out.append(_raw({}))".format(access)]

        if slot.kind == SlotKind.If:
            out = [pad + "if {}:".format(access)]
            if slot.shape is not None:
                out.extend(
                    PlainGenerator.__node(
                        slot.shape.tree(), scope, path, depth + 1, counter
                    )
                )
            else:
                out.append(PlainGenerator.__indent(depth + 1) + "pass")
            if slot.else_shape is not None:
                out.append(pad + "else:")
                out.extend(
                    PlainGenerator.__node(
                        slot.else_shape.tree(), scope, path, depth + 1, counter
                    )
                )
            return out

        if slot.kind in (SlotKind.Child, SlotKind.Each):
            index = counter[0]
            counter[0] += 1
            inner = "i{}".format(index)
            slot_path = "{}.{}".format(path, slot.name) if path else slot.name

            if slot.kind == SlotKind.Child:
                out = [pad + "{} = {}".format(inner, access)]
                body_depth = depth
            else:
                out = [pad + "for {} in ({} or ()):".format(inner, access)]
                out.append(
                    PlainGenerator.__indent(depth + 1) + "{} = {}".format(inner, inner)
                )
                body_depth = depth + 1

            if slot.shape is not None:
                out.extend(
                    PlainGenerator.__node(
                        slot.shape.tree(), inner, slot_path, body_depth, counter
                    )
                )

            return out

        return []

    @staticmethod
    def document(tree: Tag) -> str:
        return tree.documentHeader() if tree.isDocumentRoot() else ""
