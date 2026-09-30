import re
import weakref
from typing import Any, List, Optional

from ...core.Tag import Tag
from ...core.Slot import Slot
from ...core.SlotKind import SlotKind
from ...core.Escaper import Escaper
from ...core.Markup import Markup
from ...core.Raw import Raw
from .CompileException import CompileException
from .RootSlots import RootSlots
from .ScopeTypes import ScopeTypes

# Slot names the plain view reserves for itself: the ones ScopeTypes would
# otherwise bind as a local, plus the loop counters the generator emits.
RESERVED = frozenset({"self", "globals", "data", "kind", "out", "view"})

_AUTO_LOCAL = re.compile(r"^(item|v|kind)\d+$")

# Per-compile memo of has_slots(), keyed weakly by the tag so a finished compile
# does not keep a shape alive. view() installs a fresh one per tree.
_SLOT_CACHE = weakref.WeakKeyDictionary()

PRELUDE = '''from collections.abc import Mapping
from html import escape as _escape
from typing import Any, Dict, Iterable, List, Optional, Union


def _str(value):
    """Coerce a value to text the way the PHP (string) cast does.

    A bool renders as "1" or nothing rather than its repr, and a float is
    written at PHP's precision of 14 significant digits in %G notation, which
    switches to an exponent outside 1e-4..1e14 and keeps one digit after the
    point there. This is a copy of Pure\\\\Core\\\\Escaper::to_string(), so a plain
    view renders the same bytes as the compiled renderer.
    """
    if value is None:
        return ''
    if value is True:
        return '1'
    if value is False:
        return ''
    if isinstance(value, float):
        if value != value:
            return 'NAN'
        if value == float('inf'):
            return 'INF'
        if value == float('-inf'):
            return '-INF'
        text = '%.*G' % (14, value)
        if 'E' in text:
            mantissa, _, exponent = text.partition('E')
            if '.' not in mantissa:
                mantissa += '.0'
            sign, digits = exponent[0], (exponent[1:].lstrip('0') or '0')
            text = mantissa + 'E' + sign + digits
        return text
    return str(value)


def _text(value):
    """Escape a value for a text position, like the compiled renderer."""
    return _escape(_str(value), quote=False)


def _attr(name, value):
    """Build one name="value" chunk.

    A plain view writes the value as an echo, the way a hand-written view does,
    so the value is cast and escaped like any other and a null one writes an
    empty string rather than dropping the attribute. That is what purephp's
    plain view emits, and it differs from the compiled renderer on purpose:
    there, SlotRuntime.attr_open() turns a true value into a bare name.
    """
    return ' ' + name + '="' + _escape(_str(value), quote=True) + '"'


def _raw(value):
    """Join an iterable verbatim, like the compiled renderer."""
    if value is None:
        return ''
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return ''.join(_str(v) for v in value)
    return _str(value)


def _items(value):
    """Read a list slot the way the compiled renderer does.

    A mapping yields its values, as iterating the equivalent PHP array does,
    and a string is not iterable even though Python can step it. This is a
    copy of Pure\\\\Compile\\\\Internal\\\\SlotRuntime::items().
    """
    if value is None:
        return ()
    if isinstance(value, Mapping):
        return value.values()
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return value
    return value
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
        # A fresh memo per compile, so a shape rebuilt from the same tags is
        # still analyzed against its own subtree.
        PlainGenerator._SLOT_CACHE = weakref.WeakKeyDictionary()

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

        if scope != "":
            return "{}.get({})".format(scope, repr(name))

        # The root offsets share one mapping, which is None when the view was
        # called with only its named parameters.
        return "(data or {{}}).get({!r})".format(name)

    @staticmethod
    def has_slots(tag: Tag) -> bool:
        """Whether the subtree reads any slot.

        Memoized per tag: without the cache this walks every descendant again
        for each ancestor, and compile time turns quadratic on a deep tree.
        """
        cached = PlainGenerator._SLOT_CACHE.get(tag)

        if cached is not None:
            return cached

        found = False

        for value in tag.get_attrs().values():
            if isinstance(value, Slot):
                found = True
                break

        if not found:
            for child in tag.get_children():
                if isinstance(child, Slot) or (
                    isinstance(child, Tag) and PlainGenerator.has_slots(child)
                ):
                    found = True
                    break

        PlainGenerator._SLOT_CACHE[tag] = found

        return found

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
            return [
                pad
                + "out.append(_attr({0!r}, {1!r}))".format(
                    key, Escaper.to_string(value)
                )
            ]

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

        # A slot-free subtree is static markup: its output is fully known at
        # compile time, so it folds into one literal instead of a line per tag.
        # The string renderer owns the escaping, so folding is byte-identical
        # to walking the subtree.
        if not PlainGenerator.has_slots(tag):
            return [pad + "out.append({})".format(repr(tag.render()))]

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

        # Raw and Markup are already-rendered output the caller vouched for, so
        # a plain view emits them verbatim instead of escaping them the way it
        # escapes a plain string.
        if isinstance(child, (Raw, Markup)):
            return [pad + "out.append({})".format(repr(Escaper.to_string(child)))]

        return [
            pad + "out.append({})".format(repr(Escaper.text(Escaper.to_string(child))))
        ]

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
                body_path = slot_path
            else:
                out = [pad + "for {} in _items({}):".format(inner, access)]

                # The runtime binds a scalar item to the one key an item shape
                # renders; a plain view has no runtime, so it does the same with
                # plain Python and stays byte-identical for the data both forms
                # accept.
                key = RootSlots.itemKey(RootSlots.itemManifest(slot.shape))

                if key is not None:
                    out.append(
                        PlainGenerator.__indent(depth + 1)
                        + (
                            "{0} = {0} if isinstance({0}, dict) "
                            "else {{{1!r}: {0}}}".format(inner, key)
                        )
                    )

                body_depth = depth + 1
                body_path = slot_path + "[]"

            if slot.shape is not None:
                out.extend(
                    PlainGenerator.__node(
                        slot.shape.tree(), inner, body_path, body_depth, counter
                    )
                )

            return out

        return []
