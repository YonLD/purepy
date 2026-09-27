import os
from ..bootstrap import plain
from pure.loader import load_module
features_bindings = load_module(os.path.join(os.path.dirname(__file__), '../../views/features_cmp.cmp.py'), 'features_cmp').features_bindings


def plain_features_controller():
    return plain('features', features_bindings())
