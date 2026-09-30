"""Front controller and router of the XML example — one entry, two routes:

    /pure    the page function and the artifact
    /plain   the plain view, no library in the view file

`/` and `/index.py` redirect to `/plain`; anything else gets a 404 that lists
the routes as an XML document. Run it with:

    # HTTP
    python3 examples/xml/public/index.py --serve
    # one document on stdout
    python3 examples/xml/public/index.py /pure
"""

import os
import sys

# The example is self-contained: its controllers import `app.*` relative to the
# example root, so that root goes on the path before anything is imported.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pure.core.XML import XML
from pure.utils import renderXML

from app.controllers.IndexController import index_controller
from app.controllers.PlainIndexController import plain_index_controller

PAGES = {
    '/pure': 'the page function and the artifact',
    '/plain': 'the plain view, no library in the view file',
}

REDIRECTS = {
    '/': '/plain',
    '/index.php': '/plain',
}


def _route_element(description=None, path=None, redirects_to=None):
    children = [description] if description else []
    elem = XML('route', children)
    if path is not None:
        elem.path(path)
    if redirects_to is not None:
        elem.redirects_to(redirects_to)
    return elem


def render_not_found(path):
    routes = []
    for route, description in PAGES.items():
        routes.append(_route_element(description=description, path=route))
    for route, target in REDIRECTS.items():
        routes.append(_route_element(path=route, redirects_to=target))
    return renderXML(XML('routes', [XML('request', (path,))] + routes))


def route(path):
    """Resolve a request path to (status, body, location).

    A body of None means the path names a static file, which the caller hands
    back to the server rather than rendering.
    """
    _ROOT = os.path.dirname(os.path.abspath(__file__))
    file = os.path.realpath(os.path.join(_ROOT, path.lstrip('/')))

    if (
        os.path.isfile(file)
        and file != os.path.abspath(__file__)
        and file.startswith(_ROOT + os.sep)
    ):
        return 200, None, None

    if path in REDIRECTS:
        return 302, None, REDIRECTS[path]

    if path == '/pure':
        return 200, index_controller(), None

    if path == '/plain':
        return 200, plain_index_controller(), None

    return 404, render_not_found(path), None


def serve(port=8000, host=''):
    """Serve this directory over HTTP, the way `php -S` serves index.php."""
    from http.server import SimpleHTTPRequestHandler, HTTPServer

    _ROOT = os.path.dirname(os.path.abspath(__file__))

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=_ROOT, **kwargs)

        def do_GET(self):
            path = self.path.split('?')[0] or '/'
            status, body, location = route(path)

            if body is None:
                if location is None:
                    super().do_GET()
                    return

                self.send_response(302)
                self.send_header('Location', location)
                self.end_headers()
                return

            self.send_response(status)
            self.send_header('Content-Type', 'application/xml; charset=utf-8')
            self.send_header('Content-Length', str(len(body.encode())))
            self.end_headers()
            self.wfile.write(body.encode())

    httpd = HTTPServer((host, port), Handler)
    print('Serving examples/xml on http://localhost:{}/'.format(port))

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

    path = argv[0] if argv else '/plain'
    status, body, location = route(path)

    if location is not None:
        print('Status: 302 Found')
        print('Location: {}'.format(location))
        return 0

    print('Status: {}'.format(status))
    print('Content-Type: application/xml; charset=utf-8')
    print()
    print(body)

    return 0


if __name__ == '__main__':
    sys.exit(main())
