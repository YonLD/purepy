import os
from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div, h5, nav

from pure.loader import load_module
NavLink = load_module(os.path.join(os.path.dirname(__file__), '../components/NavLink.cmp.py'), 'NavLink').NavLink
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.services import PricingService


def PageHeader(*children):
    return component('PageHeader', *children)


register(PageHeader,
    factory=lambda: (
        div(
            h5(Slot.value('company')).class_name('my-0 mr-md-auto font-weight-normal'),
            nav(Slot.raw('navs')).class_name('my-2 my-md-0 mr-md-3'),
            Slot.raw('signUp')
        ).class_name('d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow')
    ),
    prepare=lambda: {
        'company': PricingService.header()['company'],
        'navs': [NavLink().props(nav) for nav in PricingService.header()['navs']],
        'signUp': NavLink().props(PricingService.header()['signUp']),
    }
)
