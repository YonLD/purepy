from typing import Union, Tuple
from pure.core.Raw import Raw
from pure.core import Tag
from .XML import XML

SELF_CLOSE_SVG_TAGS = [
    'animate',
    'animateMotion',
    'circle',
    'ellipse',
    'feBlend',
    'feColorMatrix',
    'feDisplacementMap',
    'feDropShadow',
    'feGaussianBlur',
    'feImage',
    'image',
    'line',
    'mpath',
    'path',
    'polygon',
    'polyline',
    'rect',
    'stop',
    'use'
]

class SVG(XML):
    def __init__(self, tag_name: str, children: Tuple[Union[str, Raw, Tag]]):
        super().__init__(tag_name, children)
        if tag_name.lower() in SELF_CLOSE_SVG_TAGS:
            self.set_self_close(True)
