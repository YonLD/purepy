import math
import re
from typing import Any

from html.entities import entitydefs as _NAMED_ENTITIES

# PHP's `precision` ini, which is what its `(string)` cast renders a float at.
# It is a runtime setting rather than part of the escaping configuration, so it
# stays a module constant rather than an Escaper flag.
PRECISION = 14

# A candidate entity: a named one, or a numeric code point. The closing
# semicolon is required: purephp escapes `&#41` and `&copy` as text, which is
# also what a browser does with a name it cannot terminate.
_ENTITY_PATTERN = re.compile(r"&(#[0-9]+;|#[xX][0-9a-fA-F]+;|[a-zA-Z][a-zA-Z0-9]*;)")
# Every surrogate, paired or not. PHP stores a string as bytes, so a surrogate
# reaches htmlspecialchars() as the three invalid bytes a CESU-8 encoder would
# write and each one is substituted on its own: a matched pair becomes two
# U+FFFD, not the single character it stands for. A real astral character is
# one code point above U+FFFF and never reaches this pattern.
_SURROGATE = re.compile("[\ud800-\udfff]")

# The names PHP's get_debug_type() reports, keyed by the exact type. The error
# messages name a rejected value's type, so the wording is part of the contract:
# `null` rather than `NoneType`, `string` rather than `str`, and `array` for the
# four sequence and mapping types Python spells separately and PHP spells as
# one. Anything outside the table is an object, which PHP names by its class.
_DEBUG_TYPES = {
    type(None): "null",
    bool: "bool",
    int: "int",
    float: "float",
    str: "string",
    bytes: "string",
    list: "array",
    tuple: "array",
    dict: "array",
    set: "array",
}


class Escaper:
    """The one owner of the escaping configuration.

    purephp keeps the escape flags and the encoding in constants so generated
    code references them instead of copying the values; the same applies here.
    A text position preserves the entities a value already carries, while an
    attribute value double-encodes them, because an attribute may legitimately
    hold an `&` sequence.

    Both methods produce the same bytes as purephp's `htmlspecialchars()` with
    `ENT_QUOTES | ENT_SUBSTITUTE`, so the string renderer and the compiled
    renderer agree across the two implementations.
    """

    FLAGS = ("escape", "substitute")
    ENCODING = "UTF-8"

    DOUBLE_ENCODE_TEXT = False
    DOUBLE_ENCODE_ATTR = True

    @staticmethod
    def _substitute(value: str) -> str:
        """Replace unencodable input with U+FFFD, as ENT_SUBSTITUTE does.

        A surrogate is the case that matters: it is a valid `str` with no UTF-8
        encoding, and PHP substitutes it rather than failing. Each one is
        replaced on its own, so a matched pair yields two U+FFFD — which is what
        PHP produces, since it never sees the pair as one character.
        """
        try:
            value.encode(Escaper.ENCODING)
            return value
        except UnicodeEncodeError:
            return _SURROGATE.sub("�", value)

    @staticmethod
    def _is_entity(candidate: str) -> bool:
        """Whether a matched candidate is an entity purephp leaves intact.

        A numeric one only has to be well formed and name a code point in the
        Unicode range: purephp does not ask whether that code point has a
        character, so `&#0;` and a lone surrogate are preserved just as its
        `htmlspecialchars()` preserves them.

        A named one has to be in the HTML 4.01 table, which is the table
        `htmlspecialchars()` consults. `&notreal;` has the shape of an entity
        but names nothing, and `&apos;` names one that table predates, so both
        are text and get escaped like any other `&`.
        """
        if candidate.startswith("#"):
            digits = candidate[1:-1]

            try:
                code = int(digits[1:], 16) if digits[:1] in ("x", "X") else int(digits)
            except ValueError:
                return False

            return 0 <= code <= 0x10FFFF

        return candidate[:-1] in _NAMED_ENTITIES

    @staticmethod
    def to_string(value: Any) -> str:
        """Coerce a value to text the way purephp's `(string)` cast does.

        purephp relies on the cast at every point a value becomes text: a tag
        child, an attribute value, a slot value. Python has no such cast and
        `str()` disagrees on the two types a template actually receives — `True`
        is `"1"` and `False` is `""` rather than their `repr()`, and a float
        drops a trailing `.0` instead of gaining one. Left unconverted, that
        reaches the document: `div(active)` would print `True`.

        A float is rendered at PHP's `precision=14` in `%G` notation, which
        switches to an exponent outside 1e-4..1e14 and keeps one digit after
        the point there. One class of value still differs: a double needing
        more than 14 significant digits whose 14-digit rounding ends in a zero
        keeps the zero in purephp (`2.1723865583080E+14`) where `%G` drops it.
        """
        if value is None:
            return ""
        # bool is a subclass of int, so the two are checked before the
        # numeric branches to keep `str(True)` from being reached.
        if value is True:
            return "1"
        if value is False:
            return ""
        if isinstance(value, float):
            return Escaper._float(value)

        return str(value)

    @staticmethod
    def _float(value: float) -> str:
        """Render a float the way purephp's `(string)` cast does.

        `%G` at PHP's default `precision=14` gives the same digits; only the
        exponent form needs tidying, since the cast writes it with a digit after
        the point and without a leading zero on the exponent.
        """
        if math.isnan(value):
            return "NAN"
        if math.isinf(value):
            return "INF" if value > 0 else "-INF"

        text = "%.*G" % (PRECISION, value)

        if "E" not in text:
            return text

        mantissa, _, exponent = text.partition("E")

        if "." not in mantissa:
            mantissa += ".0"

        sign, digits = exponent[0], (exponent[1:].lstrip("0") or "0")

        return mantissa + "E" + sign + digits

    @staticmethod
    def debug_type(value: Any) -> str:
        """Name a value's type the way PHP's get_debug_type() does.

        Every message that rejects a value names its type, so the wording is
        part of what the two implementations agree on.
        """
        return _DEBUG_TYPES.get(type(value)) or type(value).__name__

    @staticmethod
    def text(value: str) -> str:
        if not Escaper.DOUBLE_ENCODE_TEXT:
            return Escaper._escape(Escaper._substitute(value), preserve=True)

        return Escaper._escape(Escaper._substitute(value), preserve=False)

    @staticmethod
    def attr(value: str) -> str:
        return Escaper._escape(Escaper._substitute(value), preserve=False)

    @staticmethod
    def attribute(key: str, value: str) -> str:
        return ' {}="{}"'.format(key, Escaper.attr(value))

    @staticmethod
    def _escape(value: str, preserve: bool) -> str:
        """Escape a value, optionally leaving the entities it already carries.

        The entities are held aside while the `&` is escaped and put back
        afterwards, which is what `double_encode: false` does natively. They are
        indexed by position rather than by a placeholder character, so a value
        that happens to contain that character keeps it.
        """
        if not preserve:
            return _replace(value)

        kept = []

        def hold(match):
            candidate = match.group(1)

            if not Escaper._is_entity(candidate):
                return match.group()

            kept.append(candidate)

            return "\x00{}\x00".format(len(kept) - 1)

        # The held entity is escaped as a unit, so its `&` is restored with the
        # rest of it rather than being encoded on the way through.
        escaped = _replace(_ENTITY_PATTERN.sub(hold, value))

        return re.sub(r"\x00(\d+)\x00", lambda m: "&" + kept[int(m.group(1))], escaped)


def _replace(value: str) -> str:
    """Escape the five characters htmlspecialchars() escapes, in its order.

    Python spells the single quote `&#x27;` where PHP spells it `&#039;`, so
    the result is normalized to the PHP spelling to keep the two byte-identical.
    """
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#039;")
    )
