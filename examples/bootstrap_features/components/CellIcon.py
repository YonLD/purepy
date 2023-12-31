from typing import Dict
from pure.html import div, h3, p
from .Icon import Icon

def CellIcon(props: Dict[str, str]):
    icon = props['icon']
    title = props['title']
    content = props['content']

    return (
        div(
            Icon(icon).class_name('bi text-muted flex-shrink-0 me-3').width('1.75em').height('1.75em'),
            div(
                h3(title).class_name('fw-bold mb-0 fs-4'),
                p(content)
            )
        ).class_name('col d-flex align-items-start')
    )

