from pure.html import div
from .Card import Card

def CardDeck(cards: list):
    return div(
        list(map(Card, cards))
    ).class_name('card-deck mb-3 text-center');
