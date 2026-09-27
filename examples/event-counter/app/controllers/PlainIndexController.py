import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bootstrap import plain
from CounterData import counter_data


def plain_index_controller():
    data = counter_data()
    return plain('counter', {'initial': data['initial']})
