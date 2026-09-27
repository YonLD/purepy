import os
from pure.loader import load_module
pricing_page = load_module(os.path.join(os.path.dirname(__file__), '../../views/pricing_cmp.cmp.py'), 'pricing_cmp').pricing_page


def pricing_controller():
    return pricing_page()
