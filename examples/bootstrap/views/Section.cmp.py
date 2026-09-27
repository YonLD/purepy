from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div, h2

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.services import FeaturesService


def Section(*children):
    return component('Section', *children)


register(Section,
    factory=lambda: (
        div(
            h2(Slot.value('title')).class_name('pb-2 border-bottom'),
            div(Slot.raw('contents')).class_name(Slot.value('class'))
        ).class_name('container px-4 py-5')
    ),
    prepare=lambda section, class_, item: {
        'title': FeaturesService.section(section)['title'],
        'contents': [str(item(record)) for record in FeaturesService.section(section)['items']],
        'class': class_,
    }
)
