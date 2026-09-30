import pytest

from pure.compile.Compile import Compile
from pure.core.MissingSlotException import MissingSlotException
from pure.core.Slot import Slot

from pure.html import div, em, li, span, table, tr, ul

Compile.cachePath(None)
Compile.flush()


def test_if_renders_then_or_else_branch():
    shape = Compile.shape(div(Slot.if_("admin", span("admin"), span("guest"))))

    assert shape({"admin": True}) == "<div><span>admin</span></div>"
    assert shape({"admin": False}) == "<div><span>guest</span></div>"


def test_if_without_else_renders_nothing_when_falsy():
    shape = Compile.shape(div("a", Slot.if_("show", span("!")), "b"))

    assert shape({"show": True}) == "<div>a<span>!</span>b</div>"
    assert shape({"show": False}) == "<div>ab</div>"


def test_if_branches_share_the_current_scope():
    shape = Compile.shape(div(Slot.if_("admin", span(Slot.value("name")))))

    assert shape({"admin": True, "name": "root"}) == "<div><span>root</span></div>"


def test_if_inside_each_uses_item_scope():
    item = Compile.shape(li(Slot.value("name"), Slot.if_("admin", span("(a)"))))
    shape = Compile.shape(ul(Slot.each("items", item)))

    assert shape(
        {"items": [{"name": "x", "admin": True}, {"name": "y", "admin": False}]}
    ) == "<ul><li>x<span>(a)</span></li><li>y</li></ul>"


def test_nested_slots_accept_bare_tag_trees():
    bare = Compile.shape(
        div(
            Slot.child("box", span(Slot.value("label"))),
            Slot.each("items", li(Slot.value("value"))),
            Slot.if_("flag", em("on"), em("off")),
        )
    )

    wrapped = Compile.shape(
        div(
            Slot.child("box", Compile.shape(span(Slot.value("label")))),
            Slot.each("items", Compile.shape(li(Slot.value("value")))),
            Slot.if_("flag", Compile.shape(em("on")), Compile.shape(em("off"))),
        )
    )

    assert bare.id() == wrapped.id()


def test_if_modifiers_are_rejected():
    slot = Slot.if_("show", span("x"))

    with pytest.raises(TypeError):
        slot.default(True)

    with pytest.raises(TypeError):
        slot.required(False)


def test_default_rejects_non_value_types():
    slot = Slot.value("value")

    assert slot.default_value is None


def test_default_falls_back_when_the_slot_is_absent():
    shape = Compile.shape(div(Slot.value("maybe").default("none")))

    assert shape({}) == "<div>none</div>"
    assert shape({"maybe": "here"}) == "<div>here</div>"


def test_default_accepts_a_value_type_array():
    item = Compile.shape(li(Slot.value("v")))
    shape = Compile.shape(ul(Slot.each("items", item)))

    assert shape({"items": [{"v": "a"}]}) == "<ul><li>a</li></ul>"


def test_if_slot_in_attribute_position_is_rejected():
    from pure.compile.CompileException import CompileException

    with pytest.raises(CompileException):
        Compile.shape(div("x").class_name(Slot.if_("on", span("y")))).compile()


# A list item may be the value of the one slot its item shape renders, so a
# list of strings is a list of strings instead of a list of one-key maps.


def test_each_slot_binds_a_scalar_item_to_the_one_key_its_shape_renders():
    shape = Compile.shape(ul(Slot.each("xs", li(Slot.value("value")))))

    assert shape({"xs": ["a", "b"]}) == "<ul><li>a</li><li>b</li></ul>"
    # A mapping item is a scope of its own, so both forms render together.
    assert shape({"xs": [{"value": "a"}, "b"]}) == "<ul><li>a</li><li>b</li></ul>"
    assert shape({"xs": [1, 2]}) == "<ul><li>1</li><li>2</li></ul>"


def test_each_slot_binds_a_scalar_item_to_an_attribute_slot_too():
    shape = Compile.shape(
        ul(Slot.each("xs", li(Slot.value("value")).class_(Slot.value("value"))))
    )

    assert shape({"xs": ["a", "b"]}) == (
        '<ul><li class="a">a</li><li class="b">b</li></ul>'
    )


def test_each_slot_binds_a_scalar_item_through_nested_scopes():
    shape = Compile.shape(table(tr(Slot.each("cells", li(Slot.value("value"))))))

    assert shape({"cells": ["a", "b"]}) == (
        "<table><tr><li>a</li><li>b</li></tr></table>"
    )


def test_a_null_each_item_reports_the_slot_it_was_bound_to():
    shape = Compile.shape(ul(Slot.each("xs", li(Slot.value("value")))))

    with pytest.raises(
        MissingSlotException,
        match=r"slot 'xs\[\]\.value' is required but was null.",
    ):
        shape({"xs": [None]})


def test_each_slot_rejects_a_scalar_item_when_its_shape_reads_several_keys():
    shape = Compile.shape(ul(Slot.each("xs", li(Slot.value("a"), Slot.value("b")))))

    with pytest.raises(TypeError) as caught:
        shape({"xs": ["x"]})

    assert (
        "The item shape of this slot reads 'a' and 'b', so each item must be "
        "an array." in str(caught.value)
    )


def test_each_slot_rejects_a_scalar_item_when_its_shape_reads_a_nested_scope():
    box = Compile.shape(div(Slot.child("card", span(Slot.value("name")))))
    shape = Compile.shape(ul(Slot.each("xs", box)))

    with pytest.raises(TypeError) as caught:
        shape({"xs": ["x"]})

    assert (
        "The item shape of this slot reads 'card', so each item must be an array."
        in str(caught.value)
    )


def test_each_slot_rejects_a_scalar_item_when_its_shape_reads_no_slots():
    shape = Compile.shape(ul(Slot.each("xs", li("static"))))

    with pytest.raises(TypeError) as caught:
        shape({"xs": ["x"]})

    assert (
        "The item shape of this slot reads no slots, so each item must be an "
        "empty array." in str(caught.value)
    )


def test_each_slot_still_needs_a_mapping_item_for_its_own_keys():
    shape = Compile.shape(ul(Slot.each("xs", li(Slot.value("value")))))

    with pytest.raises(
        MissingSlotException,
        match=r"slot 'xs\[\]\.value' is required but was not provided",
    ):
        shape({"xs": [{"other": "a"}]})


def test_each_slot_binds_a_scalar_item_to_a_raw_slot():
    shape = Compile.shape(ul(Slot.each("xs", li(Slot.raw("html")))))

    assert shape(
        {"xs": ["<b>a</b>", "<i>b</i>"]}
    ) == "<ul><li><b>a</b></li><li><i>b</i></li></ul>"


def test_each_slot_rejects_a_scalar_item_when_its_shape_reads_the_key_as_a_scope():
    # The shape renders 'box' as a value *and* reads it as a child scope, so an
    # item cannot stand in for the scope alone.
    shape = Compile.shape(
        ul(Slot.each("xs", div(Slot.value("box"), Slot.child("box", li("x")))))
    )

    with pytest.raises(TypeError) as caught:
        shape({"xs": ["a"]})

    assert "each item must be an array." in str(caught.value)


def test_each_slot_rejects_a_scalar_item_when_its_shape_only_reads_a_condition():
    # A condition is a truthiness read, not a rendered value: binding a scalar
    # to it would pick a branch per item, which the shape never asked for.
    shape = Compile.shape(
        ul(Slot.each("xs", li(Slot.if_("flag", em("y"), em("n")))))
    )

    with pytest.raises(TypeError) as caught:
        shape({"xs": ["a"]})

    assert "each item must be an array." in str(caught.value)
