import os

from pure.html import a, body, code, h1, head, html, li, meta, p, title, ul
from pure.utils import renderHTML

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.controllers.CoverController import cover_controller
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.controllers.FeaturesController import features_controller
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.controllers.PlainFeaturesController import plain_features_controller
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.controllers.PlainPricingController import plain_pricing_controller
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.controllers.PricingController import pricing_controller

pages = {
    '/cover': 'the cover page: static markup, no compile step',
    '/pure/features': 'features: the page function and the component artifacts',
    '/plain/features': 'features: the plain view, components rendered up front',
    '/pure/pricing': 'pricing: the page function and the component artifacts',
    '/plain/pricing': 'pricing: the plain view, components rendered up front',
}


def render_not_found(path, pages):
    items = [
        li(a(route).href(route), ' — ', description)
        for route, description in pages.items()
    ]

    return 404, renderHTML(
        html(
            head(
                meta().charset('utf-8'),
                title('404 — nothing at ' + path)
            ),
            body(
                h1('404'),
                p('Nothing is routed at ', code(path), '. These routes exist:'),
                ul(*items)
            )
        ).lang('en')
    )


def index(path=None):
    if path is None:
        path = '/plain/features'

    file = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), path))

    if (
        file
        and os.path.isfile(file)
        and file != os.path.abspath(__file__)
        and file.startswith(os.path.dirname(os.path.abspath(__file__)) + os.sep)
    ):
        return 200, None

    routes = {
        '/cover': cover_controller,
        '/pure/features': features_controller,
        '/plain/features': plain_features_controller,
        '/pure/pricing': pricing_controller,
        '/plain/pricing': plain_pricing_controller,
    }

    handler = routes.get(path)
    if handler:
        return 200, handler()

    return render_not_found(path, pages)
