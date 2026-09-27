import os
from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import a, div, h3, p

from pure.loader import load_module
Icon = load_module(os.path.join(os.path.dirname(__file__), 'Icon.cmp.py'), 'Icon').Icon


def HangingIcon(*children):
    return component('HangingIcon', *children)


register(HangingIcon,
    factory=lambda: (
        div(
            div(
                Slot.raw('icon')
            ).class_name('icon-square text-bg-light d-inline-flex align-items-center justify-content-center fs-4 flex-shrink-0 me-3'),
            div(
                h3(Slot.value('title')).class_name('fs-2'),
                p(Slot.value('content')),
                a(Slot.value('linkText')).href(Slot.value('link')).class_name('btn btn-primary')
            )
        ).class_name('col d-flex align-items-start')
    ),
    prepare=lambda icon, title, content, link, linkText: {
        'icon': Icon().href('#' + icon),
        'title': title,
        'content': content,
        'link': link,
        'linkText': linkText,
    }
)
