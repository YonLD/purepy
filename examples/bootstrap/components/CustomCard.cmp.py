from pure.component.Call import Call
from pure.component.Prop import Prop
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div, h3, img, li, small, ul
from pure.svg import svg, use


def CustomCard(*children):
    return component('CustomCard', *children)


register(CustomCard,
    factory=lambda: (
        div(
            div(
                div(
                    h3(Slot.value('title')).class_name('pt-5 mt-5 mb-4 display-6 lh-1 fw-bold'),
                    ul(
                        li(
                            img().src(Slot.value('icon')).alt('Bootstrap').width('32').height('32').class_name('rounded-circle border border-white')
                        ).class_name('me-auto'),
                        li(
                            svg(use().href('#geo-fill')).class_name('bi me-2').width('1em').height('1em'),
                            small(Slot.value('location'))
                        ).class_name('d-flex align-items-center me-3'),
                        li(
                            svg(use().href('#calendar3')).class_name('bi me-2').width('1em').height('1em'),
                            small(Slot.value('date'))
                        ).class_name('d-flex align-items-center'),
                    ).class_name('d-flex list-unstyled mt-auto')
                ).class_name('d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1')
            ).class_name('card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg').style(Slot.value('style'))
        ).class_name('col')
    ),
    prepare=lambda title, icon, location, date, bgImg=Prop(slot='style'): {
        'title': title,
        'icon': icon,
        'location': location,
        'date': date,
        'style': "background-image: url('{}');".format(bgImg),
    }
)
