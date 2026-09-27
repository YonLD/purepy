import os
from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div

from pure.loader import load_module
Card = load_module(os.path.join(os.path.dirname(__file__), '../components/Card.cmp.py'), 'Card').Card
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.services import PricingService


def CardDeck(*children):
    return component('CardDeck', *children)


register(CardDeck,
    factory=lambda: (
        div(Slot.raw('cards')).class_name('card-deck mb-3 text-center')
    ),
    prepare=lambda: {
        'cards': [
            Card()
                .type(card['type'])
                .price(card['price'])
                .features([feature['value'] for feature in card['features']])
                .text(card['text'])
                .class_name(card['class'])
            for card in PricingService.deck()
        ],
    }
)
