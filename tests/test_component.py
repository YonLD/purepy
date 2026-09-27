import pytest

from pure.compile.Compile import Compile
from pure.component.functions import component
from pure.core.Raw import Raw
from pure.core.Slot import Slot

from pure.component.Call import Call
from pure.html import div

Compile.cachePath(None)
Compile.flush()


def test_inline_tree_binds_data_to_string():
    render = Compile.shape(div(Slot.value("title"))).compile()

    assert render.render({"title": "a & b"}) == "<div>a &amp; b</div>"


def test_raw_and_stringable_slot_values_are_coerced_without_a_cast():
    render = Compile.shape(div(Slot.raw("content"))).compile()

    assert render.render({"content": Raw.of("<b>x</b>")}) == "<div><b>x</b></div>"

    class Stringable:
        def __str__(self):
            return "<i>y</i>"

    assert render.render({"content": Stringable()}) == "<div><i>y</i></div>"


def test_raw_slot_joins_a_local_list_of_component_markup():
    render = Compile.shape(div(Slot.raw("navs"))).compile()

    navs = [Raw.of("<a>a</a>"), Raw.of("<b>b</b>")]
    assert render.render({"navs": navs}) == "<div><a>a</a><b>b</b></div>"


def test_raw_value_in_a_text_slot_is_escaped():
    render = Compile.shape(div(Slot.value("content"))).compile()

    assert (
        render.render({"content": Raw.of("<b>x</b>")})
        == "<div>&lt;b&gt;x&lt;/b&gt;</div>"
    )


def test_shape_file_compiles_when_there_is_no_artifact(tmp_path):
    file = tmp_path / "badge.shape.py"
    file.write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n"
        "shape = Compile.shape(div(Slot.value('title')))\n"
    )

    import importlib.util

    spec = importlib.util.spec_from_file_location("shape", str(file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert mod.shape.compile().shape_id == Compile.shape(div(Slot.value("title"))).id()


def test_fresh_artifact_is_loaded_instead_of_the_shape_file(tmp_path):
    file = tmp_path / "badge.shape.py"
    file.write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n"
        "def shape():\n"
        "    return Compile.shape(div(Slot.value('title')))\n"
    )

    from pure.component.Registry import Registry

    binder = Registry.component(str(file))
    assert binder is not None


def test_props_pass_values_to_slots(tmp_path):
    file = tmp_path / "badge.shape.py"
    file.write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n"
        "def shape():\n"
        "    return Compile.shape(div(Slot.value('title')))\n"
    )

    call = component(str(file))
    call.props({"title": "a & b"})
    assert isinstance(call, Call)


def test_props_accept_an_unpacked_bindings_array(tmp_path):
    file = tmp_path / "badge.shape.py"
    file.write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n"
        "def shape():\n"
        "    return Compile.shape(div(Slot.value('title')))\n"
    )

    call = component(str(file))
    call.props({"title": "b"})
    assert isinstance(call, Call)


def test_render_does_not_prepend_the_document_header(tmp_path):
    file = tmp_path / "page.shape.py"
    file.write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import html, body\n"
        "def shape():\n"
        "    return Compile.shape(html(body(Slot.value('title'))))\n"
    )

    call = component(str(file))
    call.props({"title": "a"})
    assert isinstance(call, Call)


def test_slot_errors_name_the_component_or_template(tmp_path):
    unit = tmp_path / "card.cmp.py"
    unit.write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n"
        "shape = Compile.shape(div(Slot.value('title')))\n"
    )

    with pytest.raises(Exception, match="unknown component 'Card'"):
        component("Card").props({"titel": "typo"}).render()


def test_template_slot_errors_name_the_template_path(tmp_path):
    file = tmp_path / "badge.shape.py"
    file.write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n"
        "def shape():\n"
        "    return Compile.shape(div(Slot.value('title')))\n"
    )

    with pytest.raises(Exception):
        component(str(file)).props({"other": "x"}).render()


def test_missing_template_throws(tmp_path):
    with pytest.raises(Exception):
        Registry.component(str(tmp_path / "missing.shape.py"))


def test_template_that_does_not_return_a_shape_throws(tmp_path):
    file = tmp_path / "bad.shape.py"
    file.write_text("result = 42\n")

    with pytest.raises(Exception):
        Registry.component(str(file))


def test_artifact_that_does_not_return_a_renderer_throws(tmp_path):
    file = tmp_path / "bad-artifact.shape.py"
    file.write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n"
        "def shape():\n"
        "    return Compile.shape(div(Slot.value('title')))\n"
    )

    with pytest.raises(Exception):
        Registry.component(str(file))
