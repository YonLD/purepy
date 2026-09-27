# 组件 API

**本页内容**：`component()` 与 `Call`、注册单元、契约注解、`@Template` 以及注册表边界。

Purepy has two ways to build a component. A **plain function** that returns a
tag is enough for a template in one file. A **registered unit** adds a name, a
declared data contract, precompilation and a static check. This page is about
the second; the first is covered in [Components](/guide/components).

## 公开接口一览

| Name | What it is |
| --- | --- |
| `component(name, *children) -> Call` | Build a call to a registered component |
| `register(call, factory=None, override=False, prepare=None)` | Register a unit in a `*.cmp.py` file |
| `Prop(slot=, required=, item=, deprecated=)` | Annotate a `prepare()` parameter |
| `Trusted` | Annotate a parameter whose value is already-safe markup |
| `Binds(*keys)` | Annotate a `prepare()` parameter bound to several slots |
| `@Template()` | Mark a builder so `pure compile --list` reports it |
| `Registry` | The boundary between a unit file and the library |

## `component()` 与 `Call`

```text
component(name: str, *children) -> Call
```

`component()` does not render. It returns a `Call`: a chainable builder that
accumulates named arguments, and renders when you ask it to.

```python
from pure.component import component

card = component('Card').title('Title').content('Content')

print(card.render())
print(card)
```

Both `render()` and `str()` produce the same HTML; `print(card)` uses the
latter.

| `Call` member | What it does |
| --- | --- |
| `.set(key, value)` | Bind one prop by name |
| `.props()` | The accumulated prop dict |
| `.class_(...)` / `.class_name(...)` | Shorthand for a `class` prop |
| `.style(...)` | Shorthand for a `style` prop |
| `.guard()` | Run the development checks (called for you by `render()`) |
| `.render()` | Render now, and return the HTML |

Any name that is not a `Call` member becomes a prop, so a template can accept
whatever arguments it declares:

```python
from pure.component import component

component('Card').title('T').anything_else(1)
```

### Children

`*children` are rendered child components, and they enter the template through
`Slot.raw()`:

```python
from pure.component import component

component('Card').title('T').content(component('Badge').label('New'))
```

::: warning Children need a `raw` slot
A shape is data-free: a rendered child component is runtime behaviour. To place
one, the template must read it through `Slot.raw()`. A plain view cannot contain
a component at all, because a plain view runs without purepy. :::

## 注册一个单元

```text
register(call, factory=None, override=False, prepare=None) -> None
```

A unit is a `*.cmp.py` file holding three parts: the **call function**, the
**factory** and **`prepare()`**.

```python [components/Card.cmp.py]
from pure.core.Slot import Slot

from pure.component import component, register

from pure.html import div, h2, p


def Card(*children):
    return component('Card', *children)


def factory():
    return div(
        h2(Slot.value('title')),
        p(Slot.value('content')),
    ).class_('card')


def prepare(title, content):
    return {'title': title, 'content': content}


register(Card, factory, prepare=prepare)
```

- **`call`** — the function the call site uses. Its `__name__` is the
  registered name.
- **`factory`** — returns the tag tree with `Slot` placeholders. It runs once
  per process; memoize anything expensive in it.
- **`prepare`** — receives the call-site arguments and returns the data dict the
  slots read. It may be omitted when the factory reads nothing but a single
  unnamed data dict.
- **`override** — `False` by default, so a duplicate name raises. `True` reaps
  the name the previous file owned and takes it.

A unit file registers **exactly one** component. `pure compile` refuses a file
that registers none (`no component unit is registered here`) or more than one
(`2 component units are registered here`).

::: warning A `*.cmp.py` file is not importable by name
The dot belongs to the file name, so `import components.Card` cannot work. Use
`pure.loader.load_module(path, name)`, or let the CLI and the registry discover
it. :::

## 契约注解

Annotations on `prepare()` parameters are the component's contract, and
`pure check` reads them. This is the Python spelling of purephp's
`#[Prop]`, `#[Trusted]` and `#[Binds]` attributes.

### `Prop`

```text
Prop(slot=None, required=None, item=None, deprecated=None)
```

| Field | Meaning |
| --- | --- |
| `slot` | The parameter supplies this root slot, under another name |
| `required` | Overrides the shape's own required flag |
| `item` | The parameter supplies one list item, or a list of them, of this item shape |
| `deprecated` | Kept, but warns under the development guard |

```python
from pure.component.Prop import Prop

def prepare(
    heading,                              # a required value slot
    subtitle: Prop(required=False),       # optional, the shape already says so
    rows: Prop(item='label'),             # one item, or a list of them
    teaser: Prop(deprecated='drop it'),
):
    return {'heading': heading, 'subtitle': subtitle, 'rows': rows}
```

A declared `Prop` that does not match the shape is a static error:

```
error: prop $features declares one item slot 'vaule' but the item shape of
       slot 'features' reads 'value' (did you mean 'value'?)
```

### `Trusted`

```python
from pure.component.Trusted import Trusted

def prepare(body: Trusted):
    return {'body': body}
```

`Trusted` marks a value as already-safe markup: it is not escaped again. Use it
only for content you produced, never for request input.

### `Binds`

```python
from pure.component.Binds import Binds

def prepare(media: Binds('src', 'alt')):
    return {'src': media['src'], 'alt': media['alt']}
```

`Binds(*keys)` declares that one parameter supplies several slots.

## `@Template`

```python
from pure.compile.Template import Template

@Template()
def page_shape():
    return Compile.shape(div(Slot.value('title')))
```

`@Template()` marks a memoized shape builder. The marker changes nothing about
rendering; it lets `pure compile --list` report the builder as
`name -> file (template)` so a large unit stays navigable.

## Registry boundary

`Registry` is the seam between a unit file and the library. Application code
normally does not touch it — the CLI wires it in — but it is public, and it is
what the static analysis passes drive.

| Member | What it does |
| --- | --- |
| `Registry.register(name, file, factory, override, prepare)` | Low-level registration, used by `register()` |
| `Registry.component(name_or_path) -> Callable` | The bound renderer for a unit, by name or by file path |
| `Registry.names() -> set` | Every registered name |
| `Registry.unitsFor(file) -> dict` | The units a file declares — the resolver `pure compile` uses |
| `Registry.slots(name_or_path) -> list` | The root slot manifest of a unit |
| `Registry.prepare(name_or_path) -> Callable` | The unit's `prepare()` hook |
| `Registry.reset()` | Drop every registration — for tests |

`Registry.component('Card')` and `Registry.component('components/Card.cmp.py')'
resolve to the same binder, so a call site can name a unit either way.

## 相关页面

- [Components](/guide/components) — the component model in practice
- [Props and Slots](/guide/props) — the full slot reference
- [Artifacts & Deployment](/guide/artifacts) — how a unit becomes a file
