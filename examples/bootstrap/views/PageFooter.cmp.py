import os
from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div, footer

from pure.loader import load_module
ColLogo = load_module(os.path.join(os.path.dirname(__file__), '../components/ColLogo.cmp.py'), 'ColLogo').ColLogo
from pure.loader import load_module
ColLinks = load_module(os.path.join(os.path.dirname(__file__), '../components/ColLinks.cmp.py'), 'ColLinks').ColLinks
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.services import PricingService


def PageFooter(*children):
    return component('PageFooter', *children)


register(PageFooter,
    factory=lambda: (
        footer(
            div(
                Slot.raw('logo'),
                Slot.raw('columns')
            ).class_name('row'),
        ).class_name('pt-4 my-md-5 pt-md-5 border-top')
    ),
    prepare=lambda: {
        'logo': ColLogo().props(PricingService.footer()['logo']),
        'columns': [
            ColLinks().title(column['title']).links(column['links'])
            for column in PricingService.footer()['columns']
        ],
    }
)
