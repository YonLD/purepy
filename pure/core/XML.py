from typing import Union, Tuple

from .Raw import Raw
from .Tag import Tag


class XML(Tag):
    DOCUMENT_HEADER = '<?xml version="1.0"?>'

    def __init__(self, tag_name: str, children: Tuple[Union[str, Raw, Tag], ...] = ()):
        super().__init__(tag_name, children)

    def isDocumentRoot(self) -> bool:
        return True

    def defaultHeader(self) -> str:
        return self.DOCUMENT_HEADER

    def guardAttributeName(self, key: str) -> None:
        """An XML tree names its own elements and attributes, so no standard
        attribute list applies and the development guard stays quiet.
        """
        pass
