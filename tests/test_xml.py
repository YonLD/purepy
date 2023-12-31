import unittest
from os import path, remove
from typing import Dict
from pure.core.XML import XML

def address(*args):
    tag = XML('address')
    return tag(*args)

def street(*args):
    tag = XML('street')
    return tag(*args)

def city(*args):
    tag = XML('city')
    return tag(*args)

def state(*args):
    tag = XML('state')
    return tag(*args)

def zip(*args):
    tag = XML('zip')
    return tag(*args)

def customers(*args):
    tag = XML('customers')
    return tag(*args)

def customer(*args):
    tag = XML('customer')
    return tag(*args)

def name(*args):
    tag = XML('name')
    return tag(*args)

def Address(props: Dict[str, str]):
    street_val = props.get('street')
    city_val = props.get('city')
    state_val = props.get('state')
    zip_code = props.get('zip')

    return address(
        street(street_val) if (street_val) else None,
        city(city_val) if (city_val) else None,
        state(state_val) if (state_val) else None,
        zip(zip_code) if (zip_code) else None
    )

class XMLTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__test_data = [
            {
                'street': '100 Main',
                'city': 'Framingham',
                'state': 'MA',
                'zip': '01701'
            },
            {
                'street': '720 Prospect',
                'city': 'Framingham',
                'state': 'MA',
                'zip': '01701'
            },
            {
                'street': '120 Ridge',
                'state': 'MA',
                'zip': '01760'
            }
        ]
        self.__xml = self.__create_instance()

    def __create_instance(self):
        return customers(
            customer(
                name('Charter Group'),
                list(map(Address, self.__test_data))
            ).id('55000')
        )

    def test_to_string(self):
        expected_str = '<customers><customer id="55000"><name>Charter Group</name><address><street>100 Main</street><city>Framingham</city><state>MA</state><zip>01701</zip></address><address><street>720 Prospect</street><city>Framingham</city><state>MA</state><zip>01701</zip></address><address><street>120 Ridge</street><state>MA</state><zip>01760</zip></address></customer></customers>';
        self.assertEqual(expected_str, str(self.__xml))

    def test_save(self):
        output_path = './output.xml'
        self.__xml.to_save(output_path)

        with open(output_path, 'r') as file:
            content = file.read()

        self.assertTrue(path.exists(output_path))
        excepted_str = '<?xml version="1.0"?><customers><customer id="55000"><name>Charter Group</name><address><street>100 Main</street><city>Framingham</city><state>MA</state><zip>01701</zip></address><address><street>720 Prospect</street><city>Framingham</city><state>MA</state><zip>01701</zip></address><address><street>120 Ridge</street><state>MA</state><zip>01760</zip></address></customer></customers>';
        self.assertEqual(excepted_str, content)
        remove(output_path)
