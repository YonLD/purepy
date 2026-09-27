import importlib
import inspect

from pure.core.HTML import HTML
from pure.core.SVG import SVG

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
