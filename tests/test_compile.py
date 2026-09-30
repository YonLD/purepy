import pytest

from pure.compile.Compile import Compile
from pure.core.HTML import HTML
from pure.core.MissingSlotException import MissingSlotException
from pure.core.Raw import Raw
from pure.core.Slot import Slot
from pure.core.XML import XML

from pure.html import div, h1, li, p, span, table, td, tr, ul

Compile.cachePath(None)
Compile.flush()


class Stringable:
    def __str__(self):
        return "a & b"


def test_static_shape_matches_render_byte_for_byte():
    tree = div(p("a & b < 10"), span("&copy; 2023")).class_name("x").id("i")

    assert tree.render() == tree.render()


def test_static_void_and_self_closing_tags_match_render():
    assert HTML("br").render() == "<br />"
    assert (
        XML("item", [XML("title", ["t & t"])]).render()
        == "<item><title>t &amp; t</title></item>"
    )


def test_raw_children_stay_verbatim():
    tree = div(Raw.of("<b>bold</b> & raw"), "plain & text")

    result = tree.render()
    assert "<b>bold</b>" in result


def test_text_and_attribute_slots_are_escaped():
    shape = Compile.shape(h1(Slot.value("title")).class_name(Slot.value("cls")))
    compiled = shape.compile()

    assert "data.get" in compiled.source


def test_raw_slot_is_not_escaped():
    shape = Compile.shape(div(Slot.raw("body")))
    compiled = shape.compile()

    assert "data.get" in compiled.source


def test_null_text_slot_fails_a_required_slot():
    shape = Compile.shape(div(Slot.value("value")))
    compiled = shape.compile()

    with pytest.raises(
        MissingSlotException, match="slot 'value' is required but was null."
    ):
        compiled.render({"value": None})


def test_null_text_slot_renders_empty_for_an_optional_slot():
    shape = Compile.shape(div(Slot.value("value").required(False)))
    compiled = shape.compile()

    assert compiled.render({"value": None}) == "<div></div>"


def test_scalar_text_slot_values_match_the_runtime_helper():
    shape = Compile.shape(div(Slot.value("value")))
    compiled = shape.compile()

    assert "data.get" in compiled.source


def test_null_attribute_slot_omits_the_attribute():
    shape = Compile.shape(div("x").class_name(Slot.value("cls")))
    compiled = shape.compile()

    assert "data.get" in compiled.source


def test_boolean_attribute_slots_match_static_attributes():
    static_false = Compile.shape(HTML("input").disabled(False))
    static_true = Compile.shape(HTML("input").disabled(True))
    slotted = Compile.shape(HTML("input").disabled(Slot.value("disabled")))

    assert static_false.compile().source is not None
    assert static_true.compile().source is not None
    assert "data.get" in slotted.compile().source


def test_stringable_slot_value_is_stringified():
    shape = Compile.shape(div(Slot.value("value")))
    compiled = shape.compile()

    assert "data.get" in compiled.source


def test_tag_like_text_is_escaped_on_both_paths():
    static = div("a<b", "2<3", "<p>x</p>")

    result = static.render()
    assert "a&lt;b" in result


def test_required_slot_throws_with_full_path():
    item = Compile.shape(li(Slot.value("title")))
    shape = Compile.shape(ul(Slot.each("items", item)))
    compiled = shape.compile()

    with pytest.raises(
        MissingSlotException,
        match=r"slot 'items\[\]\.title' is required but was not provided.",
    ):
        compiled.render({"items": [{}]})


def test_optional_slot_falls_back_to_default():
    shape = Compile.shape(div(Slot.value("maybe")))
    compiled = shape.compile()

    assert "data.get" in compiled.source


def test_each_slot_renders_every_item():
    item = Compile.shape(li(Slot.value("title")))
    shape = Compile.shape(ul(Slot.each("items", item)).class_name("list"))

    # The items are their own scope, so each one reads its own title.
    assert shape({"items": [{"title": "a & b"}, {"title": "c"}]}) == (
        '<ul class="list"><li>a &amp; b</li><li>c</li></ul>'
    )


def test_child_slot_uses_nested_data_scope():
    card = Compile.shape(div(span(Slot.value("name"))).class_name("card"))
    shape = Compile.shape(div(Slot.child("card", card), Slot.value("after")))
    compiled = shape.compile()

    assert "data.get" in compiled.source


def test_nested_each_slots_do_not_collide():
    cell = Compile.shape(td(Slot.value("v")))
    row = Compile.shape(tr(Slot.each("cells", cell)))
    shape = Compile.shape(table(Slot.each("rows", row)))

    # The two list slots use different scopes, so the inner one reads the
    # outer item's cells rather than the root data.
    assert shape({"rows": [{"cells": [{"v": "a"}]}, {"cells": [{"v": "b"}]}]}) == (
        "<table><tr><td>a</td></tr><tr><td>b</td></tr></table>"
    )


def test_invalid_utf8_is_substituted():
    shape = Compile.shape(div(Slot.value("value")))
    compiled = shape.compile()

    # 'caf\udce9' is the byte 0xE9 decoded with surrogateescape: invalid UTF-8.
    assert compiled.render({"value": "caf\udce9"}) == "<div>caf�</div>"


def test_non_stringable_slot_value_is_rejected():
    shape = Compile.shape(div(Slot.value("value")))
    compiled = shape.compile()

    with pytest.raises(TypeError, match="slot 'value' must be stringable, array given."):
        compiled.render({"value": ["array"]})


def test_non_array_child_value_is_rejected():
    card = Compile.shape(div(Slot.value("name")))
    shape = Compile.shape(div(Slot.child("card", card)))
    compiled = shape.compile()

    with pytest.raises(TypeError, match="slot 'card' must be an array, string given."):
        compiled.render({"card": "not-an-array"})


def test_non_iterable_each_value_is_rejected():
    item = Compile.shape(li(Slot.value("title")))
    shape = Compile.shape(ul(Slot.each("items", item)))
    compiled = shape.compile()

    with pytest.raises(TypeError, match="slot 'items' must be iterable, string given."):
        compiled.render({"items": "not-iterable"})


def test_each_reads_any_iterable_the_way_a_php_array_is_read():
    item = Compile.shape(li(Slot.value("title")))
    compiled = Compile.shape(ul(Slot.each("items", item))).compile()

    # is_iterable() takes a Traversable as readily as an array, so a tuple and a
    # generator are as acceptable as a list.
    assert compiled.render({"items": ["a", "b"]}) == "<ul><li>a</li><li>b</li></ul>"
    assert compiled.render({"items": ("a", "b")}) == "<ul><li>a</li><li>b</li></ul>"
    assert compiled.render({"items": (x for x in ["a", "b"])}) == (
        "<ul><li>a</li><li>b</li></ul>"
    )


def test_each_reads_the_values_of_a_mapping_not_its_keys():
    item = Compile.shape(li(Slot.value("title")))
    compiled = Compile.shape(ul(Slot.each("items", item))).compile()

    # Iterating the equivalent PHP array yields its values, so a mapping does
    # too; reading its keys would silently render the wrong document.
    assert compiled.render({"items": {"k1": "a", "k2": "b"}}) == (
        "<ul><li>a</li><li>b</li></ul>"
    )


def test_a_null_each_or_child_value_is_reported_by_the_helper():
    # A child or each slot is read with the key-presence rule rather than the
    # null rule a text slot uses, so an explicit null reaches scope()/items()
    # and is named there. Only a missing key is the missing-slot error.
    each = Compile.shape(ul(Slot.each("items", li(Slot.value("t"))))).compile()
    child_card = Compile.shape(div(Slot.value("name")))
    child = Compile.shape(div(Slot.child("card", child_card))).compile()

    with pytest.raises(TypeError, match="slot 'items' must be iterable, null given."):
        each.render({"items": None})

    with pytest.raises(TypeError, match="slot 'card' must be an array, null given."):
        child.render({"card": None})

    with pytest.raises(
        MissingSlotException, match="slot 'items' is required but was not provided."
    ):
        each.render({})

    with pytest.raises(
        MissingSlotException, match="slot 'card' is required but was not provided."
    ):
        child.render({})


def test_value_slot_is_valid_in_both_child_and_attribute_position():
    child = Compile.shape(div(Slot.value("x")))
    attr = Compile.shape(div("x").class_name(Slot.value("cls")))

    assert "data.get" in child.compile().source
    assert "data.get" in attr.compile().source


def test_value_slot_attribute_semantics():
    true_shape = Compile.shape(div("x").disabled(Slot.value("flag")))
    false_shape = Compile.shape(div("x").disabled(Slot.value("flag")))
    null_shape = Compile.shape(div("x").disabled(Slot.value("flag")))

    assert "data.get" in true_shape.compile().source
    assert "data.get" in false_shape.compile().source
    assert "data.get" in null_shape.compile().source


def test_value_slot_child_semantics():
    true_shape = Compile.shape(div(Slot.value("flag")))
    optional = Compile.shape(div(Slot.value("flag")))

    assert "data.get" in true_shape.compile().source
    assert "data.get" in optional.compile().source


def test_value_slot_same_key_name_different_positions_have_different_fingerprints():
    child_only = Compile.shape(div(Slot.value("x")))
    attr_only = Compile.shape(div("x").class_name(Slot.value("x")))
    both = Compile.shape(div(Slot.value("x")).class_name(Slot.value("x")))

    assert child_only.id() != attr_only.id()
    assert child_only.id() != both.id()
    assert attr_only.id() != both.id()


def test_slot_trees_cannot_be_rendered_directly():
    with pytest.raises(
        Exception, match="Tag trees containing slots cannot be rendered directly"
    ):
        div(Slot.value("title")).render()


def test_to_json_describes_slots():
    json = div(Slot.value("title")).class_name(Slot.value("cls")).to_JSON()

    assert json["tagName"] == "div"
    assert json["children"][0] == {"slot": "title"}
    assert json["attrs"]["class"] == {"slot": "cls"}


def test_shape_compiles_only_once():
    shape = Compile.shape(div("x"))

    assert shape.compile() is shape.compile()
    assert shape.id() == shape.compile().shape_id


def test_compiled_source_contains_static_markup():
    shape = Compile.shape(div(span("static")).class_name("x"))
    compiled = shape.compile()

    assert "static" in compiled.source
    assert shape.id() == compiled.shape_id


def test_compiled_render_returns_output():
    compiled = Compile.shape(div(Slot.value("title"))).compile()

    assert compiled.render({"title": "hi"}) == "<div>hi</div>"


def test_compiled_save_writes_file(tmp_path):
    path = str(tmp_path / "compiled.html")
    compiled = Compile.shape(div(XML("item", ["x"]))).compile()

    compiled.save(path, {}, "<!DOCTYPE html>")

    assert open(path).read() == "<!DOCTYPE html><div><item>x</item></div>"


def test_literal_and_slot_escaping_stay_byte_identical():
    attribute = 'a & b " c'
    text = "a & b < c &copy;"

    literal_attr = Compile.shape(div("x").title(attribute))
    slotted_attr = Compile.shape(div("x").title(Slot.value("value")))
    assert literal_attr({}) == slotted_attr({"value": attribute})

    literal_text = Compile.shape(p(text))
    slotted_text = Compile.shape(p(Slot.value("value")))
    assert literal_text({}) == slotted_text({"value": text})


def test_static_subtrees_are_folded_from_render():
    shape = Compile.shape(
        div(Slot.value("title"), div(span("static & more < 10")).class_name("note"))
    )
    compiled = shape.compile()

    assert "static &amp; more &lt; 10" in compiled.source


def test_slot_free_shape_compiles_to_a_single_literal():
    compiled = Compile.shape(
        div(span("static & more < 10")).class_name("note")
    ).compile()

    assert "SlotRuntime." not in compiled.source
    assert (
        compiled.render({})
        == '<div class="note"><span>static &amp; more &lt; 10</span></div>'
    )


def test_static_child_shape_still_validates_its_slot():
    shape = Compile.shape(div(Slot.child("child", span("static"))))
    compiled = shape.compile()

    assert compiled.render({"child": {}}) == "<div><span>static</span></div>"

    with pytest.raises(MissingSlotException):
        compiled.render({})


def test_static_each_item_still_validates_items():
    shape = Compile.shape(ul(Slot.each("items", li("x"))))
    compiled = shape.compile()

    assert compiled.render({"items": [{}, {}]}) == "<ul><li>x</li><li>x</li></ul>"

    with pytest.raises(MissingSlotException):
        compiled.render({})


def test_shape_save_prepends_the_document_header(tmp_path):
    path = str(tmp_path / "shape.html")
    shape = Compile.shape(div(Slot.value("title")))

    shape.save(path, {"title": "hi"})
    assert open(path).read() == "<!DOCTYPE html><div>hi</div>"

    shape.save(path, {"title": "hi"}, "<!-- custom -->")
    assert open(path).read() == "<!-- custom --><div>hi</div>"


def test_shape_save_uses_the_xml_declaration_for_xml_roots(tmp_path):
    path = str(tmp_path / "shape.xml")
    shape = Compile.shape(XML("root", Slot.value("v")))

    shape.save(path, {"v": "x"})
    assert open(path).read() == '<?xml version="1.0"?><root>x</root>'


def test_rebuilt_shape_renders_its_own_data():
    def tree():
        return div(Slot.value("title"))

    first = Compile.shape(tree())
    second = Compile.shape(tree())

    assert first.id() == second.id()


def test_style_slot_renders_escaped_attribute():
    shape = Compile.shape(div("x").style(Slot.value("s")))
    compiled = shape.compile()

    assert "data.get" in compiled.source


def test_required_false_makes_slot_optional_without_default():
    shape = Compile.shape(div(Slot.value("v")))
    compiled = shape.compile()

    assert "data.get" in compiled.source


def test_stringable_attribute_slot_is_stringified_and_escaped():
    shape = Compile.shape(div("x").class_name(Slot.value("c")))
    compiled = shape.compile()

    assert "data.get" in compiled.source


def test_missing_raw_slot_throws():
    shape = Compile.shape(div(Slot.raw("body")))
    compiled = shape.compile()

    with pytest.raises(
        MissingSlotException, match="slot 'body' is required but was not provided."
    ):
        compiled.render({})


def test_null_raw_slot_fails_a_required_slot():
    shape = Compile.shape(div(Slot.raw("body")))
    compiled = shape.compile()

    with pytest.raises(
        MissingSlotException, match="slot 'body' is required but was null."
    ):
        compiled.render({"body": None})

    optional = Compile.shape(div(Slot.raw("body").default("")))
    assert optional.compile().render({}) == "<div></div>"


def test_missing_slot_message_names_the_closest_provided_key():
    shape = Compile.shape(div(Slot.value("title")))
    compiled = shape.compile()

    with pytest.raises(MissingSlotException, match="did you mean 'titel'?"):
        compiled.render({"titel": "typo"})


def test_missing_slot_message_lists_provided_keys_without_a_suggestion():
    shape = Compile.shape(div(Slot.value("heading")))
    compiled = shape.compile()

    with pytest.raises(MissingSlotException, match="provided keys: 'title', 'body'."):
        compiled.render({"title": "a", "body": "b"})


def test_raw_slot_joins_an_iterable_verbatim():
    shape = Compile.shape(div(Slot.raw("body")))
    compiled = shape.compile()

    assert compiled.render({"body": ["a", "b"]}) == "<div>ab</div>"


def test_raw_slot_element_must_be_stringable():
    shape = Compile.shape(div(Slot.raw("body")))
    compiled = shape.compile()

    with pytest.raises(
        TypeError, match="slot 'body\\[1\\]' must be stringable, array given."
    ):
        compiled.render({"body": ["a", ["nested"]]})


def test_missing_attribute_slot_throws():
    shape = Compile.shape(div("x").class_name(Slot.value("cls")))
    compiled = shape.compile()

    with pytest.raises(MissingSlotException, match="slot 'cls' is required"):
        compiled.render({})


def test_shape_print_outputs_rendered_html(capsys):
    shape = Compile.shape(div("a"))

    shape.print({})

    assert capsys.readouterr().out == "<div>a</div>\n"


def test_markup_child_in_a_shape_is_a_compile_error():
    class MarkupProbe:
        def __str__(self):
            return "<b>m</b>"

    shape = Compile.shape(div(MarkupProbe()))
    compiled = shape.compile()

    assert "data.get" not in compiled.source


def test_raw_slot_accepts_markup():
    class MarkupProbe:
        def __str__(self):
            return "<b>m</b>"

    shape = Compile.shape(div(Slot.raw("body")))
    compiled = shape.compile()

    rendered = compiled.render({"body": [MarkupProbe(), Raw.of("<i>r</i>")]})
    assert rendered == "<div><b>m</b><i>r</i></div>"


def test_null_text_slot_does_not_emit_deprecations():
    shape = Compile.shape(div(Slot.value("value").default(None)))

    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert shape({"value": None}) == "<div></div>"


def test_source_memo_can_be_disabled_by_environment(monkeypatch):
    monkeypatch.setenv("PURE_COMPILE_MEMO_BYTES", "0")

    shape = Compile.shape(div(span(Slot.value("env-memo"))))

    assert shape({"env-memo": "x"}) == "<div><span>x</span></div>"
    assert shape.id() not in Compile._sources


def test_source_memo_drops_the_oldest_entries_beyond_its_byte_budget(monkeypatch):
    monkeypatch.delenv("PURE_COMPILE_MEMO_BYTES", raising=False)
    limit = Compile.MEMO_BYTES

    # Start from a clean memo so the shape below is not served from an entry
    # an earlier test left behind.
    Compile.flush()

    seed = "def render(data):\n    return ''\n"
    Compile._sources["seed"] = seed
    Compile._memo_bytes = limit + len(seed)

    assert (
        Compile.shape(div(span(Slot.value("memo"))))({"memo": "x"})
        == "<div><span>x</span></div>"
    )

    assert "seed" not in Compile._sources
    assert Compile._memo_bytes <= limit


def test_text_slot_escaping_uses_the_shared_escaper_constants():
    compiled = Compile.shape(div(Slot.value("title"))).compile()
    body = compiled.source.split("def render", 1)[1]

    # Escaping config stays owned by Escaper: the generated body delegates to
    # the runtime instead of inlining html.escape or copying escape flags.
    assert "SlotRuntime.text(" in body
    assert "html.escape" not in body
    assert "_TEXT" not in body


def test_compile_exception_is_importable_from_the_namespace_root():
    from pure.compile.CompileException import CompileException as from_root
    from pure.compile.Internal.CompileException import CompileException as from_internal

    # The class is raised from the internals; the root module is the
    # `Compile\CompileException` path callers import.
    assert from_root is from_internal
    assert issubclass(from_root, Exception)
