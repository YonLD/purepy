import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app', 'controllers'))

from IndexController import index_controller
from PlainIndexController import plain_index_controller
from pure.html import a, body, code, h1, head, html, li, meta, p, title, ul
from pure.utils import renderHTML

pages = {
    '/pure': 'the page function and the artifact',
    '/plain': 'the plain view, no library in the view file',
}

redirects = {
    '/': '/plain',
    '/index.php': '/plain',
}


def render_not_found(path, pages, redirects):
    items = []

    for route, description in pages.items():
        items.append(li(a(route).href(route), ' — ', description))

    for route, target in redirects.items():
        items.append(li(a(route).href(route), ' — redirects to ', code(target)))

    return renderHTML(html(
        head(
            meta().charset('utf-8'),
            title('404 — nothing at ' + path)
        ),
        body(
            h1('404'),
            p('Nothing is routed at ', code(path), '. These routes exist:'),
            ul(*items)
        )
    ).lang('en'))


def main():
    uri = os.environ.get('REQUEST_URI', '/plain')
    path = uri.split('?')[0] if '?' in uri else uri
    if not path:
        path = '/'

    if path in ('/', '/index.php'):
        print('Status: 302 Found')
        print('Location: /plain')
        print()
        return

    if path == '/pure':
        print('Content-Type: text/html; charset=utf-8')
        print()
        print(index_controller())
        return

    if path == '/plain':
        print('Content-Type: text/html; charset=utf-8')
        print()
        print(plain_index_controller())
        return

    print('Status: 404 Not Found')
    print('Content-Type: text/html; charset=utf-8')
    print()
    print(render_not_found(path, pages, redirects))


if __name__ == '__main__':
    main()
