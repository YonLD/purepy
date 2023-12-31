from typing import Dict
from pure.html import div, h3, ul, li, img, small
from .Icon import Icon

def CustomCard(props: Dict[str, str]):
    title = props['title']
    icon = props['icon']
    location = props['location']
    date = props['date']
    bgImg = props['bgImg']

    return (
        div(
            div(
                div(
                    h3(title).class_name('pt-5 mt-5 mb-4 display-6 lh-1 fw-bold'),
                    ul(
                        li(
                            img().src(icon).alt('Bootstrap').width('32').height('32').class_name('rounded-circle border border-white')
                        ).class_name('me-auto'),
                        li(
                            Icon('geo-fill').class_name('bi me-2').width('1em').height('1em'),
                            small(location)
                        ).class_name('d-flex align-items-center me-3'),
                        li(
                            Icon('calendar3').class_name('bi me-2').width('1em').height('1em'),
                            small(date)
                        ).class_name('d-flex align-items-center'),
                    ).class_name('d-flex list-unstyled mt-auto')
                ).class_name('d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1')
            ).class_name('card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg').style('background-image: url({});'.format(bgImg))
        ).class_name('col')
    )
