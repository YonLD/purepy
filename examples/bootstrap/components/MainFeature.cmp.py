from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import a, div, h3, p


def MainFeature(*children):
    return component('MainFeature', *children)


register(MainFeature, factory=lambda: (
    div(
        h3(Slot.value('title')).class_name('fw-bold'),
        p(Slot.value('content')).class_name('text-muted'),
        a(Slot.value('linkText')).class_name('btn btn-primary btn-lg').href(Slot.value('link'))
    ).class_name('col d-flex flex-column align-items-start gap-2')
))
