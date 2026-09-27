from typing import Union

from .core.HTML import HTML
from .core.XML import XML
from .component.Call import Call


def renderHTML(node: Union[HTML, Call]) -> str:
    return HTML.DOCUMENT_HEADER + node.render()


def renderXML(node: Union[XML, Call]) -> str:
    return XML.DOCUMENT_HEADER + node.render()
