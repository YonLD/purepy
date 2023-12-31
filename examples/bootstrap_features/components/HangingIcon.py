from typing import Dict
from pure.html import div, h3, p, a
from .Icon import Icon

def HangingIcon(props: Dict[str, str]):
    icon = props['icon']
    title = props['title']
    content = props['content']
    linkText = props['linkText']
    link = props['link']

    return (
        div(
            div(
                Icon(icon).class_name('bi').width('1em').height('1em')
            ).class_name('icon-square text-bg-light d-inline-flex align-items-center justify-content-center fs-4 flex-shrink-0 me-3'),
            div(
                h3(title).class_name('fs-2'),
                p(content),
                a(linkText).href(link).class_name('btn btn-primary')
            )
        ).class_name('col d-flex align-items-start')
    )

