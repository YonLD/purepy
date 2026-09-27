from pure.component.Call import Call
from pure.component.functions import component, register
from pure.html import div


def Divider(*children):
    return component('Divider', *children)


register(Divider, factory=lambda: (
    div().class_name('b-example-divider')
))
