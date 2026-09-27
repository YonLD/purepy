import os
from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div, h3, p

from pure.loader import load_module
Icon = load_module(os.path.join(os.path.dirname(__file__), 'Icon.cmp.py'), 'Icon').Icon


def CellIcon(*children):
    return component('CellIcon', *children)


register(CellIcon,
    factory=lambda: (
        div(
            Slot.raw('icon'),
            div(
                h3(Slot.value('title')).class_name('fw-bold mb-0 fs-4'),
                p(Slot.value('content'))
            )
        ).class_name('col d-flex align-items-start')
    ),
    prepare=lambda icon, title, content: {
        'icon': Icon().href('#' + icon).class_name('bi text-muted flex-shrink-0 me-3').width('1.75em').height('1.75em'),
        'title': title,
        'content': content,
    }
)
