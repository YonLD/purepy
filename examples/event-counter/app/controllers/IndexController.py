import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'views'))

from bootstrap import plain
from CounterData import counter_data
from counter.cmp import counter_page


def index_controller():
    return counter_page(counter_data())
