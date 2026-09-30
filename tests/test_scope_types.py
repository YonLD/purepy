from pure.compile.Compile import Compile
from pure.compile.Internal.PlainGenerator import PlainGenerator
from pure.compile.Internal.ScopeTypes import ScopeTypes
from pure.core.Slot import Slot

from pure.html import div, li, span

Compile.cachePath(None)
Compile.flush()


def _run_view(tree, **kwargs):
    namespace = {}
    exec(PlainGenerator.view(tree), namespace)

    return namespace["view"](**kwargs)


def test_static_trees_have_no_slots():
    types = ScopeTypes.of(Compile.shape(div("static")).tree())

    assert types == {}
    assert ScopeTypes.signature(div("static")) == "def view() -> str:"


def test_value_condition_and_odd_slots_are_declared():
    tree = div(
        Slot.value("title"),
        Slot.if_("city", span(Slot.value("city"))),
        Slot.value("user-name"),
    )

    types = ScopeTypes.of(tree)

    assert types["title"] == "Optional[str]"
    # A condition is read for truthiness, so its value is whatever is passed.
    assert types["city"] == "Any"

    signature = ScopeTypes.signature(tree)

    assert "title: Optional[str] = None" in signature
    assert "data: Optional[Dict[str, Any]] = None" in signature


def test_both_branches_of_a_condition_read_the_current_scope():
    tree = div(
        Slot.if_("flag", span(Slot.value("yes")), span(Slot.value("no")))
    )

    types = ScopeTypes.of(tree)

    # A key read only inside a branch is still read by this scope, so the view
    # takes it as a parameter instead of raising on it.
    assert set(types) == {"flag", "yes", "no"}
    assert _run_view(tree, flag=True, yes="Y", no="N") == "<div><span>Y</span></div>"
    assert _run_view(tree, flag=False, yes="Y", no="N") == "<div><span>N</span></div>"


def test_a_branch_key_named_after_a_keyword_reads_the_data_offsets():
    tree = div(Slot.if_("flag", span(Slot.value("else"))))

    # The key is collected, so the view declares the mapping it reads it from.
    assert "else" in ScopeTypes.of(tree)
    assert _run_view(tree, flag=True, data={"else": "E"}) == "<div><span>E</span></div>"


def test_optional_containers_may_be_null():
    tree = div(
        Slot.child("box", span("static")),
        Slot.each("list", li(Slot.value("a"), Slot.value("b"))),
    )

    types = ScopeTypes.of(tree)

    assert types["box"] == "Dict[str, Any]"
    assert types["list"] == "Iterable[Dict[str, Any]]"


def test_a_list_item_may_be_the_value_its_shape_renders():
    tree = div(Slot.each("xs", li(Slot.value("value"))))

    # A shape that renders one key also accepts a scalar standing for the whole
    # item scope, so the plain view binds it the way the runtime does.
    assert ScopeTypes.of(tree)["xs"] == "Iterable[Union[Dict[str, Any], str]]"

    # A shape that reads several keys still takes a mapping per item.
    wide = div(Slot.each("xs", li(Slot.value("a"), Slot.value("b"))))

    assert ScopeTypes.of(wide)["xs"] == "Iterable[Dict[str, Any]]"


def test_a_raw_slot_takes_markup_as_well_as_text():
    types = ScopeTypes.of(div(Slot.raw("body")))

    assert types["body"] == "Union[Iterable[Any], str, int, float, None]"


def test_a_key_that_is_also_a_condition_keeps_the_first_read():
    tree = div(Slot.if_("mode", span("a"), span("b")), Slot.value("mode"))

    # The condition is read first and wins, so the two uses do not disagree.
    assert ScopeTypes.of(tree)["mode"] == "Any"


def test_a_name_the_view_owns_reads_the_data_offsets():
    # `out` is the view's own accumulator and `data` its own mapping, so neither
    # can be a parameter; both read the mapping instead.
    tree = div(Slot.value("out"), Slot.value("data"))

    signature = ScopeTypes.signature(tree)

    assert "out:" not in signature
    assert "data: Optional[Dict[str, Any]] = None" in signature
    assert _run_view(tree, data={"out": "O", "data": "D"}) == "<div>OD</div>"


def test_a_static_tree_has_no_docblock():
    assert ScopeTypes.docblock(Compile.shape(div("static")).tree()) == ""
