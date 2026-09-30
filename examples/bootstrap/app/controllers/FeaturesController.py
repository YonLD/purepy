import os
from pure.loader import load_module
features_page = load_module(os.path.join(os.path.dirname(__file__), '../../views/features.cmp.py'), 'features').features_page


def features_controller():
    return features_page()
