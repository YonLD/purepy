import importlib.util
import io
import os
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

from pure.compile.Compile import Compile
from pure.compile.Internal.ArtifactCommand import ArtifactCommand
from pure.compile.Internal.ArtifactCompiler import ArtifactCompiler
from pure.compile.Internal.CodeGenerator import CodeGenerator
from pure.compile.Internal.PlainGenerator import PlainGenerator
from pure.compile.Internal.RootSlots import RootSlots
from pure.compile.Internal.ShapeIndex import ShapeIndex
from pure.component.Registry import Registry
from pure.compile.Template import Template
from pure.core.Raw import Raw
from pure.core.Slot import Slot

from pure.html import body, div, em, h1, h2, html, li, p, span, ul

Compile.cachePath(None)
Compile.flush()

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _flat_renderer(tree):
    index = ShapeIndex.of(tree)
    slots = RootSlots.of(tree)
    return CodeGenerator.compile(tree, index, slots)


def _run(argv, units=None):
    """Run an ArtifactCommand over in-memory streams and capture the result."""
    stdout, stderr = io.StringIO(), io.StringIO()

    code = ArtifactCommand(units).run(argv, stdout, stderr)

    return {"code": code, "stdout": stdout.getvalue(), "stderr": stderr.getvalue()}


def _registry_units(file):
    return Registry.unitsFor(file)


def _load(file, name="artifact"):
    """Import a generated file and hand back the module."""
    spec = importlib.util.spec_from_file_location("purepy_" + name, str(file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def _render_plain(file, data=None):
    """Execute a generated plain view and return what it printed."""
    namespace = {}
    exec(Path(file).read_text(), namespace)
    view = namespace["view"]

    return view(**(data or {}))


def _shape_file(tmp_path, name, code):
    path = tmp_path / name
    path.write_text(code)

    return str(path)


def _unit_file(tmp_path, name, register=""):
    """Write a *.cmp.py unit, optionally with a registration body.

    The generated component name carries a per-call suffix so two fixtures never
    declare the same function in one process.
    """
    path = tmp_path / name

    if register == "auto":
        component = "U" + uuid.uuid4().hex[:6]
        register = (
            "def {0}(*children):\n"
            "    return component('{0}', *children)\n\n"
            "register({0}, lambda: Compile.shape(span(Slot.value('label'))))\n"
        ).format(component)

    path.write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.compile.Template import Template\n"
        "from pure.core.Slot import Slot\n"
        "from pure.component import component, register\n"
        "from pure.html import span\n\n\n" + register
    )

    return str(path)


def test_compiles_shape_files_into_standalone_renderers():
    tree = div(h2(Slot.value("title"))).class_name("card")
    shape = Compile.shape(tree)
    renderer = shape.compile()

    assert shape.id() == renderer.shape_id
    assert "data.get" in renderer.source


def test_compiles_a_shape_file_returning_a_bare_tag_tree():
    tree = div(Slot.value("v"))
    shape = Compile.shape(tree)
    renderer = shape.compile()

    assert "data.get" in renderer.source


def test_artifact_contents_are_deterministic():
    tree = div(Slot.value("v"))
    shape = Compile.shape(tree)
    first = shape.compile().source
    second = Compile.shape(div(Slot.value("v"))).compile().source

    assert first == second


def test_template_artifacts_render_like_the_flat_source():
    item = Compile.shape(
        li(Slot.value("label")).class_name(Slot.value("class")).id(Slot.value("v1"))
    )

    tree = (
        div(
            h1(Slot.value("title")),
            p(Slot.raw("body")),
            Slot.value("subtitle"),
            Slot.if_("flag", span("on"), span("off")),
            ul(Slot.each("items", item)),
        )
        .class_name(Slot.value("cardClass"))
        .title(Slot.value("tip"))
    )

    shape = Compile.shape(tree)
    flat = _flat_renderer(shape.tree())

    data = {
        "title": "T",
        "body": "<b>b</b>",
        "subtitle": "S",
        "flag": True,
        "items": [{"label": "#1", "class": "c", "v1": "i1"}],
        "cardClass": "card",
        "tip": "tip",
    }

    assert flat.render(data) == Compile.shape(tree).compile().render(data)


def test_artifact_slots_fall_back_to_the_slow_paths_like_the_flat_renderer():
    tree = div(
        Slot.value("title"),
        Slot.raw("body"),
        Slot.child("meta", Compile.shape(ul(li(Slot.value("label"))))),
        Slot.if_("flag", span("on"), span("off")),
        ul(Slot.each("items", Compile.shape(li(Slot.value("label"))))),
    )

    shape = Compile.shape(tree)
    flat = _flat_renderer(shape.tree())
    compiled = shape.compile()

    cases = [
        {
            "title": "T",
            "body": "<b>b</b>",
            "meta": {"label": "m"},
            "flag": True,
            "items": [{"label": "i"}],
        },
        {
            "title": "T",
            "body": ["<b>1</b>", "<i>2</i>"],
            "meta": {"label": "m"},
            "flag": False,
            "items": [{"label": "i"}],
        },
        {"title": "T", "body": "", "meta": {"label": ""}, "flag": None, "items": []},
    ]

    for data in cases:
        assert compiled.render(data) == flat.render(data)


def test_plain_views_are_dependency_free_and_render_identically():
    item = Compile.shape(
        li(Slot.value("label")).class_name(Slot.value("class")).id(Slot.value("v1"))
    )

    tree = (
        div(
            h1(Slot.value("title")),
            p(Slot.raw("body")),
            Slot.value("subtitle"),
            Slot.if_("flag", span("on"), span("off")),
            ul(Slot.each("items", item)),
        )
        .class_name(Slot.value("cardClass"))
        .title(Slot.value("tip"))
    )

    shape = Compile.shape(tree)
    flat = _flat_renderer(shape.tree())
    plain = PlainGenerator.view(shape.tree())

    data = {
        "title": "T",
        "body": "<b>b</b>",
        "subtitle": "S",
        "flag": True,
        "items": [{"label": "#1", "class": "c", "v1": "i1"}],
        "cardClass": "card",
        "tip": "tip",
    }

    namespace = {}
    exec(plain, namespace)

    assert namespace["view"](**data) == flat.render(data)

    # A plain view is stand-alone: it imports nothing from the library.
    body = plain[plain.index("def view") :]
    assert "_text(" in body or "_attr(" in body or "_raw(" in body


def test_plain_views_join_a_traversable_raw_slot():
    def gen():
        yield "<b>a</b>"
        yield Raw.of("<i>b</i>")

    tree = div(Slot.raw("items"))
    plain = PlainGenerator.view(Compile.shape(tree).tree())

    assert "items" in plain[plain.index("def view") :].split("\n")[0]

    namespace = {}
    exec(plain, namespace)

    assert namespace["view"](items=gen()) == "<div><b>a</b><i>b</i></div>"


def test_plain_views_declare_root_slots_with_types_derived_from_the_shape():
    tree = div(
        Slot.value("title"),
        Slot.raw("body"),
        Slot.if_("flag", span("on")),
        ul(Slot.each("items", Compile.shape(li(Slot.value("label"))))),
    )

    plain = PlainGenerator.view(Compile.shape(tree).tree())
    signature = plain[plain.index("def view") :].split("\n")[0]

    assert "title" in signature
    assert "flag" in signature
    assert "items" in signature

    namespace = {}
    exec(plain, namespace)

    # Types come from the shape, so the view enforces them as annotations.
    assert "title" in namespace["view"].__annotations__


def test_plain_views_handle_child_and_each_slots():
    item = Compile.shape(li(Slot.value("value")))
    list_shape = Compile.shape(ul(Slot.each("items", item)))

    tree = div(Slot.child("meta", list_shape))
    plain = PlainGenerator.view(Compile.shape(tree).tree())

    assert "meta" in plain[plain.index("def view") :]

    namespace = {}
    exec(plain, namespace)

    rendered = namespace["view"](meta={"items": [{"value": "a"}, {"value": "b"}]})

    assert rendered == "<div><ul><li>a</li><li>b</li></ul></div>"


def test_plain_views_fall_back_to_data_offsets_for_odd_slot_names():
    tree = div(
        Slot.value("user-name"),
        Slot.value("data"),
        Slot.value("v1"),
    )

    plain = PlainGenerator.view(Compile.shape(tree).tree())

    # A name that is not a plain identifier cannot be a parameter, so it stays
    # an offset of the view data.
    assert "(data or {}).get('user-name')" in plain
    assert "(data or {}).get('v1')" in plain

    namespace = {}
    exec(plain, namespace)

    assert (
        namespace["view"](data={"user-name": "u", "data": "d", "v1": "x"})
        == "<div>udx</div>"
    )


def test_plain_views_of_static_shapes_keep_a_single_output_block():
    shape = Compile.shape(div("static & <raw>"))

    plain = PlainGenerator.view(shape.tree())
    body = plain[plain.index("def view") :]

    # A static shape has no slots, so the view takes no arguments and needs no
    # control flow, and the whole subtree folds into one literal.
    assert "def view() -> str:" in body
    assert " for " not in body
    assert "if " not in body
    # One append for the whole folded subtree, and no other statement.
    assert body.count("out.append(") == 1
    assert "out.append('<div>static &amp; &lt;raw&gt;</div>')" in body

    namespace = {}
    exec(plain, namespace)

    assert namespace["view"]() == "<div>static &amp; &lt;raw&gt;</div>"


def test_plain_views_keep_the_document_header_of_document_roots_only():
    cases = [
        (div("x"), ""),
        (html(body("x")), "<!DOCTYPE html>"),
    ]

    for tree, header in cases:
        plain = PlainGenerator.view(Compile.shape(tree).tree())

        namespace = {}
        exec(plain, namespace)

        assert namespace["view"]() == header + tree.render()


def test_compile_requires_at_least_one_path():
    missing = _run(["compile"])

    # A wrong command line is exit 2, distinct from a run that failed.
    assert missing["code"] == 2
    assert "needs at least one file or directory." in missing["stderr"]

    checked = _run(["compile", "--plain", "--check"])

    assert checked["code"] == 2
    assert "Usage:" in checked["stderr"]


def test_plain_paths_follow_the_shape_suffix(tmp_path):
    shape = str(tmp_path / "page.shape.py")

    assert ArtifactCompiler.artifactPath(shape) == str(tmp_path / "page.pure.py")
    assert ArtifactCompiler.plainPath(shape) == str(tmp_path / "page.plain.py")

    with pytest.raises(ValueError) as error:
        ArtifactCompiler.plainPath(str(tmp_path / "page.py"))

    assert "is not a *.shape.py or *.cmp.py file" in str(error.value)


def test_check_mode_reports_missing_and_stale_artifacts(tmp_path):
    file = _shape_file(
        tmp_path,
        "check.shape.py",
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n\n\n"
        'shape = Compile.shape(div(Slot.value("v")))\n',
    )

    missing = _run(["compile", "--check", file])

    assert missing["code"] == 1
    assert "missing:" in missing["stderr"]

    compiled = _run(["compile", "--plain", file])

    assert compiled["code"] == 0
    assert "compiled:" in compiled["stdout"]

    fresh = _run(["compile", "--check", file])

    assert fresh["code"] == 0
    assert "up to date:" in fresh["stdout"]

    (tmp_path / "check.pure.py").write_text("# stale\n")

    stale = _run(["compile", "--check", file])

    assert stale["code"] == 1
    assert "stale:" in stale["stderr"]
    assert "need recompiling" in stale["stderr"]


def test_write_changed_skips_files_that_are_already_current(tmp_path):
    file = _shape_file(
        tmp_path,
        "incremental.shape.py",
        'from pure.html import div\n\n\nshape = div("a")\n',
    )

    first = ArtifactCompiler.writeChanged(file, True)

    assert first["artifactWritten"] is True
    assert first["plainWritten"] is True

    second = ArtifactCompiler.writeChanged(file, True)

    assert second["artifactWritten"] is False
    assert second["plainWritten"] is False

    _shape_file(
        tmp_path,
        "incremental.shape.py",
        'from pure.html import div\n\n\nshape = div("changed")\n',
    )

    third = ArtifactCompiler.writeChanged(file, True)

    assert third["artifactWritten"] is True
    assert third["plainWritten"] is True

    renderer = _load(third["artifact"]).renderer

    assert renderer.render({}) == "<div>changed</div>"


def test_second_compile_run_reports_unchanged_files(tmp_path):
    file = _shape_file(
        tmp_path, "twice.shape.py", 'from pure.html import div\n\n\nshape = div("x")\n'
    )

    first = _run(["compile", file])

    assert first["code"] == 0
    assert "compiled:" in first["stdout"]

    second = _run(["compile", file])

    assert second["code"] == 0
    assert "unchanged:" in second["stdout"]
    assert "compiled:" not in second["stdout"]


def test_two_files_claiming_one_artifact_are_both_rejected(tmp_path):
    shape_file = _shape_file(
        tmp_path,
        "box.shape.py",
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n\n\n"
        'shape = Compile.shape(div(Slot.value("title")))\n',
    )
    unit = _unit_file(tmp_path, "box.cmp.py", "auto")

    result = _run(["compile", str(tmp_path)], _registry_units)

    assert result["code"] == 1
    assert "is claimed by both" in result["stderr"]
    assert shape_file in result["stderr"]
    assert unit in result["stderr"]

    # Neither file wins by discovery order: the target is left unwritten.
    assert "compiled:" not in result["stdout"]
    assert not (tmp_path / "box.pure.py").exists()


def test_artifact_of_another_cache_version_is_rejected_when_loaded(tmp_path):
    file = _shape_file(
        tmp_path,
        "guarded.shape.py",
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n\n\n"
        'shape = Compile.shape(div(Slot.value("v")))\n',
    )
    artifact = ArtifactCompiler.write(file)

    assert _load(artifact).renderer is not None

    # The guard line is what another version of the library would have left
    # behind; loading it must say `pure compile`, not fail on the signature.
    contents = Path(artifact).read_text()
    # A different digit count as well as a different value: importlib caches
    # compiled bytecode per (mtime, size), and a same-length edit would be
    # served from the .pyc of the first load.
    foreign = contents.replace(
        "if {} != Compile.CACHE_VERSION:".format(Compile.CACHE_VERSION),
        "if {} != Compile.CACHE_VERSION:".format(Compile.CACHE_VERSION + 100),
    )

    assert foreign != contents
    Path(artifact).write_text(foreign)
    importlib.invalidate_caches()

    with pytest.raises(RuntimeError) as error:
        _load(artifact, "foreign")

    assert "stale purepy artifact" in str(error.value)
    assert "run `pure compile` to rebuild" in str(error.value)


def test_compiles_unit_files_with_an_explicit_shape(tmp_path):
    unit = str(tmp_path / "badge.cmp.py")
    Path(unit).write_text("# unit placeholder: the shape is passed explicitly.\n")

    shape = Compile.shape(div(Slot.value("title")))
    written = ArtifactCompiler.writeUnit(unit, shape, True)

    assert written["artifact"] == str(tmp_path / "badge.pure.py")
    assert written["plain"] == str(tmp_path / "badge.plain.py")
    assert written["artifactWritten"] is True
    assert written["plainWritten"] is True

    renderer = _load(written["artifact"]).renderer

    assert renderer.render({"title": "a"}) == "<div>a</div>"

    again = ArtifactCompiler.writeUnit(unit, shape, True)

    assert again["artifactWritten"] is False
    assert again["plainWritten"] is False


def test_unit_artifacts_match_shape_file_artifacts(tmp_path):
    shape_file = _shape_file(
        tmp_path,
        "same.shape.py",
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n\n\n"
        'shape = Compile.shape(div(Slot.value("title")))\n',
    )
    # A distinct base name: `same.shape.py` and `same.cmp.py` would share one
    # artifact and the comparison below would read the same file twice.
    unit = str(tmp_path / "same-unit.cmp.py")
    Path(unit).write_text("# unit placeholder: the shape is passed explicitly.\n")

    from_shape_file = _load(ArtifactCompiler.write(shape_file)).renderer
    from_unit = _load(
        ArtifactCompiler.writeUnit(unit, Compile.shape(div(Slot.value("title"))))[
            "artifact"
        ]
    ).renderer

    assert from_shape_file.id == from_unit.id
    assert from_shape_file.render({"title": "a"}) == from_unit.render({"title": "a"})


def test_compiles_unit_files_through_the_command(tmp_path):
    file = _unit_file(tmp_path, "badge.cmp.py", "auto")

    compiled = _run(["compile", "--plain", file], _registry_units)

    assert compiled["code"] == 0
    assert "compiled:" in compiled["stdout"]
    assert (tmp_path / "badge.pure.py").exists()
    assert (tmp_path / "badge.plain.py").exists()

    fresh = _run(["compile", "--check", "--plain", file], _registry_units)

    assert fresh["code"] == 0
    assert "up to date:" in fresh["stdout"]

    listing = _run(["compile", "--list", file], _registry_units)

    assert listing["code"] == 0
    assert "(component)" in listing["stdout"]
    assert file in listing["stdout"]

    (tmp_path / "badge.pure.py").write_text("# stale\n")

    stale = _run(["compile", "--check", file], _registry_units)

    assert stale["code"] == 1
    assert "stale:" in stale["stderr"]


def test_unit_files_need_the_registry(tmp_path):
    file = _unit_file(tmp_path, "badge.cmp.py", "auto")

    result = _run(["compile", file])

    assert result["code"] == 1
    assert "need the component registry" in result["stderr"]


def test_unit_file_must_register_exactly_one_unit(tmp_path):
    empty = _unit_file(tmp_path, "empty.cmp.py")
    none = _run(["compile", empty], _registry_units)

    assert none["code"] == 1
    assert "no component unit is registered" in none["stderr"]

    two = str(tmp_path / "two.cmp.py")
    Path(two).write_text(
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.component import component, register\n"
        "from pure.html import span\n\n\n"
        "def One(*children):\n"
        "    return component('One', *children)\n\n\n"
        "def Two(*children):\n"
        "    return component('Two', *children)\n\n\n"
        'register(One, lambda: Compile.shape(span(Slot.value("label"))))\n'
        'register(Two, lambda: Compile.shape(span(Slot.value("label"))))\n'
    )

    many = _run(["compile", two], _registry_units)

    assert many["code"] == 1
    assert "already registered as 'One'" in many["stderr"]


def test_command_rejects_resolvers_that_return_several_units(tmp_path):
    file = _unit_file(tmp_path, "badge.cmp.py", "auto")
    shape = Compile.shape(span(Slot.value("label")))

    def resolver(path):
        return {
            "One": {"factory": lambda: shape, "document": False},
            "Two": {"factory": lambda: shape, "document": False},
        }

    result = _run(["compile", file], resolver)

    assert result["code"] == 1
    assert "2 component units are registered here" in result["stderr"]


def test_command_accepts_a_factory_returning_a_bare_tag_tree(tmp_path):
    file = _unit_file(tmp_path, "badge.cmp.py")

    def resolver(path):
        return {"Badge": {"factory": lambda: span(Slot.value("label"))}}

    result = _run(["compile", file], resolver)

    assert result["code"] == 0
    assert (tmp_path / "badge.pure.py").exists()
    assert "compiled:" in result["stdout"]

    renderer = _load(tmp_path / "badge.pure.py").renderer

    assert renderer.render({"label": "x"}) == "<span>x</span>"


def test_list_reports_shape_files(tmp_path):
    file = _shape_file(
        tmp_path, "plain.shape.py", 'from pure.html import div\n\n\nshape = div("x")\n'
    )

    listing = _run(["compile", "--list", file], _registry_units)

    assert listing["code"] == 0
    assert "{} (shape)".format(file) in listing["stdout"]


def test_list_reports_template_functions(tmp_path):
    file = _unit_file(
        tmp_path,
        "tpl.cmp.py",
        "@Template()\n"
        "def tplBadgeShape():\n"
        '    return Compile.shape(span(Slot.value("label")))\n\n\n'
        "def TplBadge(*children):\n"
        "    return component('TplBadge', *children)\n\n\n"
        "register(TplBadge, lambda: tplBadgeShape())\n",
    )

    listing = _run(["compile", "--list", file], _registry_units)

    assert listing["code"] == 0
    assert "TplBadge -> {} (component)".format(file) in listing["stdout"]
    assert "tplBadgeShape -> {} (template)".format(file) in listing["stdout"]


def test_compiles_directories_recursively(tmp_path):
    (tmp_path / "nested").mkdir()
    _shape_file(
        tmp_path, "a.shape.py", 'from pure.html import div\n\n\nshape = div("a")\n'
    )
    _shape_file(
        tmp_path,
        "nested/b.shape.py",
        'from pure.html import div\n\n\nshape = div("b")\n',
    )
    (tmp_path / "nested" / "notes.txt").write_text("ignored")

    result = _run(["compile", str(tmp_path)])

    assert result["code"] == 0
    assert (tmp_path / "a.pure.py").exists()
    assert (tmp_path / "nested" / "b.pure.py").exists()
    assert "a.shape.py" in result["stdout"]
    assert "b.shape.py" in result["stdout"]


def test_rejects_files_that_are_not_shapes(tmp_path):
    broken = _run(
        [
            "compile",
            _shape_file(tmp_path, "broken.shape.py", "shape = 42\n"),
        ]
    )

    assert broken["code"] == 1
    assert "must return a tag tree or pure.compile.Shape" in broken["stderr"]

    suffix = _run(["compile", _shape_file(tmp_path, "page.py", "shape = None\n")])

    assert suffix["code"] == 1
    assert "is not a *.shape.py or *.cmp.py file" in suffix["stderr"]

    missing = _run(["compile", str(tmp_path / "absent.shape.py")])

    assert missing["code"] == 1
    assert "does not exist" in missing["stderr"]

    usage = _run(["compile", "--nope"])

    assert usage["code"] == 2
    assert "unknown option '--nope'." in usage["stderr"]
    assert "Exit codes:" in usage["stderr"]


def test_renderer_save_writes_a_fragment_and_shape_save_prepends_the_roots_header(
    tmp_path,
):
    shape = Compile.shape(html(body("x")))

    fragment = tmp_path / "fragment.html"
    shape.compile().save(str(fragment), {})

    assert fragment.read_text() == "<html><body>x</body></html>"

    document = tmp_path / "document.html"
    shape.save(str(document), {})

    assert document.read_text() == "<!DOCTYPE html><html><body>x</body></html>"


def test_discards_output_emitted_while_the_shape_file_loads(tmp_path):
    file = _shape_file(
        tmp_path,
        "noisy.shape.py",
        "import sys\n"
        "print('chatter')\n"
        "sys.stdout.write('more chatter')\n\n"
        "from pure.html import div\n\n\n"
        'shape = div("x")\n',
    )

    artifact = ArtifactCompiler.write(file)

    assert "chatter" not in Path(artifact).read_text()
    assert _load(artifact).renderer.render({}) == "<div>x</div>"


def test_cli_binary_compiles_and_checks(tmp_path):
    file = _shape_file(
        tmp_path, "cli.shape.py", 'from pure.html import div\n\n\nshape = div("cli")\n'
    )
    binary = os.path.join(REPO_ROOT, "bin", "pure")

    help_run = subprocess.run(
        [sys.executable, binary, "--help"],
        capture_output=True,
        text=True,
    )

    assert help_run.returncode == 0
    assert "Usage:" in help_run.stdout

    compile_run = subprocess.run(
        [sys.executable, binary, "compile", file], capture_output=True, text=True
    )

    assert compile_run.returncode == 0
    assert (tmp_path / "cli.pure.py").exists()
    assert "compiled:" in compile_run.stdout

    check_run = subprocess.run(
        [sys.executable, binary, "compile", "--check", file],
        capture_output=True,
        text=True,
    )

    assert check_run.returncode == 0
    assert "up to date:" in check_run.stdout


def test_compile_plain_writes_and_checks_both_flavours(tmp_path):
    file = _shape_file(
        tmp_path,
        "flavours.shape.py",
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n\n\n"
        'shape = Compile.shape(div(Slot.value("v")))\n',
    )

    compiled = _run(["compile", "--plain", file])

    assert compiled["code"] == 0
    assert (tmp_path / "flavours.pure.py").exists()
    assert (tmp_path / "flavours.plain.py").exists()
    assert (
        "flavours.pure.py, {}".format(tmp_path / "flavours.plain.py")
        in compiled["stdout"]
    )

    fresh = _run(["compile", "--check", "--plain", file])

    assert fresh["code"] == 0
    assert fresh["stdout"].count("up to date:") == 2

    reordered = _run(["compile", "--plain", "--check", file])

    assert reordered["code"] == 0

    (tmp_path / "flavours.plain.py").unlink()

    missing = _run(["compile", "--check", "--plain", file])

    assert missing["code"] == 1
    assert "missing: {}".format(tmp_path / "flavours.plain.py") in missing["stderr"]

    (tmp_path / "flavours.plain.py").write_text("# tampered\n")

    stale = _run(["compile", "--check", "--plain", file])

    assert stale["code"] == 1
    assert "stale: {}".format(tmp_path / "flavours.plain.py") in stale["stderr"]


def test_artifact_renderers_report_data_keys_the_template_does_not_read(tmp_path):
    from pure.core.DevMode import DevMode

    file = _shape_file(
        tmp_path,
        "manifest.shape.py",
        "from pure.compile.Compile import Compile\n"
        "from pure.core.Slot import Slot\n"
        "from pure.html import div\n\n\n"
        'shape = Compile.shape(div(Slot.value("title")))\n',
    )
    renderer = _load(ArtifactCompiler.write(file)).renderer

    DevMode.reset()
    Compile.guard(True)

    try:
        with pytest.warns(UserWarning) as caught:
            rendered = renderer.render({"title": "t", "titel": "typo"})
    finally:
        Compile.guard(False)
        DevMode.reset()

    assert rendered == "<div>t</div>"
    assert len(caught) == 1
    assert "unknown data key 'titel' (did you mean 'title'?)" in str(caught[0].message)


def _binary():
    return Path(__file__).resolve().parent.parent / "bin" / "pure"


def test_plain_views_fold_a_slot_free_subtree_into_one_literal(tmp_path):
    tree = ul(li("a").class_name("row"), li("b"))

    body = PlainGenerator.view(tree).split("def view")[-1]

    # A subtree that reads no slot is static markup, so it folds into one
    # literal instead of a line per tag.
    assert body.count("out.append(") == 1
    assert "out.append('<ul><li class=\"row\">a</li><li>b</li></ul>')" in body


def test_folding_stops_at_the_first_slot():
    tree = div(p("static"), p(Slot.value("text")))

    body = PlainGenerator.view(tree).split("def view")[-1]

    # The paragraph that reads a slot is generated, and the static one beside it
    # is still folded.
    assert "out.append('<p>static</p>')" in body
    assert "_text(text)" in body
    assert "out.append('<div><p>static</p>')" not in body


def _render_plain_tree(tree, data):
    namespace = {}
    exec(PlainGenerator.view(tree), namespace)
    return namespace["view"](**data)


def test_the_compiled_renderer_casts_a_slot_value_the_php_way():
    compiled = _flat_renderer(Compile.shape(div(Slot.value("v"))).tree())

    # The value arrives at render time, so the cast happens in the runtime.
    assert compiled.render({"v": True}) == "<div>1</div>"
    assert compiled.render({"v": False}) == "<div></div>"
    assert compiled.render({"v": 1.0}) == "<div>1</div>"
    assert compiled.render({"v": 0.1}) == "<div>0.1</div>"


def test_the_compiled_renderer_casts_a_literal_child_at_compile_time():
    compiled = _flat_renderer(Compile.shape(div(1.0)).tree())

    # A literal is frozen into the generated source, so a bool or a float that
    # would print as its repr must not reach it either.
    assert compiled.render({}) == "<div>1</div>"
    assert _flat_renderer(Compile.shape(div(True)).tree()).render({}) == "<div>1</div>"
    assert _flat_renderer(Compile.shape(div(False)).tree()).render({}) == "<div></div>"


def test_the_plain_view_casts_a_slot_value_the_php_way():
    tree = div(Slot.value("v")).title(Slot.value("v"))

    # The plain view carries its own copy of the cast, so it has to agree.
    assert _render_plain_tree(tree, {"v": True}) == '<div title="1">1</div>'
    assert _render_plain_tree(tree, {"v": False}) == '<div title=""></div>'
    assert _render_plain_tree(tree, {"v": 1.0}) == '<div title="1">1</div>'
    assert _render_plain_tree(tree, {"v": 0.1}) == '<div title="0.1">0.1</div>'


def test_the_plain_view_writes_a_bool_attribute_as_a_cast_while_the_compiled_one_omits_it():
    # The two paths differ on purpose, as they do in purephp: a plain view
    # writes the value as an echo, while the compiled renderer's
    # SlotRuntime.attr_open() turns a true value into a bare name.
    tree = div().title(Slot.value("v"))

    assert _render_plain_tree(tree, {"v": True}) == '<div title="1"></div>'
    assert _render_plain_tree(tree, {"v": False}) == '<div title=""></div>'

    compiled = _flat_renderer(Compile.shape(tree).tree())
    assert compiled.render({"v": True}) == '<div title="title"></div>'
    assert compiled.render({"v": False}) == "<div></div>"


def test_a_slot_in_an_attribute_position_keeps_the_subtree_generated():
    tree = div("static").class_name(Slot.value("kind"))

    body = PlainGenerator.view(tree).split("def view")[-1]

    # The attribute reads a slot, so folding the whole tag would lose it.
    assert "out.append('<div>static</div>')" not in body
    assert "SlotRuntime" not in body  # a plain view has no runtime
    assert "_attr('class'" in body


def test_folding_escapes_the_same_way_walking_the_subtree_would():
    tree = div(span("a & b"), Raw.of("<i>raw</i>"))

    namespace = {}
    exec(PlainGenerator.view(tree), namespace)

    # The folded literal is the string renderer's own output, so the escaping
    # and the trusted markup are decided in one place.
    assert namespace["view"]() == "<div><span>a &amp; b</span><i>raw</i></div>"
    assert namespace["view"]() == tree.render()
