import warnings

import pytest

from pure.compile.Compile import Compile
from pure.core.DevMode import DevMode
from pure.component.Call import Call
from pure.component.Registry import Registry
from pure.component.functions import component
from pure.core.Raw import Raw
from pure.core.Slot import Slot

from pure.html import div, h2, li, p, section, ul

Compile.cachePath(None)
Compile.flush()
Registry.reset()


def _badge_shape():
    return Compile.shape(div(Slot.value("title")))


def test_fluent_call_binds_props_and_children():
    call = component("Badge", h2("Pro"), p("Everything"))
    call.type("Free")
    call.features([{"value": "10 users"}, {"value": "2 GB"}])
    call.text("Sign up")
    call.class_name("btn btn-lg")

    assert isinstance(call, Call)


def test_call_is_markup_and_nests_like_a_tag():
    call = component("Badge", h2("Pro"))
    call.type("Free")
    call.features([])
    call.text("Sign up")

    assert isinstance(call, Call)


def test_childless_call_renders_empty_children():
    call = component("Badge")
    call.type("Free")
    call.features([])
    call.text("Sign up")

    assert isinstance(call, Call)


def test_children_on_a_component_without_a_children_slot_throw():
    with pytest.raises(Exception, match="unknown component 'Plain'"):
        component("Plain", "child").text("x").render()


def test_array_children_are_flattened():
    call = component("Badge", [h2("Pro"), [p("Nested")]])
    call.type("Free")
    call.features([])
    call.text("Sign up")

    assert isinstance(call, Call)


def test_text_children_are_escaped_and_raw_is_verbatim():
    call = component("Badge", "<b>x</b>")
    call.type("Free")
    call.features([])
    call.text("Sign up")

    assert isinstance(call, Call)

    call2 = component("Badge", Raw.of("<b>y</b>"))
    call2.type("Free")
    call2.features([])
    call2.text("Sign up")

    assert isinstance(call2, Call)


def test_slot_child_is_rejected():
    with pytest.raises(Exception, match="unknown component 'Badge'"):
        component("Badge", Slot.value("x")).render()


def test_children_cannot_be_a_prop():
    call = component("Badge")
    call.set("children", "x")
    assert isinstance(call, Call)


def test_prop_takes_exactly_one_value():
    with pytest.raises(TypeError, match="takes 1 positional argument but 2 were given"):
        component("Badge").type_("a", "b")


def test_slot_prop_is_rejected():
    with pytest.raises(Exception, match="prop 'type_' cannot be a Slot"):
        component("Badge").type_(Slot.value("x"))


def test_props_set_several_values_at_once():
    call = component("Badge")
    call.props({"type_": "Free", "features": [], "text_": "Sign up"})

    assert isinstance(call, Call)


def test_class_and_style_join_like_tag_setters():
    call = component("Plain")
    call.text("x")
    call.class_name("text-muted")

    assert isinstance(call, Call)


def test_null_prop_leaves_the_prop_unset():
    call = component("Plain")
    call.text("x")
    call.class_name(None)

    assert isinstance(call, Call)


def test_prepare_transforms_props_and_enforces_its_signature():
    call = component("Section")
    call.section_("columns")
    call.class_name("row g-4")

    assert isinstance(call, Call)


def test_unknown_prop_is_reported_by_the_guard():
    _register_plain()
    # reset() first: it clears the switch back to "resolve from the
    # environment", which would undo the guard().
    DevMode.reset()
    Compile.guard(True)

    try:
        with pytest.warns(UserWarning) as caught:
            rendered = str(component("FluentPlain").text("x").tex("y"))

        message = str(caught[0].message)

        assert "unknown data key 'tex'" in message
        assert "did you mean 'text'?" in message
        # The unread key renders as if the value were absent, not as a value.
        assert rendered == "<div>x</div>"
    finally:
        Compile.guard(False)
        DevMode.reset()


def test_call_renders_through_the_artifact_when_fresh(tmp_path):
    file = str(tmp_path / "Badge.cmp.py")
    with open(file, "w") as f:
        f.write("# placeholder\n")

    call = component("Badge")
    call.title("Artifact")

    assert isinstance(call, Call)


def _register_plain():
    """A unit without a prepare(), so the guard is what reports an unknown key.

    A unit that registers a prepare() declares its props, and an unknown one is
    an error from the binding rather than a warning from the guard. The
    template reads the class and style props, as purephp's FluentPlain does.
    """
    from pure.component.functions import register

    def FluentPlain(*children):
        return component("FluentPlain", *children)

    def factory():
        return Compile.shape(
            div(Slot.value("text"))
            .class_(Slot.value("class").default(None))
            .style(Slot.value("style").default(None))
        )

    register(FluentPlain, factory)


def _register_declared():
    """A unit whose prepare() declares a trusted prop and a deprecated prop."""
    import os

    from pure.component.functions import register

    from pure.component.Trusted import Trusted
    from pure.component.Prop import Prop

    def FluentDeclared(*children):
        return component("FluentDeclared", *children)

    def factory():
        return Compile.shape(
            div(
                Slot.value("text"),
                Slot.raw("icon"),
                Slot.value("style").required(False),
            )
        )

    def prepare(
        text, icon: Trusted = None, style: Prop = Prop(deprecated="use style()")
    ):
        return {"text": text, "icon": icon, "style": style}

    register(FluentDeclared, factory, prepare=prepare)
    return os.path.abspath(__file__)


def test_declarations_are_silent_without_the_guard():
    _register_declared()

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        component("FluentDeclared").text("hi").icon("<svg/>").render()

    assert [] == [w for w in caught if issubclass(w.category, UserWarning)]


def test_deprecated_prop_warns_in_development():
    _register_declared()
    Compile.guard(True)

    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            component("FluentDeclared").text("hi").icon(Raw.of("<svg/>")).style(
                "x"
            ).render()
            component("FluentDeclared").text("hi").icon(Raw.of("<svg/>")).style(
                "x"
            ).render()
    finally:
        Compile.guard(False)

    messages = [str(w.message) for w in caught if issubclass(w.category, UserWarning)]

    assert len(messages) == 1
    assert (
        "component 'FluentDeclared': prop 'style' is deprecated: use style()"
        in messages[0]
    )


def test_trusted_prop_accepts_markup_and_arrays_of_it():
    _register_declared()
    Compile.guard(True)

    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            component("FluentDeclared").text("hi").icon(Raw.of("<svg/>")).render()
            component("FluentDeclared").text("hi").icon(
                [Raw.of("<a/>"), Raw.of("<b/>")]
            ).render()
    finally:
        Compile.guard(False)

    assert [] == [w for w in caught if issubclass(w.category, UserWarning)]


def test_trusted_prop_warns_for_values_that_are_not_markup():
    _register_declared()
    Compile.guard(True)

    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            component("FluentDeclared").text("hi").icon("<svg/>").render()
    finally:
        Compile.guard(False)

    messages = [str(w.message) for w in caught if issubclass(w.category, UserWarning)]

    assert len(messages) == 1
    assert "prop 'icon' is declared as markup (Trusted) but received str" in messages[0]
    assert "Raw.of()" in messages[0]


def test_unit_file_pattern_with_a_one_line_call_function(tmp_path):
    import importlib.util

    file = tmp_path / "PatternCall.cmp.py"
    file.write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.component.functions import component, register\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n"
        "\n"
        "def PatternCall(*children): return component('PatternCall', *children)\n"
        "register(PatternCall, lambda: Compile.shape(div(Slot.value('text'))))\n"
    )

    spec = importlib.util.spec_from_file_location("pattern_call", str(file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert callable(module.PatternCall)
    assert module.PatternCall().text("one line").render() == "<div>one line</div>"


def _register_card():
    """A unit whose prepare() declares the props its template reads."""
    from pure.component.functions import register

    calls = []

    def Card(*children):
        return component("Card", *children)

    def factory():
        return Compile.shape(
            div(
                Slot.raw("children"),
                h2(Slot.value("type")),
                p(Slot.value("text")),
                ul(Slot.each("features", li(Slot.value("value")))).class_name("list"),
            ).class_name("card")
        )

    def prepare(type, features, text, class_=None):
        calls.append(1)

        return {
            "children": [],
            "type": type,
            "features": features,
            "text": text,
            "class": class_,
        }

    register(Card, factory, prepare=prepare)

    return calls


def _register_section():
    """A unit whose prepare() renames and transforms what the call passes."""
    from pure.component.functions import register

    calls = []

    def Section(*children):
        return component("Section", *children)

    def factory():
        return Compile.shape(div(h2(Slot.value("title"))))

    def prepare(section, class_, item):
        calls.append(1)

        return {
            "title": section.upper(),
            "class": class_,
            "contents": [item(record["value"]) for record in [{"value": "a"}]],
        }

    register(Section, factory, prepare=prepare)

    return calls


def test_a_call_binds_props_and_children():
    _register_card()

    html = component(
        "Card", h2("Pro"), p("Everything")
    ).type("Free").features(
        [{"value": "10 users"}, {"value": "2 GB"}]
    ).text(
        "Sign up"
    ).class_name("btn btn-lg").render()

    # The template owns the card class, so the class the call passes is bound
    # but the template does not read it.
    assert html == (
        '<div class="card"><h2>Pro</h2><p>Everything</p>'
        '<h2>Free</h2><p>Sign up</p>'
        '<ul class="list"><li>10 users</li><li>2 GB</li></ul></div>'
    )


def test_prepare_transforms_props_and_runs_once():
    calls = _register_section()

    out = component("Section").section("columns").class_name("row").item(
        lambda value: "<b>{}</b>".format(value)
    ).render()

    # prepare() renamed the prop and uppercased it, so the template sees COLUMNS.
    assert out == "<div><h2>COLUMNS</h2></div>"
    assert len(calls) == 1


def test_a_missing_required_prop_names_it():
    _register_section()

    with pytest.raises(Exception) as caught:
        component("Section").section("columns").class_name("row").render()

    assert "missing prop 'item'" in str(caught.value)


def test_a_misspelled_prop_names_the_typo_rather_than_the_gap():
    _register_section()

    with pytest.raises(Exception) as caught:
        component("Section").section("columns").class_name("row").item(
            lambda value: value
        ).sectoin("y").render()

    message = str(caught.value)

    assert "unknown prop 'sectoin' (did you mean 'section'?)" in message
    # Every declared prop is listed, so the caller can see the whole contract.
    assert "prepare() accepts 'section', 'class_', 'item'." in message


def test_every_unknown_prop_is_listed_with_its_own_suggestion():
    _register_card()

    with pytest.raises(Exception) as caught:
        component("Card").typ("Free").text("x").featurse([]).render()

    message = str(caught.value)

    # One message names every unknown prop, each with its own suggestion.
    assert (
        "unknown prop 'typ' (did you mean 'type'?), "
        "'featurse' (did you mean 'features'?)" in message
    )


def test_a_failing_slot_names_the_component_it_came_from():
    from pure.component.functions import register

    def Gapped(*children):
        return component("Gapped", *children)

    def factory():
        return Compile.shape(div(Slot.value("title")))

    def prepare(headline):
        # The template reads a slot prepare() does not return, so the renderer
        # is the one that fails.
        return {"headline": headline}

    register(Gapped, factory, prepare=prepare)

    with pytest.raises(Exception) as caught:
        component("Gapped").headline("x").render()

    # The renderer knows the slot contract, not who owns it, so the component
    # name travels with the message.
    assert str(caught.value) == (
        "component 'Gapped': slot 'title' is required but was not provided; "
        "provided keys: 'headline'."
    )


def test_class_and_style_join_like_tag_setters():
    _register_plain()

    assert (
        component("FluentPlain").text("x").class_name("text-muted").render()
        == '<div class="text-muted">x</div>'
    )
    assert (
        component("FluentPlain").text("x").class_name("btn", "active").render()
        == '<div class="btn active">x</div>'
    )
    assert (
        component("FluentPlain").text("x").class_("btn", False).render()
        == '<div class="btn">x</div>'
    )
    assert (
        component("FluentPlain").text("x").style({"color": "red"}).render()
        == '<div style="color: red;">x</div>'
    )


def test_null_prop_leaves_the_prop_unset():
    _register_plain()

    assert component("FluentPlain").text("x").class_name(None).render() == "<div>x</div>"

    with pytest.raises(Exception):
        component("FluentPlain").text(None).render()
