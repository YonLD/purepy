from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import a


def NavLink(*children):
    return component('NavLink', *children)


register(NavLink, factory=lambda: (
    a(Slot.value('text')).class_name(Slot.value('class').default('')).href(Slot.value('href'))
))
