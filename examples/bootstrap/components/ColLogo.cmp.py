from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div, img, small


def ColLogo(*children):
    return component('ColLogo', *children)


register(ColLogo, factory=lambda: (
    div(
        img().class_name('mb-2').src(Slot.value('src')).width(Slot.value('width')).height(Slot.value('height')),
        small(Slot.value('text')).class_name('d-block mb-3 text-muted')
    ).class_name('col-12 col-md')
))
