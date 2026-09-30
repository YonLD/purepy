import os

from pure.loader import load_module

_COVER = os.path.join(
    os.path.dirname(__file__), '..', '..', 'views', 'cover.py'
)
cover_page = load_module(_COVER).cover_page


def cover_controller():
    return cover_page()
