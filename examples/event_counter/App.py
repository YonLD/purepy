from pure.html import div, h1, button, span

def App():
    return (
        div(
            h1('JavaScript Counter App'),
            div(
                button('+').id('add').onclick('handleAdd()'),
                span(0).id('output'),
                button('-').id('subtract'),
            ).class_name('counter-container')
        )
    )

