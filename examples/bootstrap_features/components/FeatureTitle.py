from typing import Dict
from pure.html import div, h4, p
from .Icon import Icon

def FeatureTitle(props: Dict[str, str]):
    icon = props['icon']
    title = props['title']
    content = props['content']

    return (
        div(
            div(
                Icon(icon).class_name('bi').width('1em').height('1em')
            ).class_name('feature-icon-small d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-4 rounded-3'),
            h4(title).class_name('fw-semibold mb-0'),
            p(content).class_name('text-muted')
        ).class_name('col d-flex flex-column gap-2')
    )
