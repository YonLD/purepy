import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

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
    if path in ('/', '/index.php'):
        return 302, REDIRECTS[path]
    if path == '/pure':
        return 200, index_controller()
    if path == '/plain':
        return 200, plain_index_controller()
    return 404, render_not_found(path)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else '/plain'
    status, body = route(path)
    print('Status: {}'.format(status))
    print('Content-Type: application/xml; charset=utf-8')
    print()
    print(body)


if __name__ == '__main__':
    main()
