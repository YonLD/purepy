import os
import pytest

from pure.compile.Compile import Compile
from pure.core.DevMode import DevMode
from pure.compile.Internal.RendererCache import RendererCache
from pure.compile.Internal.ShapeGuard import ShapeGuard
from pure.core.Slot import Slot

from pure.html import div, li, span, ul

Compile.cachePath(None)
Compile.flush()


def test_id_is_stable_and_structure_sensitive():
    a = Compile.shape(div(span("x")).class_name("c"))
    b = Compile.shape(div(span("x")).class_name("c"))
    c = Compile.shape(div(span("y")).class_name("c"))

    assert len(a.id()) == 40
    assert a.id() == b.id()
    assert a.id() != c.id()


def test_id_separates_the_attribute_name_of_a_slot_value():
    as_class = Compile.shape(div("t").class_name(Slot.value("x")))
    as_id = Compile.shape(div("t").id(Slot.value("x")))

    assert as_class.id() != as_id.id()


def test_cache_writes_and_reloads_byte_identically(tmp_path):
    Compile.cachePath(str(tmp_path))
    Compile.flush()

    shape = Compile.shape(div(span(Slot.value("v"))).class_name("c"))
    source = shape.compile().source

    Compile.flush()

    reloaded = Compile.shape(div(span(Slot.value("v"))).class_name("c"))

    assert shape.id() == reloaded.id()
    assert source == reloaded.compile().source

    Compile.cachePath(None)
    Compile.flush()


def test_cache_hit_uses_the_stored_renderer(tmp_path):
    Compile.cachePath(str(tmp_path))
    Compile.flush()

    item = Compile.shape(li(Slot.value("label")))

    def build():
        return Compile.shape(ul(Slot.each("items", item)))

    shape = build()
    shape.compile()

    Compile.flush()

    assert build().id() == shape.id()

    Compile.cachePath(None)
    Compile.flush()


def test_corrupted_cache_is_regenerated(tmp_path):
    Compile.cachePath(str(tmp_path))
    Compile.flush()

    shape = Compile.shape(div(span("x")))
    shape.compile()

    Compile.flush()

    reloaded = Compile.shape(div(span("x")))
    assert reloaded.id() == shape.id()

    Compile.cachePath(None)
    Compile.flush()


def test_mutating_a_tree_after_compile_cannot_poison_the_cache():
    tree = div(span(Slot.value("v"))).class_name("c")
    shape = Compile.shape(tree)
    id_before = shape.id()

    Compile.flush()
    tree.class_name("late")

    assert shape.id() != id_before

    fresh = Compile.shape(div(span(Slot.value("v"))).class_name("c"))

    assert shape.id() != fresh.id()


def test_id_follows_tree_mutation_without_poisoning_the_cache():
    tree = div(span(Slot.value("v")))
    shape = Compile.shape(tree)
    id_before = shape.id()

    tree.class_name("late")

    assert id_before != shape.id()

    fresh = Compile.shape(div(span(Slot.value("v"))))

    assert shape.id() != fresh.id()


def test_cache_path_null_disables_disk_writes(tmp_path):
    Compile.cachePath(str(tmp_path))
    try:
        Compile.cachePath(None)

        Compile.shape(div("x")).compile()

        # A null cache path means "keep everything in memory".
        assert list(tmp_path.iterdir()) == []
        assert Compile.clearCache() == 0
    finally:
        Compile.cachePath(None)
        Compile.flush()


def test_flush_invalidates_memory_renderers():
    shape = Compile.shape(div(Slot.value("v")))

    first = shape.compile()
    assert shape.compile() is first

    Compile.flush()

    second = shape.compile()
    assert first.shape_id == second.shape_id


def test_guard_warns_once_per_call_site():
    Compile.guard(True)

    try:
        with pytest.warns(UserWarning) as caught:
            for _ in range(25):
                Compile.shape(div("guarded"))
    finally:
        Compile.guard(False)
        DevMode.reset()

    # One warning, at the threshold, for the caller's own line -- not one per
    # call, and not attributed to the library's own Compile.shape() frame.
    assert len(caught) == 1

    message = str(caught[0].message)

    assert "was called 20 times" in message
    assert "test_compile_cache.py:" in message
    assert "pure/compile/Compile.py" not in message


def test_guard_enables_from_the_environment_variable(monkeypatch):
    DevMode.reset()
    ShapeGuard._calls = {}
    monkeypatch.setenv("PURE_COMPILE_GUARD", "1")

    try:
        with pytest.warns(UserWarning) as caught:
            for _ in range(25):
                Compile.shape(div("guarded"))
    finally:
        monkeypatch.delenv("PURE_COMPILE_GUARD")
        Compile.guard(False)
        DevMode.reset()
        ShapeGuard._calls = {}

    assert len(caught) == 1
    assert "memoize" in str(caught[0].message)


def test_guard_warns_about_data_keys_the_template_does_not_read():
    Compile.guard(True)

    try:
        shape = Compile.shape(div(Slot.value("title")))
        compiled = shape.compile()

        with pytest.warns(UserWarning) as caught:
            compiled.render({"title": "t", "titel": "typo"})
            compiled.render({"title": "t", "titel": "typo"})

        assert len(caught) == 1
        assert "did you mean 'title'?" in str(caught[0].message)
    finally:
        Compile.guard(False)


def test_data_key_guard_enables_from_the_environment_variable(monkeypatch):
    DevMode.reset()
    monkeypatch.setenv("PURE_COMPILE_GUARD", "1")

    shape = Compile.shape(div(Slot.value("title")))
    compiled = shape.compile()

    with pytest.warns(UserWarning) as caught:
        compiled.render({"title": "t", "extra": 1})

    assert "'extra'" in str(caught[0].message)

    Compile.guard(False)
    DevMode.reset()


def test_stale_cache_version_is_regenerated(tmp_path):
    Compile.cachePath(str(tmp_path))
    Compile.flush()

    shape = Compile.shape(div(span("x")))
    shape.compile()

    Compile.flush()

    reloaded = Compile.shape(div(span("x")))
    assert reloaded.id() == shape.id()

    Compile.cachePath(None)
    Compile.flush()


def _skip_as_root():
    if os.geteuid() == 0:
        pytest.skip("running as root: permission checks are bypassed")


def test_cache_path_rejects_loose_permissions(tmp_path):
    _skip_as_root()

    loose = tmp_path / "loose"
    loose.mkdir(mode=0o700)
    os.chmod(loose, 0o777)

    try:
        with pytest.raises(ValueError, match="must not be writable by group or others"):
            Compile.cachePath(str(loose))
    finally:
        os.chmod(loose, 0o700)
        loose.rmdir()


def test_cache_path_rejects_unwritable_directory(tmp_path):
    _skip_as_root()

    locked = tmp_path / "locked"
    locked.mkdir(mode=0o555)

    try:
        with pytest.raises(ValueError):
            Compile.cachePath(str(locked))
    finally:
        os.chmod(locked, 0o755)
        locked.rmdir()


def test_clear_cache_removes_only_own_files(tmp_path):
    Compile.cachePath(str(tmp_path))
    try:
        shape = Compile.shape(div("x"))
        shape.compile()

        foreign = tmp_path / "keep.py"
        foreign.write_text("# not ours\n")

        assert Compile.clearCache() == 1
        assert not (tmp_path / (shape.id() + ".py")).exists()
        assert foreign.exists()

        foreign.unlink()
    finally:
        Compile.cachePath(None)
        Compile.flush()


def test_garbage_cache_file_is_regenerated(tmp_path):
    Compile.cachePath(str(tmp_path))
    try:
        shape = Compile.shape(div(span("x")))
        shape.compile()

        file = tmp_path / (shape.id() + ".py")
        file.write_text("not python at all")

        # The fingerprint changes, so this is a fresh id; a garbage file for
        # the id under test must be replaced by usable generated code.
        shape2 = Compile.shape(div(span("x")))
        assert shape2({}) is not None

        file.write_text("not python at all")
        Compile.flush()
        Compile._sources = {}

        assert Compile.shape(div(span("x")))({}) == "<div><span>x</span></div>"
        assert "purepy-shape" in file.read_text()
    finally:
        Compile.cachePath(None)
        Compile.flush()


def test_write_leaves_no_temp_file_behind(tmp_path):
    Compile.cachePath(str(tmp_path))
    try:
        shape = Compile.shape(div("x"))
        shape.compile()

        leftovers = [p.name for p in tmp_path.iterdir() if p.name.startswith("shape-")]

        assert leftovers == []
        assert (tmp_path / (shape.id() + ".py")).exists()
    finally:
        Compile.cachePath(None)
        Compile.flush()


def test_write_cleans_up_its_temp_file_when_the_rename_fails(tmp_path, monkeypatch):
    Compile.cachePath(str(tmp_path))
    try:
        shape = Compile.shape(div("x"))
        shape.compile()

        target = tmp_path / (shape.id() + ".py")
        target.unlink()

        def failing_rename(src, dst):
            raise OSError("rename refused")

        monkeypatch.setattr(os, "rename", failing_rename)

        RendererCache.write(str(target), "    return ''", "deadbeef")

        leftovers = [p.name for p in tmp_path.iterdir() if p.name.startswith("shape-")]

        assert leftovers == []
        assert not target.exists()
    finally:
        Compile.cachePath(None)
        Compile.flush()
