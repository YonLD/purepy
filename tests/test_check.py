import io
import os

import pytest

from pure.compile.Compile import Compile
from pure.component.Registry import Registry
from pure.core.DevMode import DevMode
from pure.core.Slot import Slot

from pure.html import div, h2, li, p, section, span, ul


# --- harness -------------------------------------------------------------
#
# purephp drives every case through the `pure check` command and asserts on
# its exit code and diagnostics. The same shape is used here so a test can
# only pass when the checker actually reports what it claims to.


@pytest.fixture(autouse=True)
def _reset():
    Compile.cachePath(None)
    Compile.flush()
    DevMode.reset()
    Registry.reset()
    yield
    Registry.reset()
    Compile.flush()
    DevMode.reset()


def write_file(dir, name, code):
    path = os.path.join(str(dir), name)
    with open(path, "w") as f:
        f.write(code)
    return path


def run_check(argv):
    from pure.compile.Internal.CheckCommand import CheckCommand

    out, err = io.StringIO(), io.StringIO()
    Registry.reset()
    try:
        code = CheckCommand(lambda f: Registry.unitsFor(f)).run(argv, out, err)
    finally:
        Registry.reset()

    return {"code": code, "stdout": out.getvalue(), "stderr": err.getvalue()}


UNIT_HEADER = (
    "from pure.compile.Compile import Compile\n"
    "from pure.component.functions import component, register\n"
    "from pure.core.Slot import Slot\n"
    "from pure.html import div, h2, li, p, section, span, ul\n"
)


def test_clean_unit_passes(tmp_path):
    file = write_file(
        tmp_path,
        "clean.cmp.py",
        UNIT_HEADER
        + """
def CleanBox(*children):
    return component('CleanBox', *children)

def prepare(title: str, items: list):
    return {'title': title, 'items': items}

register(CleanBox, lambda: Compile.shape(
    div(Slot.value('title'), ul(Slot.each('items', li(Slot.value('label')))))
), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "ok: component 'CleanBox' -> {}".format(file) in result["stdout"]
    assert "checked 1 unit(s): 0 error(s), 0 warning(s)." in result["stdout"]


def test_type_mismatch_between_slot_and_parameter_is_an_error(tmp_path):
    file = write_file(
        tmp_path,
        "types.cmp.py",
        UNIT_HEADER
        + """
def TypeBox(*children):
    return component('TypeBox', *children)

def prepare(title: str, items: str):
    return {'title': title, 'items': items}

register(TypeBox, lambda: Compile.shape(
    div(Slot.value('title'), ul(Slot.each('items', li(Slot.value('label')))))
), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    # purephp names the PHP type ("string"); the Python port names the Python one.
    assert (
        "slot 'items' is a list slot but parameter $items is typed str"
        in result["stdout"]
    )
    assert "slot 'title'" not in result["stdout"]


def test_nullable_parameter_for_a_required_slot_warns(tmp_path):
    file = write_file(
        tmp_path,
        "nullable.cmp.py",
        """
from typing import Optional

from pure.compile.Compile import Compile
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div

def NullBox(*children):
    return component('NullBox', *children)

def prepare(title: Optional[str]):
    return {'title': title}

register(NullBox, lambda: Compile.shape(div(Slot.value('title'))), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "warning: component 'NullBox': parameter $title is nullable but slot 'title' is required" in result[
        "stdout"
    ].replace(
        " -> {}".format(file), ""
    )

    strict = run_check(["check", "--strict", file])

    assert strict["code"] == 1


def test_unused_parameter_warns(tmp_path):
    file = write_file(
        tmp_path,
        "unused.cmp.py",
        UNIT_HEADER
        + """
def UnusedBox(*children):
    return component('UnusedBox', *children)

def prepare(title: str, extra: str = ''):
    return {'title': title}

register(UnusedBox, lambda: Compile.shape(div(Slot.value('title'))), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert (
        "parameter $extra is neither used by prepare() nor a slot of the template"
        in result["stdout"]
    )


def test_function_that_does_not_return_a_call_is_an_error(tmp_path):
    file = write_file(
        tmp_path,
        "plain-fn.cmp.py",
        UNIT_HEADER
        + """
def PlainFunctionBox(*children):
    return 'not a call'

register(PlainFunctionBox, lambda: Compile.shape(div(Slot.value('title'))))
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert "'PlainFunctionBox()' must return pure.component.Call" in result["stdout"]


def test_unit_without_prepare_or_call_function_points_at_the_call_sites(tmp_path):
    # The internal primitive registers under a name with no call function:
    # the public register() always derives one.
    file = write_file(
        tmp_path,
        "page.cmp.py",
        """
from pure.compile.Compile import Compile
from pure.component.Registry import Registry
from pure.core.Slot import Slot
from pure.html import div

Registry.register('PageBox', __file__, lambda: Compile.shape(div(Slot.value('title'))))
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "no prepare() and no function named 'PageBox'" in result["stdout"]
    assert "0 error(s), 0 warning(s)." in result["stdout"]


def test_fluent_unit_without_prepare_points_at_the_call_sites(tmp_path):
    file = write_file(
        tmp_path,
        "fluent.cmp.py",
        UNIT_HEADER
        + """
def FluentBox(*children):
    return component('FluentBox', *children)

register(FluentBox, lambda: Compile.shape(div(Slot.value('title'))))
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "fluent unit: its props are the template slots" in result["stdout"]


def test_fluent_unit_checks_prepare_against_the_slots(tmp_path):
    file = write_file(
        tmp_path,
        "fluent-ok.cmp.py",
        UNIT_HEADER
        + """
def FluentOk(*children):
    return component('FluentOk', *children)

def prepare(title: str):
    return {'title': title}

register(FluentOk, lambda: Compile.shape(div(Slot.value('title'))), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "0 error(s), 0 warning(s)." in result["stdout"]


def test_shape_file_with_conflicting_slot_kinds_is_an_error(tmp_path):
    file = write_file(
        tmp_path,
        "conflict.shape.py",
        """
from pure.compile.Compile import Compile
from pure.core.Slot import Slot
from pure.html import div, li, span, ul

def shape():
    return Compile.shape(div(
        Slot.value('items'),
        ul(Slot.each('items', li(Slot.value('label')))),
    ))
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert (
        "slot 'items' is used as a value or raw slot and as a child or list scope"
        in result["stdout"]
    )


def test_clean_shape_file_passes(tmp_path):
    file = write_file(
        tmp_path,
        "clean.shape.py",
        """
from pure.compile.Compile import Compile
from pure.core.Slot import Slot
from pure.html import div

def shape():
    return Compile.shape(div(Slot.value('title')))
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "ok: {} (shape)".format(file) in result["stdout"]


def test_directory_is_searched_recursively(tmp_path):
    nested = os.path.join(str(tmp_path), "nested")
    os.makedirs(nested)

    write_file(
        nested,
        "nested.cmp.py",
        UNIT_HEADER
        + """
def NestedBox(*children):
    return component('NestedBox', *children)

register(NestedBox, lambda: Compile.shape(div(Slot.value('title'))))
""",
    )

    result = run_check(["check", str(tmp_path)])

    assert result["code"] == 0
    assert "checked 1 unit(s)" in result["stdout"]


def test_missing_path_is_reported(tmp_path):
    result = run_check(["check", os.path.join(str(tmp_path), "missing")])

    assert result["code"] == 1
    assert "does not exist" in result["stderr"]


def test_usage_errors(tmp_path):
    missing = run_check(["check"])
    assert missing["code"] == 1
    assert "check needs at least one file or directory" in missing["stderr"]

    unknown = run_check(["check", "--nope", str(tmp_path)])
    assert unknown["code"] == 1
    assert "unknown option '--nope'" in unknown["stderr"]

    help_result = run_check(["check", "--help"])
    assert help_result["code"] == 0
    assert "Usage:" in help_result["stdout"]
    assert "pure compile --check" in help_result["stdout"]


def _arrow_unit(dir, name, shape_src, prepare_src, filename=None):
    return write_file(
        dir,
        filename or (name + ".cmp.py"),
        UNIT_HEADER
        + """
def {name}(*children):
    return component('{name}', *children)

def prepare({params}):
    return {body}

register({name}, lambda: Compile.shape({shape}), prepare=prepare)
""".format(
            name=name, shape=shape_src, params=prepare_src[0], body=prepare_src[1]
        ),
    )


def test_arrow_prepare_returns_one_array_literal(tmp_path):
    file = _arrow_unit(
        tmp_path,
        "ArrowOk",
        "div(Slot.value('title'))",
        ("title: str", "{'title': title}"),
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "does not return one array literal" not in result["stdout"]
    assert "0 error(s), 0 warning(s)." in result["stdout"]


def test_arrow_prepare_keys_are_compared_against_the_slots(tmp_path):
    file = _arrow_unit(
        tmp_path,
        "ArrowMiss",
        "div(Slot.value('title'), Slot.value('desc'))",
        ("title: str", "{'title': title}"),
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert "required slot 'desc' is not returned by prepare()" in result["stdout"]


def test_arrow_prepare_unused_parameter_warns(tmp_path):
    file = _arrow_unit(
        tmp_path,
        "ArrowUnused",
        "div(Slot.value('title'))",
        ("title: str, extra: str = ''", "{'title': title}"),
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert (
        "parameter $extra is neither used by prepare() nor a slot of the template"
        in result["stdout"]
    )


def test_call_methods_are_not_reported_as_unknown_props(tmp_path):
    write_file(
        tmp_path,
        "target-methods.cmp.py",
        UNIT_HEADER
        + """
def CheckTargetMethods(*children):
    return component('CheckTargetMethods', *children)

register(CheckTargetMethods, lambda: Compile.shape(div(Slot.value('title'))))
""",
    )

    write_file(
        tmp_path,
        "page-methods.cmp.py",
        UNIT_HEADER
        + """
def CheckPageMethods(*children):
    return component('CheckPageMethods', *children)

register(CheckPageMethods, lambda: Compile.shape(section(Slot.raw('body'))))

def checkPageMethodsBody():
    return str(CheckTargetMethods().props(title='a').render())
""",
    )

    result = run_check(["check", str(tmp_path)])

    assert result["code"] == 0
    assert "binds 'props'" not in result["stdout"]
    assert "binds 'render'" not in result["stdout"]


def test_closure_form_registration_derives_name_and_file(tmp_path):
    file = write_file(
        tmp_path,
        "closure-form.cmp.py",
        UNIT_HEADER
        + """
def ClosureBox(*children):
    return component('ClosureBox', *children)

register(ClosureBox, lambda: Compile.shape(div(Slot.value('title'))))
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "component 'ClosureBox'" in result["stdout"]
    assert "no component unit is registered" not in result["stdout"] + result["stderr"]
    assert "no function named 'ClosureBox'" not in result["stdout"]


def test_closure_form_rejects_an_anonymous_closure(tmp_path):
    file = write_file(
        tmp_path,
        "closure-anon.cmp.py",
        UNIT_HEADER
        + """
register(
    lambda *children: None,
    factory=lambda: Compile.shape(div(Slot.value('title'))),
)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert "anonymous" in result["stderr"]


def test_template_function_must_declare_a_shape_return_type(tmp_path):
    file = write_file(
        tmp_path,
        "attr-template.cmp.py",
        """
from pure.compile.Compile import Compile
from pure.compile.Template import Template
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div

def TplBox(*children):
    return component('TplBox', *children)

register(TplBox, lambda: Compile.shape(div(Slot.value('title'))))

@Template
def tplBoxBroken() -> str:
    return 'not a shape'
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert "tplBoxBroken" in result["stdout"]
    assert "must declare a return type" in result["stdout"]


def test_template_marked_function_is_not_taken_for_the_call_function(tmp_path):
    file = write_file(
        tmp_path,
        "attr-tpl-skip.cmp.py",
        """
from pure.compile.Compile import Compile
from pure.compile.Template import Template
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div

def TplSkip(*children):
    return component('TplSkip', *children)

register(TplSkip, lambda: Compile.shape(div(Slot.value('title'))))

@Template
def TplSkipShape():
    return Compile.shape(div(Slot.value('title')))
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "no function named 'TplSkipShape'" not in result["stdout"]


PROP_HEADER = UNIT_HEADER + "from pure.component.Prop import Prop\n"


def test_two_props_declaring_one_slot_are_an_error(tmp_path):
    file = write_file(
        tmp_path,
        "dup.cmp.py",
        PROP_HEADER
        + """
def CheckDup(*children):
    return component('CheckDup', *children)

def prepare(text: Prop = Prop(slot='title'), heading: Prop = Prop(slot='title')):
    return {'title': text + heading}

register(CheckDup, lambda: Compile.shape(div(Slot.value('title'))), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert "props $text and $heading declare the same slot 'title'" in result["stdout"]


def test_declared_slot_must_be_returned_by_a_prepare_literal(tmp_path):
    file = write_file(
        tmp_path,
        "literal.cmp.py",
        PROP_HEADER
        + """
def CheckLiteral(*children):
    return component('CheckLiteral', *children)

def prepare(text: Prop = Prop(slot='title')):
    return {'titel': text}

register(CheckLiteral, lambda: Compile.shape(div(h2(Slot.value('title')))), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert (
        "prop $text declares slot 'title', which prepare() does not return"
        in result["stdout"]
    )


def test_declared_slot_must_be_read_by_the_template(tmp_path):
    file = write_file(
        tmp_path,
        "typo.cmp.py",
        PROP_HEADER
        + """
def CheckTypo(*children):
    return component('CheckTypo', *children)

def prepare(text: Prop = Prop(slot='titel')):
    return {'titel': text}

register(CheckTypo, lambda: Compile.shape(div(h2(Slot.value('title')))), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert (
        "prop $text declares slot 'titel', which the template does not read (did you mean 'title'?)"
        in result["stdout"]
    )


def test_undeclared_required_slot_is_an_error_when_prepare_is_computed(tmp_path):
    file = write_file(
        tmp_path,
        "undeclared.cmp.py",
        PROP_HEADER
        + """
def CheckUndeclared(*children):
    return component('CheckUndeclared', *children)

def prepare(text: Prop = Prop(slot='title'), body: str = ''):
    data = {'title': text.upper(), 'contents': body}
    return data

register(CheckUndeclared, lambda: Compile.shape(
    div(h2(Slot.value('title')), div(Slot.raw('contents')))
), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert (
        "required slot 'contents' is not covered by any declaration and prepare() does not return a readable array literal"
        in result["stdout"]
    )


def test_fluent_unit_with_a_computed_prepare_result_is_not_compared(tmp_path):
    file = _arrow_unit(
        tmp_path,
        "CheckFluentComputed",
        "div(Slot.value('title'))",
        ("title: str", "data"),
        filename="fluent-computed.cmp.py",
    )
    # prepare() must build `data` and return it, so the literal is not readable.
    with open(file, "a") as f:
        pass

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "prepare() does not return one array literal" in result["stdout"]


def test_prepare_keys_are_read_from_an_interpolated_literal(tmp_path):
    file = write_file(
        tmp_path,
        "interpolated.cmp.py",
        UNIT_HEADER
        + """
def CheckInterpolated(*children):
    return component('CheckInterpolated', *children)

def prepare(title: str, bg: str = ''):
    return {
        'title': title,
        'style': "background-image: url('%s');" % bg,
    }

register(CheckInterpolated, lambda: Compile.shape(
    div(Slot.value('title')).style(Slot.value('style').default(None))
), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "prepare() does not return one array literal" not in result["stdout"]
    assert "0 error(s), 0 warning(s)." in result["stdout"]


def test_binds_must_match_a_readable_literal(tmp_path):
    file = write_file(
        tmp_path,
        "binds-literal.cmp.py",
        UNIT_HEADER
        + """
from pure.component.Binds import Binds

def CheckBindsLiteral(*children):
    return component('CheckBindsLiteral', *children)

@Binds('title', 'titel')
def prepare():
    return {'title': 'Pricing', 'desc': 'Plans'}

register(CheckBindsLiteral, lambda: Compile.shape(
    div(Slot.value('title'), div(Slot.raw('desc')))
), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert (
        "#[Binds] declares 'titel', which prepare() does not return" in result["stdout"]
    )


def test_deprecated_prop_is_reported_at_call_sites(tmp_path):
    write_file(
        tmp_path,
        "deprecated-target.cmp.py",
        PROP_HEADER
        + """
def CheckDeprecated(*children):
    return component('CheckDeprecated', *children)

def prepare(title: Prop = Prop(slot='title'), style: Prop = Prop(deprecated='use class()')):
    return {'title': title, 'style': style}

register(CheckDeprecated, lambda: Compile.shape(
    div(Slot.value('title')).style(Slot.value('style'))
), prepare=prepare)
""",
    )

    write_file(
        tmp_path,
        "deprecated-calls.cmp.py",
        UNIT_HEADER
        + """
def CheckDeprecatedPage(*children):
    return component('CheckDeprecatedPage', *children)

register(CheckDeprecatedPage, lambda: Compile.shape(div()))

def checkDeprecatedBody():
    return str(CheckDeprecated('Home').style('color: red'))
""",
    )

    result = run_check(["check", str(tmp_path)])

    assert result["code"] == 0
    assert (
        "component 'CheckDeprecated': the call binds 'style', which is deprecated: use class()"
        in result["stdout"]
    )
    assert "0 error(s), 1 warning(s)." in result["stdout"]


def test_fluent_unit_prepare_mismatch_is_reported(tmp_path):
    file = _arrow_unit(
        tmp_path,
        "CheckFluentTypo",
        "div(h2(Slot.value('title')))",
        ("section: str", "{'titel': section.upper()}"),
        filename="fluent-typo.cmp.py",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert (
        "prepare() returns 'titel' but the template does not read it (did you mean 'title'?)"
        in result["stdout"]
    )
    assert "required slot 'title' is not returned by prepare()" in result["stdout"]


def test_call_function_can_resolve_the_unit_by_file_path(tmp_path):
    file = write_file(
        tmp_path,
        "namespaced.cmp.py",
        UNIT_HEADER
        + """
def NamespacedBox(*children):
    return component(__file__)

register(NamespacedBox, lambda: Compile.shape(div(Slot.value('title'))))
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert (
        "fluent unit: its props are the template slots, so the call sites are checked instead"
        in result["stdout"]
    )
    assert "0 error(s), 0 warning(s)." in result["stdout"]


def test_declared_required_must_match_the_signature(tmp_path):
    # purephp reads #[Prop(required: false)] as an attribute, separate from the
    # parameter's default. In Python the declaration is the annotation, so a
    # real default stays visible as the default.
    file = write_file(
        tmp_path,
        "declared-required.cmp.py",
        PROP_HEADER
        + """
def CheckDeclaredRequired(*children):
    return component('CheckDeclaredRequired', *children)

def prepare(
    text: Prop(required=False),
    klass: Prop(required=True, slot='class') = None,
):
    return {'title': text, 'class': klass}

register(CheckDeclaredRequired, lambda: Compile.shape(
    div(Slot.value('title'), Slot.value('class').default(''))
), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 1
    assert (
        "prop $text is declared optional but its parameter has no default value; callers must pass it"
        in result["stdout"]
    )
    assert (
        "prop $klass is declared required but its parameter has a default value; callers may omit it"
        in result["stdout"]
    )


def test_declared_slots_carry_the_bindings_of_a_computed_prepare(tmp_path):
    file = write_file(
        tmp_path,
        "declared.cmp.py",
        PROP_HEADER
        + """
def CheckDeclared(*children):
    return component('CheckDeclared', *children)

def prepare(text: Prop = Prop(slot='title'), body: Prop = Prop(slot='contents')):
    data = {'title': text.upper(), 'contents': body}
    return data

register(CheckDeclared, lambda: Compile.shape(
    div(h2(Slot.value('title')), div(Slot.raw('contents')))
), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "its bindings are read from the #[Prop] declarations" in result["stdout"]
    assert "0 error(s), 0 warning(s)." in result["stdout"]


def test_declared_item_is_checked_against_the_item_shape(tmp_path):
    file = write_file(
        tmp_path,
        "declared-item.cmp.py",
        PROP_HEADER
        + """
def CheckDeclaredItem(*children):
    return component('CheckDeclaredItem', *children)

def prepare(features: Prop(item='value')):
    return {'features': [{'value': f} for f in features]}

register(CheckDeclaredItem, lambda: Compile.shape(
    ul(Slot.each('features', li(Slot.value('value'))))
), prepare=prepare)
""",
    )

    result = run_check(["check", file])

    assert result["code"] == 0
    assert "0 error(s), 0 warning(s)." in result["stdout"]


def test_trusted_prop_must_bind_a_raw_slot(tmp_path):
    header = UNIT_HEADER + "from pure.component.Trusted import Trusted\n"

    write_file(
        tmp_path,
        "trusted-text.cmp.py",
        header
        + """
def CheckTrustedText(*children):
    return component('CheckTrustedText', *children)

def prepare(title: Trusted):
    return {'title': title}

register(CheckTrustedText, lambda: Compile.shape(div(Slot.value('title'))), prepare=prepare)
""",
    )

    write_file(
        tmp_path,
        "trusted-raw.cmp.py",
        header
        + """
from pure.core.Raw import Raw

def CheckTrustedRaw(*children):
    return component('CheckTrustedRaw', *children)

def prepare(icon: Trusted):
    return {'icon': icon}

register(CheckTrustedRaw, lambda: Compile.shape(div(Slot.raw('icon'))), prepare=prepare)
""",
    )

    write_file(
        tmp_path,
        "trusted-mixed.cmp.py",
        header
        + """
def CheckTrustedMixed(*children):
    return component('CheckTrustedMixed', *children)

def prepare(body: Trusted):
    return {'body': body}

register(CheckTrustedMixed, lambda: Compile.shape(
    div(Slot.raw('body'), Slot.value('body'))
), prepare=prepare)
""",
    )

    write_file(
        tmp_path,
        "trusted-unread.cmp.py",
        header
        + """
def CheckTrustedUnread(*children):
    return component('CheckTrustedUnread', *children)

def prepare(extra: Trusted = None):
    return {'extra': extra}

register(CheckTrustedUnread, lambda: Compile.shape(div()), prepare=prepare)
""",
    )

    result = run_check(["check", str(tmp_path)])

    assert result["code"] == 1
    assert "ok: component 'CheckTrustedRaw'" in result["stdout"]
    assert (
        "prop $title is declared as markup (#[Trusted]) but slot 'title' is a text slot"
        in result["stdout"]
    )
    assert (
        "prop $body is declared as markup (#[Trusted]) but slot 'body' is also read as a text slot"
        in result["stdout"]
    )
    assert (
        "prop $extra is declared as markup (#[Trusted]) but slot 'extra' is not read by the template"
        in result["stdout"]
    )


def test_binds_declares_the_keys_of_a_computed_prepare(tmp_path):
    header = UNIT_HEADER + "from pure.component.Binds import Binds\n"

    write_file(
        tmp_path,
        "binds-covered.cmp.py",
        header
        + """
def CheckBindsCovered(*children):
    return component('CheckBindsCovered', *children)

@Binds('title', 'desc')
def covered():
    data = {'title': 'Pricing', 'desc': 'Plans'}
    return data

register(CheckBindsCovered, lambda: Compile.shape(
    div(Slot.value('title'), div(Slot.raw('desc')))
), prepare=covered)
""",
    )

    write_file(
        tmp_path,
        "binds-uncovered.cmp.py",
        header
        + """
def CheckBindsUncovered(*children):
    return component('CheckBindsUncovered', *children)

@Binds('title')
def uncovered():
    data = {'title': 'Pricing'}
    return data

register(CheckBindsUncovered, lambda: Compile.shape(
    div(Slot.value('title'), div(Slot.raw('desc')))
), prepare=uncovered)
""",
    )

    result = run_check(["check", str(tmp_path)])

    assert result["code"] == 1
    assert "its bindings are read from the #[Binds] declarations" in result["stdout"]
    assert (
        "required slot 'desc' is not covered by any declaration and prepare() does not return a readable array literal"
        in result["stdout"]
    )


def test_fluent_call_site_props_are_checked_against_the_target(tmp_path):
    write_file(
        tmp_path,
        "target.cmp.py",
        UNIT_HEADER
        + """
def CheckTarget(*children):
    return component('CheckTarget', *children)

register(CheckTarget, lambda: Compile.shape(div(Slot.value('title'))))
""",
    )

    write_file(
        tmp_path,
        "page-calls.cmp.py",
        UNIT_HEADER
        + """
def CheckPageCalls(*children):
    return component('CheckPageCalls', *children)

register(CheckPageCalls, lambda: Compile.shape(div()))

def checkPageCallsBody():
    return str(CheckTarget('child').titel('typo'))

def checkPageCallsChildren():
    return str(CheckTarget('child').children('x'))
""",
    )

    result = run_check(["check", str(tmp_path)])

    assert result["code"] == 1
    assert (
        "component 'CheckTarget': the call binds 'titel', which the target does not accept (did you mean 'title'?)"
        in result["stdout"]
    )
    assert (
        "component 'CheckTarget': pass children to the call itself" in result["stdout"]
    )


def test_declared_item_mismatches_are_reported(tmp_path):
    def unit(name, shape, prepare_body, params):
        write_file(
            tmp_path,
            name + ".cmp.py",
            PROP_HEADER
            + """
def {name}(*children):
    return component('{name}', *children)

def prepare({params}):
    return {body}

register({name}, lambda: Compile.shape({shape}), prepare=prepare)
""".format(
                name=name, shape=shape, params=params, body=prepare_body
            ),
        )

    unit(
        "CheckItemWrong",
        "ul(Slot.each('features', li(Slot.value('value'))))",
        "{'features': [{'vaule': f} for f in features]}",
        "features: Prop(item='vaule')",
    )
    unit(
        "CheckItemMulti",
        "ul(Slot.each('features', li(Slot.value('value'), Slot.value('url'))))",
        "{'features': [{'value': f} for f in features]}",
        "features: Prop(item='value')",
    )
    unit(
        "CheckItemText",
        "div(Slot.value('title'))",
        "{'title': title}",
        "title: Prop(item='value')",
    )
    unit(
        "CheckItemStatic",
        "ul(Slot.each('features', li('static')))",
        "{'features': features}",
        "features: Prop(item='value')",
    )

    result = run_check(["check", str(tmp_path)])

    assert result["code"] == 1
    assert (
        "prop $features declares one item slot 'vaule' but the item shape of slot 'features' reads 'value' (did you mean 'value'?)"
        in result["stdout"]
    )
    assert (
        "prop $features declares one item slot 'value' but the item shape of slot 'features' reads 'value', 'url'"
        in result["stdout"]
    )
    assert (
        "prop $title declares item: 'value' but slot 'title' is not a list slot"
        in result["stdout"]
    )
    assert (
        "prop $features declares item: 'value' but the item shape of slot 'features' reads no slots"
        in result["stdout"]
    )


def test_call_site_item_keys_are_checked_against_the_item_shape(tmp_path):
    write_file(
        tmp_path,
        "items-target.cmp.py",
        UNIT_HEADER
        + """
from pure.html import a as html_a

def CheckItems(*children):
    return component('CheckItems', *children)

register(CheckItems, lambda: Compile.shape(
    ul(Slot.each('links', li(html_a(Slot.value('text')).href(Slot.value('href')))))
))
""",
    )

    write_file(
        tmp_path,
        "items-declared.cmp.py",
        PROP_HEADER
        + """
from pure.html import a as html_a

def CheckItemsDeclared(*children):
    return component('CheckItemsDeclared', *children)

def prepare(rows: Prop(slot='links')):
    return {'links': rows}

register(CheckItemsDeclared, lambda: Compile.shape(
    ul(Slot.each('links', li(html_a(Slot.value('text')).href(Slot.value('href')))))
), prepare=prepare)
""",
    )

    write_file(
        tmp_path,
        "items-calls.cmp.py",
        UNIT_HEADER
        + """
def CheckItemsPage(*children):
    return component('CheckItemsPage', *children)

register(CheckItemsPage, lambda: Compile.shape(div()))

def checkItemsBody():
    return str(
        CheckItems('x').links([{'text': 'Team', 'href': '#'}])
        + str(CheckItems('x').links([
            {'text': 'A', 'href': '#'},
            {'txet': 'B', 'href': '#'},
        ]))
        + str(CheckItems('x').links([{'text': 'Team'}]))
        + str(CheckItemsDeclared('x').rows([{'text': 'Team', 'href': '#'}]))
        + str(CheckItems('x').links(['a', 'b']))
    )
""",
    )

    result = run_check(["check", str(tmp_path)])

    assert result["code"] == 1
    assert (
        "item 2 of 'links' binds 'txet', which the item shape of slot 'links' does not read (did you mean 'text'?)"
        in result["stdout"]
    )
    assert (
        "item 2 of 'links' does not provide 'text', which the item shape of slot 'links' requires"
        in result["stdout"]
    )
    assert (
        "item 1 of 'links' does not provide 'href', which the item shape of slot 'links' requires"
        in result["stdout"]
    )
    assert "of 'rows'" not in result["stdout"]
    assert "binds 'a'" not in result["stdout"]
    assert "3 error(s)" in result["stdout"]
