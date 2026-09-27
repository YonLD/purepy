import html
import re

_ENTITY_PATTERN = re.compile(r"&(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);")
_PLACEHOLDER = "\x00"


class Escaper:
    """The one owner of the escaping configuration.

    purephp keeps the escape flags and the encoding in constants so generated
    code references them instead of copying the values; the same applies here.
    A text position preserves the entities a value already carries, while an
    attribute value double-encodes them, because an attribute may legitimately
    hold an `&` sequence.
    """

    FLAGS = ("escape", "substitute")
    ENCODING = "UTF-8"

    DOUBLE_ENCODE_TEXT = False
    DOUBLE_ENCODE_ATTR = True

    @staticmethod
    def _substitute(value: str) -> str:
        """Replace unencodable input with U+FFFD, as ENT_SUBSTITUTE does."""
        if not any("\ud800" <= ch <= "\udfff" for ch in value):
            return value

        return value.encode(Encoder(), "surrogateescape").decode(Encoder(), "replace")

    @staticmethod
    def _preserve_entities(value: str):
        entities = []

        def replacer(match):
            entities.append(match.group())
            return _PLACEHOLDER

        return _ENTITY_PATTERN.sub(replacer, value), entities

    @staticmethod
    def _restore_entities(value: str, entities) -> str:
        for entity in entities:
            value = value.replace(_PLACEHOLDER, entity, 1)

        return value

    @staticmethod
    def text(value: str) -> str:
        if not Escaper.DOUBLE_ENCODE_TEXT:
            value, entities = Escaper._preserve_entities(Escaper._substitute(value))
            return Escaper._restore_entities(html.escape(value, quote=False), entities)

        return html.escape(Escaper._substitute(value), quote=False)

    @staticmethod
    def attr(value: str) -> str:
        return html.escape(Escaper._substitute(value), quote=True)

    @staticmethod
    def attribute(key: str, value: str) -> str:
        return ' {}="{}"'.format(key, Escaper.attr(value))


def Encoder() -> str:
    return Escaper.ENCODING
