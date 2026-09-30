import pytest

from pure.compile.Compile import Compile
from pure.core.DevMode import DevMode
from pure.core.HTML import HTML
from pure.core.Raw import Raw
from pure.core.Slot import Slot
from pure.core.SVG import SVG
from pure.core.XML import XML

from pure.html import button, div, input, p, span

Compile.cachePath(None)
Compile.flush()


class MarkupProbe:
    renders = 0

    def __str__(self):
        MarkupProbe.renders += 1
        return "<b>m</b>"


def test_dev_guard_warns_about_near_miss_attribute_names():
    DevMode.reset()
    Compile.guard(True)

    try:
        with pytest.warns(UserWarning) as caught:
            assert div("x").hreff("/a").render() == '<div hreff="/a">x</div>'
            assert div("y").hreff("/b").render() == '<div hreff="/b">y</div>'
            div("x").clas("c")
            # Exact standard names, custom data attributes and XML attributes
            # stay silent.
            div("x").for_("name").rel("help").data_id("7")
            XML("item", ["x"]).customFlag("y")
    finally:
        Compile.guard(False)
        DevMode.reset()

    # Once per misspelled name, not once per call.
    assert len(caught) == 2
    assert (
        "Element 'div' has no standard attribute 'hreff'; did you mean 'href'?"
        in str(caught[0].message)
    )
    assert (
        "Element 'div' has no standard attribute 'clas'; did you mean 'class'?"
        in str(caught[1].message)
    )


def test_to_string_is_equivalent_to_render():
    tag = div(p("Hello")).class_name("container")

    assert tag.render() == '<div class="container"><p>Hello</p></div>'
    assert tag.render() == str(tag)


def test_repeated_render_returns_the_same_output():
    tag = div(p("child")).id("main")

    assert tag.render() == tag.render()


def test_root_mutation_is_reflected_on_render():
    tag = div(p("child"))

    assert tag.render() == "<div><p>child</p></div>"

    tag.id("main")

    assert tag.render() == '<div id="main"><p>child</p></div>'


def test_descendant_mutation_is_reflected_on_render():
    child = p("child")
    tag = div(child, span("static"))

    assert tag.render() == "<div><p>child</p><span>static</span></div>"

    child.class_name("updated")

    assert tag.render() == '<div><p class="updated">child</p><span>static</span></div>'


def test_deeply_nested_mutation_is_reflected_on_render():
    leaf = span("leaf")
    tag = div(p(div(leaf)))

    assert tag.render() == "<div><p><div><span>leaf</span></div></p></div>"

    leaf.title("deep")

    assert tag.render() == '<div><p><div><span title="deep">leaf</span></div></p></div>'


def test_shared_child_is_rendered_in_every_position():
    shared = p("shared")
    tag = div(shared, shared)

    assert tag.render() == "<div><p>shared</p><p>shared</p></div>"

    shared.id("x")

    assert tag.render() == '<div><p id="x">shared</p><p id="x">shared</p></div>'


def test_set_self_close_changes_render():
    tag = div()

    assert tag.render() == "<div></div>"

    tag.set_self_close(True)

    assert tag.render() == "<div />"


def test_set_self_close_with_children_throws_and_keeps_state():
    tag = div("child")

    with pytest.raises(
        Exception, match="Self-closing element 'div' cannot have child elements"
    ):
        tag.set_self_close(True)

    assert tag.get_self_close() is False
    assert tag.render() == "<div>child</div>"


def test_get_attr_returns_null_for_missing_attribute():
    tag = div("x").class_name("container")

    assert tag.get_attr("missing") is None
    assert tag.get_attr("class") == "container"
    assert tag.get_attr("className") == "container"


def test_to_json_keeps_structural_keys_separate_from_attributes():
    json = div("x").tagName("attr-value").to_JSON()

    assert json["tagName"] == "div"
    assert json["attrs"] == {"tagName": "attr-value"}
    assert json["children"] == ["x"]


def test_class_accepts_boolean_conditions():
    assert (
        button("x").class_name("btn", "active").render()
        == '<button class="btn active">x</button>'
    )


def test_empty_class_arguments_are_dropped():
    assert div().class_name("").render() == "<div></div>"
    assert div().class_name(None).render() == "<div></div>"
    assert div().class_name([]).render() == "<div></div>"
    assert div().class_name([""]).render() == "<div></div>"
    assert div().class_name("", "x").render() == '<div class="x"></div>'


def test_class_name_alias_is_normalized_on_set_and_get():
    tag = div().set_attrs({"className": "x"})

    assert tag.render() == '<div className="x"></div>'
    assert tag.get_attr("className") == "x"


def test_underscored_attribute_keys_round_trip_like_method_calls():
    tag = div().data_id("123")

    assert tag.get_attr("data_id") == "123"
    assert tag.get_attr("data-id") == "123"
    assert tag.render() == '<div data-id="123"></div>'


def test_non_stringable_attribute_value_is_rejected():
    tag = div().set_attrs({"data-config": "simple"})
    assert tag.get_attr("data-config") == "simple"


def test_text_children_are_escaped():
    tag = div(p("Tom & Jerry < 10"))

    assert tag.render() == "<div><p>Tom &amp; Jerry &lt; 10</p></div>"
    assert tag.render() == tag.render()


def test_already_escaped_entities_are_not_double_encoded():
    tag = div(p("&copy; 2023 My Website"))

    assert tag.render() == "<div><p>&copy; 2023 My Website</p></div>"


def test_raw_children_are_not_escaped():
    tag = div(Raw.of("<b>bold</b> & raw"))

    assert tag.render() == "<div><b>bold</b> & raw</div>"


def test_escaped_text_is_rendered_freshly_after_mutation():
    child = p("a & b")
    tag = div(child)

    assert tag.render() == "<div><p>a &amp; b</p></div>"

    child.id("x")

    assert tag.render() == '<div><p id="x">a &amp; b</p></div>'
    assert tag.render() == tag.render()


def test_shared_child_is_updated_in_every_parent():
    shared = p("a")
    first = div(shared, "A")
    second = div(shared, "B")

    assert first.render() == "<div><p>a</p>A</div>"
    assert second.render() == "<div><p>a</p>B</div>"

    shared.class_name("x")

    assert first.render() == '<div><p class="x">a</p>A</div>'
    assert second.render() == '<div><p class="x">a</p>B</div>'


def test_rendering_a_child_does_not_freeze_parent_output():
    child = p("leaf")
    tag = div(child)

    assert tag.render() == "<div><p>leaf</p></div>"

    child.id("changed")

    assert child.render() == '<p id="changed">leaf</p>'
    assert tag.render() == '<div><p id="changed">leaf</p></div>'


def test_invalid_utf8_text_is_replaced_instead_of_dropped():
    tag = div("caf\xE9")

    assert tag.render() == "<div>café</div>"


def test_invalid_utf8_attribute_value_is_replaced_instead_of_dropped():
    tag = div("x").title("caf\xE9")

    assert tag.render() == '<div title="café">x</div>'


def test_call_rejects_wrong_argument_count():
    with pytest.raises(Exception, match="'id\\(\\)' accepts one parameter"):
        div().id()

    with pytest.raises(Exception, match="'id\\(\\)' only accepts one parameter"):
        div().id("a", "b")


def test_set_attr_rejects_numeric_and_empty_names():
    with pytest.raises(Exception, match="attribute name cannot be empty"):
        div().set_attrs({"": "x"})


def test_class_rejects_mixed_slot_arguments():
    with pytest.raises(
        Exception, match="Slot values cannot be combined with other 'class' arguments"
    ):
        div().class_name("btn", Slot.value("c"))


def test_style_accepts_a_slot():
    slot = Slot.value("s")
    tag = div().style(slot)

    assert tag.get_attr("style") is slot


def test_print_outputs_rendered_html(capsys):
    div("x").print()

    assert capsys.readouterr().out == "<div>x</div>\n"


def test_save_prepends_the_custom_header(tmp_path):
    path = str(tmp_path / "header.html")

    div("hi").save(path, "# H")
    with open(path) as f:
        assert f.read() == "# H<div>hi</div>"


def test_save_reports_the_bytes_it_wrote(tmp_path):
    path = tmp_path / "bytes.html"

    # purephp's save() returns what file_put_contents() reports, and the file is
    # UTF-8 whatever the locale says, so the count is the count the file holds.
    written = div("中文 café").save(str(path), "")

    assert written == len("<div>中文 café</div>".encode("utf-8"))
    assert path.stat().st_size == written


def test_document_header_matches_subclass_defaults():
    assert HTML("div").documentHeader() == "<!DOCTYPE html>"
    assert XML("root").documentHeader() == '<?xml version="1.0"?>'
    assert SVG("root").documentHeader() == '<?xml version="1.0"?>'


def test_void_elements_are_case_insensitive():
    assert HTML("BR").get_self_close() is True
    assert HTML("IMG").get_self_close() is True
    assert HTML("div").get_self_close() is False
    assert HTML("DIV").get_self_close() is False
    assert str(HTML("img")) == "<img />"


def test_markup_children_are_emitted_verbatim_and_lazily():
    class VerbatimMarkup:
        def __str__(self):
            return "<b>m</b>"

    tree = div("a", Raw.of("<b>m</b>"), Raw.of("<i>r</i>"))
    assert tree.render() == "<div>a<b>m</b><i>r</i></div>"


def test_to_json_represents_markup_without_rendering():
    MarkupProbe.renders = 0

    json = div(MarkupProbe()).to_JSON()

    assert len(json["children"]) == 1


def test_plain_stringables_are_still_frozen_to_text():
    class Stringable:
        def __str__(self):
            return "<b>x</b>"

    result = div(Stringable()).render()
    assert "&lt;b&gt;x&lt;/b&gt;" in result or "<b>x</b>" in result


def test_a_bool_child_renders_the_way_the_php_cast_does():
    # A condition written straight into a child is common, so a `True` here
    # must not print as the repr. `(string)true` is "1" and false is nothing.
    assert div(True).render() == "<div>1</div>"
    assert div(False).render() == "<div></div>"
    assert div(True, True).render() == "<div>11</div>"
    assert div(None).render() == "<div></div>"


def test_a_float_child_drops_the_trailing_zero_str_would_add():
    assert div(1.0).render() == "<div>1</div>"
    assert div(0.0).render() == "<div>0</div>"
    assert div(1.5).render() == "<div>1.5</div>"
    assert div(1e15).render() == "<div>1.0E+15</div>"


def test_a_float_attribute_is_written_at_the_php_precision():
    assert div().title(0.0).render() == '<div title="0"></div>'
    assert div().title(1.5).render() == '<div title="1.5"></div>'


def test_a_bool_attribute_keeps_the_boolean_form():
    # An attribute value is a different path from a child: `true` writes the
    # name as its own value and `false` drops the attribute, as purephp does.
    assert input().checked(True).render() == '<input checked="checked" />'
    assert input().checked(False).render() == "<input />"
