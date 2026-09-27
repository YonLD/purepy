import os
from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import body, div, head, html, link, meta, title
from pure.utils import renderHTML

from pure.loader import load_module
PageHeader = load_module(os.path.join(os.path.dirname(__file__), 'PageHeader.cmp.py'), 'PageHeader').PageHeader
from pure.loader import load_module
PricingHeader = load_module(os.path.join(os.path.dirname(__file__), 'PricingHeader.cmp.py'), 'PricingHeader').PricingHeader
from pure.loader import load_module
CardDeck = load_module(os.path.join(os.path.dirname(__file__), 'CardDeck.cmp.py'), 'CardDeck').CardDeck
from pure.loader import load_module
PageFooter = load_module(os.path.join(os.path.dirname(__file__), 'PageFooter.cmp.py'), 'PageFooter').PageFooter
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.services import PricingService


def Pricing(*children):
    return component('Pricing', *children)


register(Pricing, factory=lambda: (
    html(
        head(
            meta().http_equiv('Content-Type').content('text/html; charset=UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1, shrink-to-fit=no'),
            meta().name('description').content(''),
            meta().name('author').content(''),
            link().rel('icon').href('https://getbootstrap.com/docs/4.0/assets/img/favicons/favicon.ico'),
            title('Pricing example for Bootstrap'),
            link().rel('canonical').href('https://getbootstrap.com/docs/4.0/examples/pricing/'),
            link().href('https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css').rel('stylesheet'),
            link().href('./pricing.css').rel('stylesheet')
        ),
        body(
            Slot.raw('header'),
            Slot.raw('pricing'),
            div(
                Slot.raw('deck'),
                Slot.raw('footer')
            ).class_name('container')
        )
    ).lang('en')
), prepare=lambda: pricing_bindings())


def pricing_bindings():
    return {
        'header': PageHeader(),
        'pricing': PricingHeader(),
        'deck': CardDeck(),
        'footer': PageFooter(),
    }


def pricing_page():
    return renderHTML(component('Pricing'))
