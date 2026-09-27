from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.svg import svg, use


def Icon(*children):
    return component('Icon', *children)


register(Icon, factory=lambda: (
    svg(use().href(Slot.value('href')))
    .class_name(Slot.value('class').default('bi'))
    .width(Slot.value('width').default('1em'))
    .height(Slot.value('height').default('1em'))
))
