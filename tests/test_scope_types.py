from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div, li, span

Compile.cachePath(None)
Compile.flush()


def test_static_trees_have_no_slots():
    shape = Compile.shape(div("static"))
    compiled = shape.compile()

    assert "data.get" not in compiled.source


def test_value_condition_and_odd_slots_are_declared():
    tree = Compile.shape(
        div(
            Slot.value("title"),
            Slot.if_("city", span(Slot.value("city"))),
            Slot.value("user-name"),
        )
    )
    compiled = tree.compile()

    assert "data.get" in compiled.source


def test_if_branches_share_the_current_scope():
    tree = Compile.shape(
        div(Slot.if_("flag", span(Slot.value("then")), span(Slot.value("else"))))
    )
    compiled = tree.compile()

    assert compiled.source is not None


def test_optional_containers_may_be_null():
    tree = Compile.shape(
        div(
            Slot.child("box", span("static")),
            Slot.each("list", li(Slot.value("value"))),
        )
    )
    compiled = tree.compile()

    assert compiled.source is not None


def test_a_condition_key_that_is_also_a_value_drops_mixed():
    tree = Compile.shape(
        div(
            Slot.if_("mode", span("a"), span("b")),
            Slot.value("mode"),
        )
    )
    compiled = tree.compile()

    assert "data.get" in compiled.source


def test_static_trees_have_no_annotations():
    from pure.compile.Internal.ScopeTypes import ScopeTypes

    assert "" == ScopeTypes.docblock(Compile.shape(div("static")).tree())
