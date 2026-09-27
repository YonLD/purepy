import os
from ..bootstrap import plain
from pure.loader import load_module
pricing_bindings = load_module(os.path.join(os.path.dirname(__file__), '../../views/pricing_cmp.cmp.py'), 'pricing_cmp').pricing_bindings


def plain_pricing_controller():
    return plain('pricing', pricing_bindings())
