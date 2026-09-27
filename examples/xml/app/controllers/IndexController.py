import os

from .XmlData import xml_data
from pure.loader import load_module

_XML = os.path.join(os.path.dirname(__file__), '..', '..', 'views', 'xml.cmp.py')
xml_page = load_module(_XML).xml_page


def index_controller():
    return xml_page(xml_data())
