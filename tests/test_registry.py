import pytest

from pure.compile.Compile import Compile
from pure.component.functions import component, register
from pure.component.Registry import Registry
from pure.core.Slot import Slot

from pure.html import body, div, html, span

Compile.cachePath(None)
Compile.flush()
Registry.reset()


@pytest.fixture(autouse=True)
def _reset():
    Compile.cachePath(None)
    Compile.flush()
    Registry.reset()
    yield
    Registry.reset()
    Compile.flush()


def _badge_shape():
    return Compile.shape(span(Slot.value("label")))


def test_shape_file_returning_a_bare_tag_tree_is_wrapped(tmp_path):
    file = tmp_path / "bare.shape.py"
    file.write_text(
        "from pure.html import span\n"
        "from pure.core.Slot import Slot\n"
        "shape = span(Slot.value('label'))\n"
    )

    assert file.exists()


def test_factory_is_lazy_when_the_artifact_is_fresh(tmp_path):
    calls = []

    def Badge(*children):
        return component("Badge", *children)

    def factory():
        calls.append(1)
        return _badge_shape()

    register(Badge, factory)

    file = tmp_path / "Badge.cmp.py"
    file.write_text("# placeholder\n")
    Compile.flush()

    assert "Badge" in Registry.names()
    assert len(calls) == 0


def test_factory_runs_once_per_generation_without_an_artifact():
    calls = []

    def Badge(*children):
        return component("Badge", *children)

    def factory():
        calls.append(1)
        return _badge_shape()

    register(Badge, factory)

    assert "Badge" in Registry.names()

    Compile.flush()

    assert "Badge" in Registry.names()


def test_factory_must_return_a_shape():
    def Badge(*children):
        return component("Badge", *children)

    def factory():
        return "not a shape"

    register(Badge, factory)

    with pytest.raises(Exception):
        Registry.component("Badge")


def test_one_file_registers_one_unit(tmp_path):
    first = tmp_path / "Badge.cmp.py"
    first.write_text("# placeholder\n")

    Registry.register("BadgeA", str(first), lambda: _badge_shape())

    with pytest.raises(Exception, match="a unit file registers one component"):
        Registry.register("BadgeB", str(first), lambda: _badge_shape())


def test_unknown_name_lists_known_components():
    def Badge(*children):
        return component("Badge", *children)

    def factory():
        return _badge_shape()

    register(Badge, factory)

    with pytest.raises(Exception, match="unknown component 'Nope'"):
        Registry.component("Nope")


def test_unknown_name_without_registrations():
    with pytest.raises(Exception, match="unknown component 'Nope'"):
        Registry.component("Nope")


def test_units_for_reports_the_units_of_a_file(tmp_path):
    badge_file = tmp_path / "Badge.cmp.py"
    badge_file.write_text("# placeholder\n")
    page_file = tmp_path / "Page.cmp.py"
    page_file.write_text("# placeholder\n")

    Registry.register("Badge", str(badge_file), lambda: _badge_shape())
    Registry.register("Page", str(page_file), lambda: Compile.shape(html(body())))

    units = Registry.unitsFor(str(badge_file))
    assert "Badge" in units
    assert "factory" in units["Badge"]


def test_reset_clears_registrations():
    def Badge(*children):
        return component("Badge", *children)

    def factory():
        return _badge_shape()

    register(Badge, factory)

    Registry.reset()

    with pytest.raises(Exception, match="unknown component 'Badge'"):
        Registry.component("Badge")


def test_bare_shape_path_still_renders(tmp_path):
    file = tmp_path / "bare-page.shape.py"
    file.write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n"
        "shape = Compile.shape(div(Slot.value('title')))\n"
    )

    assert file.exists()


def test_an_unregistered_unit_path_is_not_loaded_as_a_template(tmp_path):
    file = tmp_path / "Loose.cmp.py"
    file.write_text("# placeholder\n")

    with pytest.raises(Exception):
        Registry.component(str(file))


def test_a_path_like_typo_lists_known_components():
    def Badge(*children):
        return component("Badge", *children)

    def factory():
        return _badge_shape()

    register(Badge, factory)

    with pytest.raises(Exception):
        Registry.component("ui/Bdge")


def test_an_empty_name_is_rejected(tmp_path):
    file = tmp_path / "Badge.cmp.py"
    file.write_text("# placeholder\n")

    with pytest.raises(Exception, match="component name must not be empty"):
        Registry.register("", str(file), lambda: _badge_shape())


def test_a_unit_file_must_exist(tmp_path):
    missing = str(tmp_path / "Missing.cmp.py")

    with pytest.raises(Exception, match="unit file '.*' does not exist"):
        Registry.register("BadgeMissing", missing, lambda: _badge_shape())


def render_unit(name_or_path, data=None):
    """Render a registered component, by name or by unit file path."""
    return Registry.component(name_or_path)(data if data is not None else {})


def test_renders_a_registered_component_by_name():
    def Badge(*children):
        return component("Badge", *children)

    register(Badge, lambda: _badge_shape())

    assert "<span>x</span>" == render_unit("Badge", {"label": "x"})
    assert "<span>y</span>" == render_unit("Badge", {"label": "y"})


def test_factory_returning_a_bare_tag_tree_is_wrapped():
    def Bare(*children):
        return component("Bare", *children)

    register(Bare, lambda: span(Slot.value("label")))

    assert "<span>x</span>" == render_unit("Bare", {"label": "x"})


def test_name_and_path_resolve_to_the_same_binder():
    import os

    def Same(*children):
        return component("Same", *children)

    register(Same, lambda: _badge_shape())
    file = os.path.realpath(__file__)

    assert Registry.component("Same") is Registry.component(file)
    assert "<span>x</span>" == render_unit(file, {"label": "x"})


def test_registering_the_same_name_for_the_same_file_is_idempotent():
    def Idem(*children):
        return component("Idem", *children)

    register(idem := Idem, lambda: _badge_shape())
    register(idem, lambda: _badge_shape())

    assert "<span>x</span>" == render_unit("Idem", {"label": "x"})


def test_duplicate_name_throws_unless_overridden(tmp_path):
    first = tmp_path / "first.cmp.py"
    first.write_text("# first\n")
    second = tmp_path / "second.cmp.py"
    second.write_text("# second\n")

    Registry.register("Dup", str(first), lambda: _badge_shape())

    with pytest.raises(Exception, match="already registered by"):
        Registry.register("Dup", str(second), lambda: _badge_shape())

    Registry.register(
        "Dup", str(second), lambda: div(Slot.value("label")), override=True
    )

    assert "<div>override</div>" == render_unit("Dup", {"label": "override"})
    assert {} == Registry.unitsFor(str(first))


def test_override_reaps_the_name_that_owned_the_file(tmp_path):
    file = tmp_path / "owned.cmp.py"
    file.write_text("# owned\n")
    other = tmp_path / "other.cmp.py"
    other.write_text("# other\n")

    Registry.register("First", str(file), lambda: _badge_shape())
    Registry.register("Second", str(file), lambda: _badge_shape(), override=True)

    # One file registers one unit, so the second name reaps the first.
    assert ["Second"] == Registry.names()
    assert ["Second"] == list(Registry.unitsFor(str(file)))
    assert "<span>x</span>" == render_unit("Second", {"label": "x"})

    with pytest.raises(Exception, match="unknown component 'First'"):
        render_unit("First", {})


def test_render_does_not_prepend_the_document_header():
    def Doc(*children):
        return component("Doc", *children)

    register(Doc, lambda: html(body("a")))

    body_out = render_unit("Doc", {})

    assert "<html><body>a</body></html>" == body_out
    assert "<!DOCTYPE html><html><body>a</body></html>" == "<!DOCTYPE html>" + body_out


def test_an_artifact_of_the_same_second_serves_the_unit(tmp_path):
    import os

    file = tmp_path / "cached.cmp.py"
    file.write_text("# cached\n")

    calls = []

    def factory():
        calls.append(1)
        return _badge_shape()

    Registry.register("Cached", str(file), factory)
    Compile.cachePath(str(tmp_path))

    try:
        # Build the unit artifact, the file the registry looks for.
        from pure.compile.Internal.ArtifactCompiler import ArtifactCompiler

        ArtifactCompiler.writeUnit(str(file), _badge_shape(), False)
        calls.clear()

        assert "<span>x</span>" == render_unit("Cached", {"label": "x"})
        assert 0 == len(calls)
    finally:
        Compile.cachePath(None)
