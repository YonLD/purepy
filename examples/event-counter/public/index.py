"""Front controller and router of the counter example — one entry, two routes:

    /pure    the page function and the artifact
    /plain   the plain view, no library in the view file

A request that matches nothing gets a 404 that lists these routes; `/` and
`/index.py` redirect to `/plain`. Static files (style.css, script.js) are handed
back to the server. Run it with:

    # HTTP
    python3 examples/event-counter/public/index.py --serve
    # one page on stdout
    python3 examples/event-counter/public/index.py /pure
"""

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))

# The example is self-contained: its controllers sit beside this entry.
sys.path.insert(0, os.path.join(_ROOT, '..', 'app', 'controllers'))

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

ROUTES = {
    '/pure': index_controller,
    '/plain': plain_index_controller,
}


def render_not_found(path, pages, redirects):
    """The 404 page: it reports the request and lists every route that exists,
    so it doubles as a map of the example.
    """
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


def index(path=None):
    """Resolve a request path to (status, body, location).

    A body of None means the path names a static file, which the caller hands
    back to the server rather than rendering.
    """
    if path is None:
        path = '/plain'

    file = os.path.realpath(os.path.join(_ROOT, path.lstrip('/')))

    if (
        os.path.isfile(file)
        and file != os.path.abspath(__file__)
        and file.startswith(_ROOT + os.sep)
    ):
        return 200, None, None

    if path in redirects:
        return 302, None, redirects[path]

    handler = ROUTES.get(path)

    if handler:
        return 200, handler(), None

    return 404, render_not_found(path, pages, redirects), None


def serve(port=8000, host=''):
    """Serve this directory over HTTP, the way `php -S` serves index.php."""
    from http.server import SimpleHTTPRequestHandler, HTTPServer

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=_ROOT, **kwargs)

        def do_GET(self):
            path = self.path.split('?')[0] or '/'
            status, body, location = index(path)

            if body is None:
                if location is None:
                    super().do_GET()
                    return

                self.send_response(302)
                self.send_header('Location', location)
                self.end_headers()
                return

            self.send_response(status)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body.encode())))
            self.end_headers()
            self.wfile.write(body.encode())

    httpd = HTTPServer((host, port), Handler)
    print('Serving examples/event-counter on http://localhost:{}/'.format(port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


def main():
    argv = sys.argv[1:]

    if argv and argv[0] in ('-h', '--help'):
        print(__doc__.strip())
        return 0

    if argv and argv[0] == '--serve':
        serve(int(argv[1]) if len(argv) > 1 else 8000)
        return 0

    # A CLI run with no path renders the plain view, as purephp's front
    # controller does with no REQUEST_URI.
    status, body, location = index(argv[0] if argv else None)

    if location is not None:
        print('Status: 302 Found')
        print('Location: {}'.format(location))
        return 0

    print('Status: {}'.format(status))
    print('Content-Type: text/html; charset=utf-8')
    print()
    print(body)

    return 0


if __name__ == '__main__':
    sys.exit(main())
