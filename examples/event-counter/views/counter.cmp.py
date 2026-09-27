from pure.compile.Compile import Compile
from pure.compile.Shape import Shape
from pure.compile.Template import Template
from pure.component.Call import Call
from pure.core.Slot import Slot
from pure.component.functions import component, register
from pure.html import button, div, h1, span
from pure.utils import renderHTML


def CounterPageShape():
    shape = getattr(CounterPageShape, '_shape', None)
    if shape is None:
        shape = Compile.shape(
            div(
                h1('JavaScript Counter App'),
                div(
                    button('+').id('add').onclick('handleAdd()'),
                    span(Slot.value('initial')).id('output'),
                    button('-').id('subtract')
                ).class_name('counter-container')
            )
        )
        CounterPageShape._shape = shape
    return shape


def Counter(*children):
    return component('Counter', *children)


register(Counter, lambda: CounterPageShape())


def counter_page(data):
    return renderHTML(component('Counter').initial(data['initial']))
