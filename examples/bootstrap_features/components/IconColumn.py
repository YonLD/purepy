from typing import Dict
from pure.html import div, h3, p, a
from .Icon import Icon

def IconColumn(props: Dict[str, str]):
    icon = props['icon']
    title = props['title']
    content = props['content']
    linkText = props['linkText']
    link = props['link']

    return (
        div(
            div(
                Icon(icon).class_name('bi').width('1em').height('1em')
            ).class_name('feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3'),
            h3(title).class_name('fs-2'),
            p(content),
            a(
                linkText,
                Icon('chevron-right').class_name('bi').width('1em').height('1em'),
            ).href(link).class_name('icon-link d-inline-flex align-items-center')
        ).class_name('feature col')
    )
