import unittest
from os import path, remove
from typing import Dict
from pure.core.XML import XML
from pure.core.Raw import Raw


def address(*args):
    return XML("address", args)


def street(*args):
    return XML("street", args)


def city(*args):
    return XML("city", args)


def state(*args):
    return XML("state", args)


def zip(*args):
    return XML("zip", args)


def customers(*args):
    return XML("customers", args)


def customer(*args):
    return XML("customer", args)


def name(*args):
    return XML("name", args)


def Address(props: Dict[str, str]):
    street_val = props.get("street")
    city_val = props.get("city")
    state_val = props.get("state")
    zip_code = props.get("zip")

    return address(
        street(street_val) if (street_val) else None,
        city(city_val) if (city_val) else None,
        state(state_val) if (state_val) else None,
        zip(zip_code) if (zip_code) else None,
    )


class XMLTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__test_data = [
            {"street": "100 Main", "city": "Framingham", "state": "MA", "zip": "01701"},
            {
                "street": "720 Prospect",
                "city": "Framingham",
                "state": "MA",
                "zip": "01701",
            },
            {"street": "120 Ridge", "state": "MA", "zip": "01760"},
        ]
        self.__xml = self.__create_instance()

    def __create_instance(self):
        return customers(
            customer(name("Charter Group"), list(map(Address, self.__test_data))).id(
                "55000"
            )
        )

    def test_to_string(self):
        expected_str = '<customers><customer id="55000"><name>Charter Group</name><address><street>100 Main</street><city>Framingham</city><state>MA</state><zip>01701</zip></address><address><street>720 Prospect</street><city>Framingham</city><state>MA</state><zip>01701</zip></address><address><street>120 Ridge</street><state>MA</state><zip>01760</zip></address></customer></customers>'
        self.assertEqual(expected_str, str(self.__xml))

    def test_save(self):
        output_path = "./output.xml"
        self.__xml.save(output_path)

        with open(output_path, "r") as file:
            content = file.read()

        self.assertTrue(path.exists(output_path))
        excepted_str = '<?xml version="1.0"?><customers><customer id="55000"><name>Charter Group</name><address><street>100 Main</street><city>Framingham</city><state>MA</state><zip>01701</zip></address><address><street>720 Prospect</street><city>Framingham</city><state>MA</state><zip>01701</zip></address><address><street>120 Ridge</street><state>MA</state><zip>01760</zip></address></customer></customers>'
        self.assertEqual(excepted_str, content)
        remove(output_path)

    def test_magic_static_method(self):
        # Test magic static method approach
        xml = XML(
            "root",
            (
                XML("item", ("Content 1",)),
                XML("item", ("Content 2",)),
            ),
        )

        self.assertEqual("root", xml.get_tag_name())
        self.assertEqual(2, len(xml.get_children()))

    def test_constructor_method(self):
        # Test constructor approach
        xml = XML(
            "custom-root",
            (
                XML("custom-item", ("Custom Content 1",)),
                XML("custom-item", ("Custom Content 2",)),
            ),
        )

        self.assertEqual("custom-root", xml.get_tag_name())
        self.assertEqual(2, len(xml.get_children()))

    def test_string_children_are_escaped_not_filtered(self):
        # String children are text: XML-looking content is escaped, not
        # dropped. Use Raw.of() to emit trusted markup.
        xml = XML("root", ("<item>This stays visible</item>", "a<b"))

        self.assertEqual(
            "<root>&lt;item&gt;This stays visible&lt;/item&gt;a&lt;b</root>",
            str(xml),
        )

    def test_raw_preserves_content(self):
        # Test that Raw.of() preserves XML content
        xml = XML(
            "root",
            (
                Raw.of("<item>This should be preserved</item>"),
                Raw.of("<data>This too</data>"),
            ),
        )

        output = str(xml)

        self.assertIn("<item>This should be preserved</item>", output)
        self.assertIn("<data>This too</data>", output)

    def test_attribute_values_are_escaped(self):
        tag = XML("root").data('"><item>attack</item>')

        self.assertEqual(
            '<root data="&quot;&gt;&lt;item&gt;attack&lt;/item&gt;"></root>',
            str(tag),
        )


if __name__ == "__main__":
    unittest.main()
