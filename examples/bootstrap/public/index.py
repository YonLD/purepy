"""Front controller and router of the bootstrap example — one entry, five routes:

    /cover             the cover page (static markup, no compile step)
    /pure/features     the features page function and component artifacts
    /plain/features    the features plain view, components rendered up front
    /pure/pricing      the pricing page function and the component artifacts
    /plain/pricing     the pricing plain view, components rendered up front

A request that matches nothing gets a 404 that lists these routes. Static files
(style.css, pricing.css) are handed back to the server. Run it with:

    # HTTP, the way `php -S localhost:8000 -t examples/bootstrap/public ...` runs
    python3 examples/bootstrap/public/index.py --serve
    # one page on stdout
    python3 examples/bootstrap/public/index.py /cover
"""

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))

# The example is self-contained: its controllers import `app.*` relative to the
# example root, so that root goes on the path before anything is imported.
sys.path.insert(0, os.path.abspath(os.path.join(_ROOT, '..')))

from pure.html import a, body, code, h1, head, html, li, meta, p, title, ul
from pure.utils import renderHTML

from app.controllers.CoverController import cover_controller
from app.controllers.FeaturesController import features_controller
from app.controllers.PlainFeaturesController import plain_features_controller
from app.controllers.PlainPricingController import plain_pricing_controller
from app.controllers.PricingController import pricing_controller

# The routes of this router, for the 404 map below.
pages = {
    '/cover': 'the cover page: static markup, no compile step',
    '/pure/features': 'features: the page function and the component artifacts',
    '/plain/features': 'features: the plain view, components rendered up front',
    '/pure/pricing': 'pricing: the page function and the component artifacts',
    '/plain/pricing': 'pricing: the plain view, components rendered up front',
}

ROUTES = {
    '/cover': cover_controller,
    '/pure/features': features_controller,
    '/plain/features': plain_features_controller,
    '/pure/pricing': pricing_controller,
    '/plain/pricing': plain_pricing_controller,
}


def render_not_found(path, pages):
    """The 404 page: it reports the request and lists every route that exists,
    so it doubles as a map of the example. It is built with the HTML functions of
    this library, which escape the requested path and the route descriptions.
    """
    items = [
        li(a(route).href(route), ' — ', description)
        for route, description in pages.items()
    ]

    return 404, renderHTML(html(
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
    """Resolve a request path to (status, body).

    A body of None means the path names a static file, which the caller hands
    back to the server rather than rendering.
    """
    if path is None:
        path = '/plain/features'

    # A request path starts with a slash, which os.path.join would read as an
    # absolute path and drop this directory from, so the separator is stripped.
    file = os.path.realpath(os.path.join(_ROOT, path.lstrip('/')))

    if (
        os.path.isfile(file)
        and file != os.path.abspath(__file__)
        and file.startswith(_ROOT + os.sep)
    ):
        return 200, None

    handler = ROUTES.get(path)

    if handler:
        return 200, handler()

    return render_not_found(path, pages)


def serve(port=8000, host=''):
    """Serve this directory over HTTP, the way `php -S` serves index.php."""
    from http.server import SimpleHTTPRequestHandler, HTTPServer

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=_ROOT, **kwargs)

        def do_GET(self):
            path = self.path.split('?')[0] or '/'
            status, body = index(path)

            # An existing file is the server's own business, like the
            # cli-server branch of purephp's front controller.
            if body is None:
                super().do_GET()
                return

            self.send_response(status)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body.encode())))
            self.end_headers()
            self.wfile.write(body.encode())

    httpd = HTTPServer((host, port), Handler)
    print('Serving examples/bootstrap on http://localhost:{}/'.format(port))

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
        port = int(argv[1]) if len(argv) > 1 else 8000
        serve(port)
        return 0

    # A CLI run with no path renders the plain features view, as purephp's
    # front controller does with no REQUEST_URI.
    status, body = index(argv[0] if argv else None)

    print('Status: {}'.format(status))
    print('Content-Type: text/html; charset=utf-8')
    print()
    print(body)

    return 0


if __name__ == '__main__':
    sys.exit(main())
