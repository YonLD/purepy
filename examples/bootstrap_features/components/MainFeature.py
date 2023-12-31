from pure.html import div, h3, p, a

def MainFeature(title: str, content: str, linkText: str, link: str):
    return (
        div(
            h3(title).class_name('fw-bold'),
            p(content).class_name('text-muted'),
            a(linkText).class_name('btn btn-primary btn-lg').href(link)
        ).class_name('col d-flex flex-column align-items-start gap-2')
    )
