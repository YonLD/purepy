from typing import Union, Tuple

from .Raw import Raw
from .Tag import Tag, TagFactory
from .XML import XML

SELF_CLOSE_SVG_TAGS = {
    "animate",
    "animateMotion",
    "animateTransform",
    "circle",
    "ellipse",
    "feBlend",
    "feColorMatrix",
    "feComposite",
    "feConvolveMatrix",
    "feDistantLight",
    "feDisplacementMap",
    "feDropShadow",
    "feFlood",
    "feFuncA",
    "feFuncB",
    "feFuncG",
    "feFuncR",
    "feGaussianBlur",
    "feImage",
    "feMergeNode",
    "feMorphology",
    "feOffset",
    "fePointLight",
    "feSpotLight",
    "feTile",
    "feTurbulence",
    "image",
    "line",
    "mpath",
    "path",
    "polygon",
    "polyline",
    "rect",
    "set",
    "stop",
    "use",
    "view",
}


class SVG(XML, metaclass=TagFactory):
    def __init__(self, tag_name: str, children: Tuple[Union[str, Raw, Tag], ...] = ()):
        super().__init__(tag_name, children)
        if not children and tag_name in SELF_CLOSE_SVG_TAGS:
            self.set_self_close(True)

    def guardAttributeName(self, key: str) -> None:
        self.guardStandardAttribute(key)

    def isDocumentRoot(self) -> bool:
        return False
