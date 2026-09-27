from pure.component.Call import Call
from pure.component.Prop import Prop
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import button, div, h1, h4, li, small, ul


def Card(*children):
    return component('Card', *children)


register(Card,
    factory=lambda: (
        div(
            div(
                h4(Slot.value('type')).class_name('my-0 font-weight-normal')
            ).class_name('card-header'),
            div(
                h1('$', Slot.value('price'), ' ', small('/ mo').class_name('text-muted')).class_name('card-title pricing-card-title'),
                ul(Slot.each('features', li(Slot.value('value')))).class_name('list-unstyled mt-3 mb-4'),
                button(Slot.value('text')).type('button').class_name(Slot.value('class'))
            ).class_name('card-body')
        ).class_name('card mb-4 box-shadow')
    ),
    prepare=lambda type, price, text, class_, features=Prop(item='value'): {
        'type': type,
        'price': price,
        'features': [{'value': feature} for feature in features],
        'text': text,
        'class': class_,
    }
)
