from pure.html import div, h5, ul, li, a

def ColLinks(props: dict):
    title = props['title']
    links = props['links']

    return div(
        h5(title),
        ul(
            list(map(lambda link: li(a(link['text']).class_name('text-muted').href(link['href'])), links))
        ).class_name('list-unstyled text-small')
    ).class_name('col-6 col-md');
