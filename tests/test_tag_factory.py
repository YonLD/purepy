import importlib
import inspect

import pytest

from pure.core.HTML import HTML
from pure.core.SVG import SVG
from pure.core.XML import XML

HTML_FUNCTIONS = [
    "a",
    "abbr",
    "address",
    "area",
    "article",
    "aside",
    "audio",
    "b",
    "base",
    "bdi",
    "bdo",
    "blockquote",
    "body",
    "br",
    "button",
    "canvas",
    "caption",
    "cite",
    "code",
    "col",
    "colgroup",
    "data",
    "datalist",
    "dd",
    "del",
    "details",
    "dfn",
    "dialog",
    "div",
    "dl",
    "dt",
    "em",
    "embed",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hgroup",
    "hr",
    "html",
    "htmlVar",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "label",
    "legend",
    "li",
    "link",
    "main",
    "map",
    "mark",
    "menu",
    "meta",
    "meter",
    "nav",
    "noscript",
    "object",
    "ol",
    "optgroup",
    "option",
    "output",
    "p",
    "picture",
    "pre",
    "progress",
    "q",
    "rp",
    "rt",
    "ruby",
    "s",
    "samp",
    "script",
    "section",
    "select",
    "slot",
    "small",
    "source",
    "span",
    "strong",
    "style",
    "sub",
    "summary",
    "sup",
    "table",
    "tbody",
    "td",
    "template",
    "textarea",
    "tfoot",
    "th",
    "thead",
    "time",
    "title",
    "tr",
    "track",
    "u",
    "ul",
    "video",
    "wbr",
]

SVG_FUNCTIONS = [
    "a",
    "animate",
    "animateMotion",
    "animateTransform",
    "circle",
    "clipPath",
    "defs",
    "desc",
    "ellipse",
    "feBlend",
    "feColorMatrix",
    "feComponentTransfer",
    "feComposite",
    "feConvolveMatrix",
    "feDiffuseLighting",
    "feDisplacementMap",
    "feDistantLight",
    "feDropShadow",
    "feFlood",
    "feFuncA",
    "feFuncB",
    "feFuncG",
    "feFuncR",
    "feGaussianBlur",
    "feImage",
    "feMerge",
    "feMergeNode",
    "feMorphology",
    "feOffset",
    "fePointLight",
    "feSpecularLighting",
    "feSpotLight",
    "feTile",
    "feTurbulence",
    "filter",
    "foreignObject",
    "g",
    "image",
    "line",
    "linearGradient",
    "marker",
    "mask",
    "metadata",
    "mpath",
    "path",
    "pattern",
    "polygon",
    "polyline",
    "radialGradient",
    "rect",
    "script",
    "set",
    "stop",
    "style",
    "svg",
    "svgSwitch",
    "svgUse",
    "symbol",
    "text",
    "textPath",
    "title",
    "tspan",
    "view",
]


def _declared(module_name):
    module = importlib.import_module(module_name)
    if "html" in module_name:
        expected = set(n.lower() for n in HTML_FUNCTIONS)
    else:
        expected = set(n.lower() for n in SVG_FUNCTIONS)
    return sorted(
        name
        for name, obj in inspect.getmembers(module, inspect.isfunction)
        if obj.__module__ == module_name and name in expected
    )


def test_every_html_factory_creates_its_tag():
    from pure.core.HTML import SELF_CLOSE_HTML_TAGS

    from pure import html as html_module

    for name in HTML_FUNCTIONS:
        tag = "var" if name == "htmlVar" else name
        factory_name = (
            "Del" if name == "del" else ("var" if name == "htmlVar" else name)
        )
        factory = getattr(html_module, factory_name)
        assert callable(factory), f"{name}() is declared."
        element = factory()

        assert isinstance(element, HTML), f"{name}()"
        assert element.get_tag_name() == tag, f"{name}() tag name"
        assert element.get_self_close() == (
            tag.lower() in SELF_CLOSE_HTML_TAGS
        ), f"{name}() self-close flag"


def test_every_svg_factory_creates_its_tag():
    from pure.core.SVG import SELF_CLOSE_SVG_TAGS

    from pure import svg as svg_module

    for name in SVG_FUNCTIONS:
        if name == "svgUse":
            tag = "use"
        elif name == "svgSwitch":
            tag = "switch"
        else:
            tag = name
        factory_name = (
            "switch" if name == "svgSwitch" else ("use" if name == "svgUse" else name)
        )
        factory = getattr(svg_module, factory_name)
        assert callable(factory), f"{name}() is declared."
        element = factory()

        assert isinstance(element, SVG), f"{name}()"
        assert element.get_tag_name() == tag, f"{name}() tag name"
        assert element.get_self_close() == (
            tag in SELF_CLOSE_SVG_TAGS
        ), f"{name}() self-close flag"


def test_a_tag_class_builds_an_element_by_reading_its_name():
    # purephp reaches the same element through `__callStatic`, so a static
    # read on the class is the mirror of a module-level function.
    assert HTML.div("hi").render() == "<div>hi</div>"
    assert SVG.circle("hi").render() == "<circle>hi</circle>"
    assert XML.row("hi").render() == "<row>hi</row>"

    from pure.html import div

    assert HTML.div("hi").render() == div("hi").render()


def test_a_custom_element_needs_no_declaration():
    # A magic static call needs no entry either, so a tag the library does not
    # know is still constructible. An unknown name is not a void element either,
    # so it keeps its closing tag the way `SVG.circle()` does not.
    assert HTML.myWidget("x").render() == "<myWidget>x</myWidget>"
    assert SVG.myShape().render() == "<myShape></myShape>"


def test_a_static_element_behaves_like_the_function_one():
    assert HTML.br().render() == "<br />"
    assert HTML.div("a", "b").render() == "<div>ab</div>"
    assert HTML.div().render() == "<div></div>"
    assert HTML.a("x").href("/y").render() == '<a href="/y">x</a>'
    # The cast the class inherits applies here too.
    assert HTML.div(True).render() == "<div>1</div>"


def test_an_underscored_name_is_not_an_element():
    # The machinery Python probes for (copy, pickle, the ABC registry) reads
    # underscored attributes, and each has to keep raising AttributeError
    # instead of building an element named after it.
    for cls in (HTML, SVG, XML):
        with pytest.raises(AttributeError):
            getattr(cls, "_missing_")

