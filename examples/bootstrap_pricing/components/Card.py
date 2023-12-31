from pure.html import div, h4, h1, ul, li, button, small

def Card(props: dict):
    type = props['type']
    price = props['price']
    features = props['features']
    btn = props['btn']

    return div(
        div(
            h4(
                type
            ).class_name('my-0 font-weight-normal')
        ).class_name('card-header'),
        div(
            h1(
                '${} '.format(price),
                small('/ mo').class_name('text-muted')
            ).class_name('card-title pricing-card-title'),
            ul(
                list(map(li, features))
            ).class_name('list-unstyled mt-3 mb-4'),
            button(btn['text']).type('button').class_name('btn btn-lg btn-block {}'.format(btn['class']))
        ).class_name('card-body')
    ).class_name('card mb-4 box-shadow');
