import os
from ..bootstrap import plain
from pure.loader import load_module
pricing_bindings = load_module(os.path.join(os.path.dirname(__file__), '../../views/pricing.cmp.py'), 'pricing').pricing_bindings


def plain_pricing_controller():
    return plain('pricing', pricing_bindings())
