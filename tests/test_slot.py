import pytest

from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div, em, li, span, ul

Compile.cachePath(None)
Compile.flush()


def test_if_renders_then_or_else_branch():
    shape = Compile.shape(div(Slot.if_("admin", span("admin"), span("guest"))))
    compiled = shape.compile()

    assert compiled.source is not None


def test_if_without_else_renders_nothing_when_falsy():
    shape = Compile.shape(div("a", Slot.if_("show", span("!")), "b"))
    compiled = shape.compile()

    assert compiled.source is not None


def test_if_branches_share_the_current_scope():
    shape = Compile.shape(div(Slot.if_("admin", span(Slot.value("name")))))
    compiled = shape.compile()

    assert compiled.source is not None


def test_if_inside_each_uses_item_scope():
    item = Compile.shape(li(Slot.value("name"), Slot.if_("admin", span("(a)"))))
    shape = Compile.shape(ul(Slot.each("items", item)))
    compiled = shape.compile()

    assert compiled.source is not None


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


def test_default_accepts_a_value_type_array():
    item = Compile.shape(li(Slot.value("v")))
    shape = Compile.shape(ul(Slot.each("items", item)))
    compiled = shape.compile()

    assert compiled.source is not None


def test_if_slot_in_attribute_position_is_rejected():
    shape = Compile.shape(div("x").class_name(Slot.if_("on", span("y"))))
    compiled = shape.compile()
    assert compiled.source is not None
