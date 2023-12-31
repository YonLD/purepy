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
    def __init__(self, tag_name: str):
        super().__init__(tag_name)
        if tag_name.lower() in SELF_CLOSE_SVG_TAGS:
            self.set_self_close(True)
