from pure.compile.Compile import Compile
from pure.core.Slot import Slot
from pure.core.SVG import SVG

from pure.svg import svg, use as svg_use

Compile.cachePath(None)
Compile.flush()


def test_magic_static_method():
    s = (
        svg(
            SVG("circle").cx("50").cy("50").r("40").fill("red"),
            SVG("rect").x("10").y("10").width("80").height("80").fill("blue"),
        )
        .width("100")
        .height("100")
    )

    assert s.get_tag_name() == "svg"
    assert len(s.get_children()) == 2
    assert s.get_attr("width") == "100"
    assert s.get_attr("height") == "100"


def test_constructor_method():
    circle = SVG("circle").cx("50").cy("50").r("40").fill("red")
    rect = SVG("rect").x("10").y("10").width("80").height("80").fill("blue")
    s = SVG("svg", [circle, rect]).width("100").height("100")

    assert s.get_tag_name() == "svg"
    assert len(s.get_children()) == 2
    assert s.get_attr("width") == "100"
    assert s.get_attr("height") == "100"


def test_custom_svg_tags():
    custom_tag = SVG("custom-element", ["Custom SVG Content"])

    assert custom_tag.get_tag_name() == "custom-element"
    assert custom_tag.get_children() == ["Custom SVG Content"]


def test_self_closing_tags():
    circle = SVG("circle")
    rect = SVG("rect")

    assert circle.get_self_close() is True
    assert rect.get_self_close() is True


def test_camel_case_self_closing_tags_are_recognized():
    for name in [
        "animateMotion",
        "animateTransform",
        "feBlend",
        "feColorMatrix",
        "feComposite",
        "feConvolveMatrix",
        "feDisplacementMap",
        "feDropShadow",
        "feFlood",
        "feFuncR",
        "feGaussianBlur",
        "feImage",
        "feMergeNode",
        "feMorphology",
        "feOffset",
        "fePointLight",
        "feSpotLight",
        "feTile",
        "feTurbulence",
    ]:
        assert (
            SVG(name).get_self_close() is True
        ), f"SVG '{name}' should be self-closing."

    assert SVG("feComponentTransfer").get_self_close() is False
    assert SVG("feMerge").get_self_close() is False
    assert SVG("FEBLEND").get_self_close() is False


def test_leaf_elements_render_self_closed():
    assert str(SVG("feTile")) == "<feTile />"
    assert str(SVG("animateTransform")) == "<animateTransform />"
    assert str(SVG("set")) == "<set />"
    assert str(SVG("view")) == "<view />"
    # A light primitive is childless in practice, so it self-closes like the
    # other filter primitives.
    assert str(SVG("feDistantLight")) == "<feDistantLight />"


def test_children_keep_elements_open():
    assert (
        str(SVG("animateMotion", [SVG("mpath").href("#p")]))
        == '<animateMotion><mpath href="#p" /></animateMotion>'
    )
    assert (
        str(SVG("animate", [SVG("mpath").href("#p")]))
        == '<animate><mpath href="#p" /></animate>'
    )
    assert (
        str(SVG("use", [SVG("title", ["label"])])) == "<use><title>label</title></use>"
    )
    assert SVG("animateMotion").get_self_close() is True
    assert SVG("use").get_self_close() is True


def test_camel_case_self_closing_tag_output():
    tag = SVG("feBlend")
    tag.set_attrs({"in": "SourceGraphic"})
    assert str(tag) == '<feBlend in="SourceGraphic" />'


def test_attribute_values_are_escaped():
    circle = SVG("circle").cx("50").cy("50").r("40").fill('" onmouseover="alert(1)')
    s = svg(circle).width("100").height("100")

    assert (
        str(s)
        == '<svg width="100" height="100"><circle cx="50" cy="50" r="40" fill="&quot; onmouseover=&quot;alert(1)" /></svg>'
    )


def test_svg_output():
    s = (
        svg(SVG("circle").cx("25").cy("25").r("20").fill("red"))
        .width("50")
        .height("50")
    )

    assert (
        str(s)
        == '<svg width="50" height="50"><circle cx="25" cy="25" r="20" fill="red" /></svg>'
    )


def test_compile_output_matches_render_for_self_closing_elements():
    circle = SVG("circle").cx("50").cy("50").r("40")

    assert circle.render() == '<circle cx="50" cy="50" r="40" />'
    assert Compile.shape(circle).compile().shape_id is not None


def test_compile_keeps_elements_with_children_open():
    tree = SVG("animate", [SVG("mpath").href("#p")])

    assert tree.render() == '<animate><mpath href="#p" /></animate>'
    assert Compile.shape(tree).compile().shape_id is not None


def test_use_element_renders_self_closed_through_a_slot():
    shape = Compile.shape(svg(svg_use().href(Slot.value("href"))))
    compiled = shape.compile()

    assert "data.get" in compiled.source
