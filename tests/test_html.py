import unittest
from os import path, remove

from pure.core.HTML import HTML
from pure.raw import raw_html
from pure.html import (
    html,
    head,
    meta,
    title,
    body,
    div,
    header,
    h1,
    nav,
    ul,
    li,
    a,
    main,
    section,
    h2,
    p,
    form,
    label,
    input,
    textarea,
    footer,
    button,
    span,
)


class HTMLTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__html: HTML = self.__create_instance()

    def __create_instance(self):
        return html(
            head(meta().charset("UTF-8"), title("Complex HTML Code Example")),
            body(
                div(
                    header(
                        h1("Welcome to My Website"),
                        nav(
                            ul(
                                li(a("Home").href("#")),
                                li(a("About").href("#")),
                                li(a("Services").href("#")),
                                raw_html('<li><a href="#">Contact</a></li>'),
                            )
                        ).class_name("nav"),
                    ).class_name("header"),
                    main(
                        section(
                            h2("About Us"),
                            p(
                                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultrices urna eget sapien ullamcorper, vel efficitur massa semper."
                            ),
                            a("Learn More").href("#").class_name("button"),
                        ).class_name("section"),
                        section(
                            h2("Our Services"),
                            ul(li("Service 1"), li("Service 2"), li("Service 3")),
                        ).class_name("section"),
                        section(
                            h2("Contact Us"),
                            form(
                                label("Name:").class_name("form-label").htmlFor("name"),
                                input()
                                .type("text")
                                .id("name")
                                .name("name")
                                .class_name("form-input"),
                                label("Email:")
                                .class_name("form-label")
                                .htmlFor("email"),
                                input()
                                .type("email")
                                .id("email")
                                .name("email")
                                .class_name("form-input"),
                                label("Message:")
                                .class_name("form-label")
                                .htmlFor("message"),
                                textarea()
                                .id("message")
                                .name("message")
                                .class_name("form-input"),
                                button("Submit").type("submit").class_name("button"),
                            ),
                        ).class_name("section"),
                    ),
                    footer(
                        p("&copy; 2023 My Website. All rights reserved.")
                    ).class_name("footer"),
                ).class_name("container"),
            ),
        ).lang("en")

    def test_tag_name(self):
        self.assertEqual("html", html().get_tag_name())
        self.assertEqual("head", head().get_tag_name())
        self.assertEqual("body", body().get_tag_name())
        self.assertEqual("div", div().get_tag_name())
        self.assertEqual("title", title().get_tag_name())
        self.assertEqual("p", p().get_tag_name())
        self.assertEqual("a", a().get_tag_name())

    def test_attributes(self):
        tag = (
            input()
            .type("text")
            .id("my-input")
            .value(0)
            .disabled(False)
            .readonly(None)
            .required(True)
        )
        attributes = tag.get_attrs()

        self.assertEqual(4, len(attributes))
        self.assertNotIn("disabled", attributes)
        self.assertNotIn("readonly", attributes)
        self.assertEqual("text", tag.get_attr("type"))
        self.assertEqual("my-input", tag.get_attr("id"))
        self.assertEqual("0", tag.get_attr("value"))
        self.assertEqual("required", tag.get_attr("required"))

    def test_children(self):
        child1 = "Hello"
        child2 = span("World").style("color: red;")
        tag = div(child1, child2)
        children = tag.get_children()

        self.assertEqual(2, len(children))
        self.assertEqual(child1, children[0])
        self.assertEqual(child2, children[1])

    def test_to_JSON(self):
        excepted = {
            "tagName": "html",
            "attrs": {"lang": "en"},
            "children": [
                {
                    "tagName": "head",
                    "attrs": {},
                    "children": [
                        {
                            "tagName": "meta",
                            "attrs": {"charset": "UTF-8"},
                            "children": [],
                        },
                        {
                            "tagName": "title",
                            "attrs": {},
                            "children": ["Complex HTML Code Example"],
                        },
                    ],
                },
                {
                    "tagName": "body",
                    "attrs": {},
                    "children": [
                        {
                            "tagName": "div",
                            "attrs": {"class": "container"},
                            "children": [
                                {
                                    "tagName": "header",
                                    "attrs": {"class": "header"},
                                    "children": [
                                        {
                                            "tagName": "h1",
                                            "attrs": {},
                                            "children": ["Welcome to My Website"],
                                        },
                                        {
                                            "tagName": "nav",
                                            "attrs": {"class": "nav"},
                                            "children": [
                                                {
                                                    "tagName": "ul",
                                                    "attrs": {},
                                                    "children": [
                                                        {
                                                            "tagName": "li",
                                                            "attrs": {},
                                                            "children": [
                                                                {
                                                                    "tagName": "a",
                                                                    "attrs": {
                                                                        "href": "#"
                                                                    },
                                                                    "children": [
                                                                        "Home"
                                                                    ],
                                                                }
                                                            ],
                                                        },
                                                        {
                                                            "tagName": "li",
                                                            "attrs": {},
                                                            "children": [
                                                                {
                                                                    "tagName": "a",
                                                                    "attrs": {
                                                                        "href": "#"
                                                                    },
                                                                    "children": [
                                                                        "About"
                                                                    ],
                                                                }
                                                            ],
                                                        },
                                                        {
                                                            "tagName": "li",
                                                            "attrs": {},
                                                            "children": [
                                                                {
                                                                    "tagName": "a",
                                                                    "attrs": {
                                                                        "href": "#"
                                                                    },
                                                                    "children": [
                                                                        "Services"
                                                                    ],
                                                                }
                                                            ],
                                                        },
                                                        '<li><a href="#">Contact</a></li>',
                                                    ],
                                                }
                                            ],
                                        },
                                    ],
                                },
                                {
                                    "tagName": "main",
                                    "attrs": {},
                                    "children": [
                                        {
                                            "tagName": "section",
                                            "attrs": {"class": "section"},
                                            "children": [
                                                {
                                                    "tagName": "h2",
                                                    "attrs": {},
                                                    "children": ["About Us"],
                                                },
                                                {
                                                    "tagName": "p",
                                                    "attrs": {},
                                                    "children": [
                                                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultrices urna eget sapien ullamcorper, vel efficitur massa semper."
                                                    ],
                                                },
                                                {
                                                    "tagName": "a",
                                                    "attrs": {
                                                        "href": "#",
                                                        "class": "button",
                                                    },
                                                    "children": ["Learn More"],
                                                },
                                            ],
                                        },
                                        {
                                            "tagName": "section",
                                            "attrs": {"class": "section"},
                                            "children": [
                                                {
                                                    "tagName": "h2",
                                                    "attrs": {},
                                                    "children": ["Our Services"],
                                                },
                                                {
                                                    "tagName": "ul",
                                                    "attrs": {},
                                                    "children": [
                                                        {
                                                            "tagName": "li",
                                                            "attrs": {},
                                                            "children": ["Service 1"],
                                                        },
                                                        {
                                                            "tagName": "li",
                                                            "attrs": {},
                                                            "children": ["Service 2"],
                                                        },
                                                        {
                                                            "tagName": "li",
                                                            "attrs": {},
                                                            "children": ["Service 3"],
                                                        },
                                                    ],
                                                },
                                            ],
                                        },
                                        {
                                            "tagName": "section",
                                            "attrs": {"class": "section"},
                                            "children": [
                                                {
                                                    "tagName": "h2",
                                                    "attrs": {},
                                                    "children": ["Contact Us"],
                                                },
                                                {
                                                    "tagName": "form",
                                                    "attrs": {},
                                                    "children": [
                                                        {
                                                            "tagName": "label",
                                                            "attrs": {
                                                                "class": "form-label",
                                                                "for": "name",
                                                            },
                                                            "children": ["Name:"],
                                                        },
                                                        {
                                                            "tagName": "input",
                                                            "attrs": {
                                                                "type": "text",
                                                                "id": "name",
                                                                "name": "name",
                                                                "class": "form-input",
                                                            },
                                                            "children": [],
                                                        },
                                                        {
                                                            "tagName": "label",
                                                            "attrs": {
                                                                "class": "form-label",
                                                                "for": "email",
                                                            },
                                                            "children": ["Email:"],
                                                        },
                                                        {
                                                            "tagName": "input",
                                                            "attrs": {
                                                                "type": "email",
                                                                "id": "email",
                                                                "name": "email",
                                                                "class": "form-input",
                                                            },
                                                            "children": [],
                                                        },
                                                        {
                                                            "tagName": "label",
                                                            "attrs": {
                                                                "class": "form-label",
                                                                "for": "message",
                                                            },
                                                            "children": ["Message:"],
                                                        },
                                                        {
                                                            "tagName": "textarea",
                                                            "attrs": {
                                                                "id": "message",
                                                                "name": "message",
                                                                "class": "form-input",
                                                            },
                                                            "children": [],
                                                        },
                                                        {
                                                            "tagName": "button",
                                                            "attrs": {
                                                                "type": "submit",
                                                                "class": "button",
                                                            },
                                                            "children": ["Submit"],
                                                        },
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                },
                                {
                                    "tagName": "footer",
                                    "attrs": {"class": "footer"},
                                    "children": [
                                        {
                                            "tagName": "p",
                                            "attrs": {},
                                            "children": [
                                                "&copy; 2023 My Website. All rights reserved."
                                            ],
                                        }
                                    ],
                                },
                            ],
                        }
                    ],
                },
            ],
        }

        self.assertEqual(excepted, self.__html.to_JSON())

    def test_to_string(self):
        excepted_str = '<html lang="en"><head><meta charset="UTF-8" /><title>Complex HTML Code Example</title></head><body><div class="container"><header class="header"><h1>Welcome to My Website</h1><nav class="nav"><ul><li><a href="#">Home</a></li><li><a href="#">About</a></li><li><a href="#">Services</a></li><li><a href="#">Contact</a></li></ul></nav></header><main><section class="section"><h2>About Us</h2><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultrices urna eget sapien ullamcorper, vel efficitur massa semper.</p><a href="#" class="button">Learn More</a></section><section class="section"><h2>Our Services</h2><ul><li>Service 1</li><li>Service 2</li><li>Service 3</li></ul></section><section class="section"><h2>Contact Us</h2><form><label class="form-label" for="name">Name:</label><input type="text" id="name" name="name" class="form-input" /><label class="form-label" for="email">Email:</label><input type="email" id="email" name="email" class="form-input" /><label class="form-label" for="message">Message:</label><textarea id="message" name="message" class="form-input"></textarea><button type="submit" class="button">Submit</button></form></section></main><footer class="footer"><p>&copy; 2023 My Website. All rights reserved.</p></footer></div></body></html>'
        self.assertEqual(excepted_str, str(self.__html))

    def test_save(self):
        output_path = "./output.html"
        tag = div("Hello, World!")
        tag.save(output_path)

        with open(output_path, "r") as file:
            content = file.read()

        self.assertTrue(path.exists(output_path))
        self.assertEqual("<!DOCTYPE html><div>Hello, World!</div>", content)
        remove(output_path)

    def test_magic_static_method(self):
        tag = div("Hello World")

        self.assertEqual("div", tag.get_tag_name())
        self.assertEqual(["Hello World"], tag.get_children())

    def test_constructor_method(self):
        tag = HTML("custom-tag", ["Custom Content"])

        self.assertEqual("custom-tag", tag.get_tag_name())
        self.assertEqual(["Custom Content"], tag.get_children())

    def test_void_elements_reject_children(self):
        with self.assertRaises(Exception) as ctx:
            input("child")

        self.assertEqual(
            "Self-closing element 'input' cannot have child elements.",
            str(ctx.exception),
        )

    def test_string_children_are_escaped_not_filtered(self):
        # String children are text: markup-looking content is escaped so no
        # data is lost. Use Raw.of() to emit trusted markup.
        tag = div("<p>This stays visible</p>", "<strong>This too</strong>", "a<b")

        self.assertEqual(
            "<div>&lt;p&gt;This stays visible&lt;/p&gt;&lt;strong&gt;This too&lt;/strong&gt;a&lt;b</div>",
            str(tag),
        )

    def test_raw_preserves_content(self):
        tag = div(
            raw_html("<p>This should be preserved</p>"),
            raw_html("<strong>This too</strong>"),
        )

        output = str(tag)

        self.assertIn("<p>This should be preserved</p>", output)
        self.assertIn("<strong>This too</strong>", output)

    def test_class_name(self):
        # purephp writes this as one mixed array ([0 => 'class-d', 'class-e' => true,
        # ...]); Python has no mixed array, so the entries are passed as separate
        # arguments, which clx() joins the same way.
        tag = div().className(
            "class-a class-b",
            "class-c",
            "class-d",
            {
                "class-e": True,
                "class-f": False,
                "class-g": None,
                "class-h": 0,
                "class-i": "",
                "class-j": "not empty string",
            },
            None,
            "",
        )

        self.assertEqual(
            "class-a class-b class-c class-d class-e class-j", tag.get_attr("class")
        )

    def test_style(self):
        tag = div().style(
            {
                "color": False,
                "background-color": "#fff",
                "line-height": 1.5,
                "font-size": "20px",
                "position": None,
            }
        )

        self.assertEqual(
            "background-color: #fff; line-height: 1.5; font-size: 20px;",
            tag.get_attr("style"),
        )

    def test_attribute_values_are_escaped(self):
        tag = input().type("text").value('"><script>alert(1)</script>')

        self.assertEqual(
            '<input type="text" value="&quot;&gt;&lt;script&gt;alert(1)&lt;/script&gt;" />',
            str(tag),
        )

    def test_save(self):
        output_path = "./output.html"
        tag = div("Hello, World!")

        tag.save(output_path)

        with open(output_path, "r") as file:
            content = file.read()

        self.assertTrue(path.exists(output_path))
        self.assertEqual("<!DOCTYPE html><div>Hello, World!</div>", content)
        remove(output_path)


if __name__ == "__main__":
    unittest.main()
