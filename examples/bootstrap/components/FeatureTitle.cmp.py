import os
from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div, h4, p

from pure.loader import load_module
Icon = load_module(os.path.join(os.path.dirname(__file__), 'Icon.cmp.py'), 'Icon').Icon


def FeatureTitle(*children):
    return component('FeatureTitle', *children)


register(FeatureTitle,
    factory=lambda: (
        div(
            div(
                Slot.raw('icon')
            ).class_name('feature-icon-small d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-4 rounded-3'),
            h4(Slot.value('title')).class_name('fw-semibold mb-0'),
            p(Slot.value('content')).class_name('text-muted')
        ).class_name('col d-flex flex-column gap-2')
    ),
    prepare=lambda icon, title, content: {
        'icon': Icon().href('#' + icon),
        'title': title,
        'content': content,
    }
)
