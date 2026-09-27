from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div, h1, p

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.services import PricingService


def PricingHeader(*children):
    return component('PricingHeader', *children)


register(PricingHeader, factory=lambda: (
    div(
        h1(Slot.value('title')).class_name('display-4'),
        p(Slot.value('desc')).class_name('lead')
    ).class_name('pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center')
), prepare=lambda: PricingService.pricing())
