from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import a, div, h5, li, ul


def ColLinks(*children):
    return component('ColLinks', *children)


register(ColLinks, factory=lambda: (
    div(
        h5(Slot.value('title')),
        ul(
            Slot.each('links', li(a(Slot.value('text')).class_name('text-muted').href(Slot.value('href'))))
        ).class_name('list-unstyled text-small')
    ).class_name('col-6 col-md')
))
