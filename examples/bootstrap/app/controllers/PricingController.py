import os
from pure.loader import load_module
pricing_page = load_module(os.path.join(os.path.dirname(__file__), '../../views/pricing.cmp.py'), 'pricing').pricing_page


def pricing_controller():
    return pricing_page()
