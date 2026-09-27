from typing import Union, Tuple

from .Raw import Raw
from .Tag import Tag

SELF_CLOSE_HTML_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
}


class HTML(Tag):
    DOCUMENT_HEADER = "<!DOCTYPE html>"

    def __init__(self, tag_name: str, children: Tuple[Union[str, Raw, Tag], ...] = ()):
        super().__init__(tag_name, children)
        if tag_name.lower() in SELF_CLOSE_HTML_TAGS:
            self.set_self_close(True)

    def isDocumentRoot(self) -> bool:
        return self.get_tag_name().lower() == "html"

    def defaultHeader(self) -> str:
        return self.DOCUMENT_HEADER

    def guardAttributeName(self, key: str) -> None:
        self.guardStandardAttribute(key)
