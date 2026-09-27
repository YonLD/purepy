import os
import unittest

from pure.clx import clx
from pure.compile.Compile import Compile
from pure.component.Registry import Registry
from pure.component.functions import component
from pure.core.XML import XML
from pure.html import body, div, html
from pure.sty import sty
from pure.utils import renderHTML, renderXML


class UtilsTest(unittest.TestCase):
    __file = os.path.abspath(__file__)

    def test_clx(self):
        self.assertEqual(
            "class-a class-b class-c class-d",
            clx(
                "class-a",
                "class-b",
                {"class-c": True, "class-d": True, "class-e": False},
            ),
        )

        self.assertEqual(
            "class-a class-b class-c",
            clx(
                None,
                "",
                ["class-a", "class-b"],
                {
                    "class-c": True,
                },
            ),
        )

    def test_sty(self):
        self.assertEqual(
            "background-color: red; height: 36px; border: 1px solid #fff;",
            sty(
                {
                    "background-color": "red",
                    "height": "36px",
                    "border": "1px solid #fff",
                }
            ),
        )

    def test_clx_drops_booleans_and_keeps_explicit_string_zero(self):
        # Deliberately not a literal so static analysis cannot narrow the branch.
        flag = os.environ.get("PUREPY_TEST_FLAG") is not None

        self.assertEqual("btn", clx("btn", "active" if flag else False))
        self.assertEqual("btn active", clx("btn", "active"))
        self.assertIsNone(clx(False))
        self.assertIsNone(clx(True))
        self.assertEqual("0", clx("0"))
        self.assertEqual("0", clx(["0"]))

    def test_clx_drops_non_string_array_entries(self):
        # List entries: only non-empty strings and numbers survive.
        self.assertIsNone(clx([True, None, ["nested"], ""]))
        self.assertEqual("1 2.5", clx([1, 2.5]))
        self.assertEqual("0", clx([0]))
        self.assertEqual("0", clx([0.0]))
        self.assertEqual("zero 5", clx(["zero", 5]))

        # Map entries: the key survives only for truthy, non-empty-string values,
        # and a numeric-string key has already become an int key.
        self.assertIsNone(
            clx(
                {
                    "zero": 0,
                    "strict-zero": "0",
                    "empty": "",
                    "false": False,
                    "none": None,
                }
            )
        )
        self.assertIsNone(clx({"0": True}))
        self.assertEqual("a b", clx({"a": "yes", "b": 1}))

    def test_render_html_prepends_the_doctype(self):
        self.assertEqual(
            '<!DOCTYPE html><html lang="en"><body><div>Hello</div></body></html>',
            renderHTML(html(body(div("Hello"))).lang("en")),
        )

    def test_render_html_keeps_fragments_intact_behind_the_header(self):
        self.assertEqual("<!DOCTYPE html><div>&lt;b&gt;</div>", renderHTML(div("<b>")))

    def test_render_html_renders_component_calls(self):
        def factory():
            return Compile.shape(html(body(div("Hi"))))

        Registry.register("UtilsPage", self.__file, factory)

        self.assertEqual(
            "<!DOCTYPE html><html><body><div>Hi</div></body></html>",
            renderHTML(component("UtilsPage")),
        )

    def test_render_xml_prepends_the_declaration(self):
        self.assertEqual(
            '<?xml version="1.0"?><customers><customer id="55000">'
            "<name>Charter Group</name></customer></customers>",
            renderXML(
                XML(
                    "customers",
                    XML("customer", XML("name", "Charter Group")).id("55000"),
                )
            ),
        )

    def test_render_xml_renders_component_calls(self):
        def factory():
            return Compile.shape(XML("customers", XML("name", "Charter Group")))

        Registry.register("UtilsXml", self.__file, factory)

        self.assertEqual(
            '<?xml version="1.0"?><customers><name>Charter Group</name></customers>',
            renderXML(component("UtilsXml")),
        )


if __name__ == "__main__":
    unittest.main()
