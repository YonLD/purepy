import os
from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import a, div, h3, p
from pure.svg import svg, use

from pure.loader import load_module
Icon = load_module(os.path.join(os.path.dirname(__file__), 'Icon.cmp.py'), 'Icon').Icon


def IconColumn(*children):
    return component('IconColumn', *children)


register(IconColumn,
    factory=lambda: (
        div(
            div(
                Slot.raw('icon')
            ).class_name('feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3'),
            h3(Slot.value('title')).class_name('fs-2'),
            p(Slot.value('content')),
            a(
                Slot.value('linkText'),
                svg(use().href('#chevron-right')).class_name('bi').width('1em').height('1em')
            ).href(Slot.value('link')).class_name('icon-link d-inline-flex align-items-center')
        ).class_name('feature col')
    ),
    prepare=lambda icon, title, content, link, linkText: {
        'icon': Icon().href('#' + icon),
        'title': title,
        'content': content,
        'link': link,
        'linkText': linkText,
    }
)
