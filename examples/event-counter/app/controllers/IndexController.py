import os
import sys

_APP = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_VIEWS = os.path.join(_APP, '..', 'views')

# The controllers are imported as top-level modules by public/index.py, so the
# app directory goes on the path for `bootstrap` and `CounterData`.
sys.path.insert(0, _APP)

from pure.loader import load_module

from CounterData import counter_data

# The unit file is named `counter.cmp.py`, which is not a module name, so it is
# loaded by path the way purephp requires it.
counter_page = load_module(
    os.path.join(_VIEWS, 'counter.cmp.py'), 'counter'
).counter_page


def index_controller():
    return counter_page(counter_data())
