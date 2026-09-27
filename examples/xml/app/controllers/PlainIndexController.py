from .XmlData import xml_data
from ..bootstrap import plain


def plain_index_controller():
    data = xml_data()
    return plain('xml', {'addresses': data['addresses']})
