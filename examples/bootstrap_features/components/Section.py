from pure.html import div, h2

def Section(title: str, contents: list, classList: str):
    return (
        div(
            h2(title).class_name('pb-2 border-bottom'),
            div(contents).class_name(classList)
        ).class_name('container px-4 py-5')
    )
