# Compiled Rendering

**Prerequisites**: [Components](/guide/components) · **On this page**: how a component's template compiles, the runtime cache, and performance.

Compiled rendering turns a data-free **shape** — a component's template —
into a flat Python renderer. Static markup is escaped once at compile time and
emitted as a literal string, so rendering a page costs little more than string
concatenation plus escaping of the dynamic values.

A component's factory returns a bare tag tree of `Slot` placeholders; the
registry wraps it into a `Shape` — the same wrap `Compile.shape()` performs
for an inline tree. Templates are built **once per process** — in a long-running
worker, a CLI process, or any host that keeps module state between requests.
Under standard WSGI, where every request starts a fresh process, enable the
on-disk cache (see [Caching](#caching)) to load compiled renderers instead of
regenerating them per request, or deploy with precompiled artifacts
(see [Artifacts & Deployment](/guide/artifacts)).

## Shape, Slot, Renderer

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div, h1, li, ul

# A shape is a normal tag tree with Slot placeholders instead of data.
item = Compile.shape(li(Slot.value('title')))

root = Compile.shape(
    div(
        h1(Slot.value('heading')),
        ul(Slot.each('items', item)),
    ).class_('card')
)

# Rendering binds plain data.
print(root({
    'heading': 'Users',
    'items': [{'title': 'Ada'}, {'title': 'Grace'}],
}))
```

Output:

```html
<div class="card"><h1>Users</h1><ul><li>Ada</li><li>Grace</li></ul></div>
```

| Object | Meaning |
| --- | --- |
| `Shape` | A data-free tree: `shape(data)`, `compile()`, `id()`, `print(data)`, `save(path, data)` |
| `Renderer` | The compiled renderer: `render(data)`, `save(path, data)`, and the `source` / `id` / `slots` properties |
| `Slot` | A placeholder for data, bound at render time |

All four rendering paths — `shape(data)`, `renderer.render(data)`, the flat
`CodeGenerator` path and the generated plain view — produce **byte-identical**
output for the same tree, because they share one escaping implementation. The
tests assert exactly that, so a divergence in any one path is a test failure
rather than a surprise in production.

The slots a template can use (`Slot.value()`, `Slot.raw()`, `Slot.child()`,
`Slot.each()`, `Slot.if_()`), their modifiers, value coercion and the missing
data rules are documented once in [Props and Slots](/guide/props#slot-reference);
this page does not repeat them.

## Scope and Missing Data

`Slot.child()` and `Slot.each()` create a nested data scope; inside it, slots
resolve against that scope. Missing required keys raise
`pure.core.MissingSlotException.MissingSlotException` with the full path, whose
message names the closest provided key or lists the keys the scope did provide.
Use `.default(value)` or `.required(False)` for optional data — the full rules
are in [Props and Slots](/guide/props).

`Slot.if_()` branches share the current scope, so this works naturally:

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import li, span

item = Compile.shape(
    li(
        Slot.value('name'),
        Slot.if_('admin', span('(admin)')),
    )
)
```

::: tip Python keyword escapes
`if` is a Python keyword, so the branch helper is `Slot.if_()`. The same
convention applies to attributes: `for_()` renders `for="…"`, `class_()`
renders `class="…"`, and `data_id()` still renders `data-id="…"`. A trailing
underscore only escapes a keyword; anywhere else an underscore becomes a
hyphen. :::

## Components

The template of a component — a `*.cmp.py` unit with its call function, lazy
factory and `prepare()` hook (the full treatment is in
[Components](/guide/components)) — goes through this same pipeline: the factory
runs once per compile generation, the tree wraps into a shape, and the compiled
renderer is what requests reuse.

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

A `*.cmp.py` file is not importable under its own name — the dot is part of
the file name, not a package path. Load one with `pure.loader.load_module`,
or let the CLI and the component registry find it:

```python
from pure.loader import load_module

card = load_module('components/Card.cmp.py', 'Card')

print(card.Card().title('Title').content('Content'))
```

Output:

```html
<div class="card"><h2>Title</h2><p>Content</p></div>
```

Inside a template, nested shapes use `Slot.child()`, lists use `Slot.each()`,
optional/conditional markup uses `Slot.if_()`, and rendered child components
enter through `Slot.raw()`.

## Lists

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import li, ul

row = Compile.shape(li(Slot.value('label')))

shape = Compile.shape(ul(Slot.each('rows', row)))

print(shape({'rows': [{'label': 'a'}, {'label': 'b'}]}))
```

## Caching

By default the compiled renderer exists only in memory, which suits
long-running workers that keep state between requests. Under a plain WSGI
server the shape tree is rebuilt and the renderer regenerated on every request
— slower than immediate rendering — so enable the on-disk renderer cache and
load the generated code instead of regenerating it:

```python
from pure.compile.Compile import Compile

# Once, during bootstrap
Compile.cachePath('/var/cache/purepy')
```

- `Compile.cachePath(dir)` enables the on-disk renderer cache; pass `None`
  to disable (the default).
- Cache files are content-addressed by `Shape.id()`; a changed shape writes a
  new file.
- Writes are atomic (temporary file plus `os.rename`), so concurrent workers
  are safe.
- `cachePath()` creates a missing directory with mode `0700` and rejects
  group/other-writable modes. It does not check whether the path is outside the
  web root, so keep the cache in a dedicated directory outside the document
  root.
- `Compile.clearCache()` deletes the files written by the library.
- `Compile.flush()` invalidates in-memory renderers (useful in long-running
  workers after a deploy).

### Memoize your shapes

To catch shapes that are rebuilt per request instead of memoized, turn on the
development guard:

```python
from pure.compile.Compile import Compile

Compile.guard(True)
```

It also warns about a misspelled standard attribute name, and about data keys a
template never reads. See [Development Guard](/guide/troubleshooting#development-guard).

Build each shape once and reuse it:

```python
_shape = None


def shape():
    global _shape
    if _shape is None:
        _shape = Compile.shape(div(Slot.value('title')))
    return _shape
```

## Shape Identity

`Shape.id()` is a SHA-1 fingerprint of the structure: the same tree always
produces the same id, and any structural change produces a different one. It
mixes in `Compile.CACHE_VERSION` and the Python minor version, so a runtime
upgrade never reuses a renderer built for the old one.

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div

a = Compile.shape(div(Slot.value('x')))
b = Compile.shape(div(Slot.value('x')))
c = Compile.shape(div(Slot.value('y')))

assert a.id() == b.id()   # same structure, same id
assert a.id() != c.id()   # different slot name, different id
```

The fingerprint walks the tree through the same `ShapeWalker` the code
generator uses, so a shape and its compiled renderer always agree on what
"the same shape" means.

## Where to go next

- [Artifacts & Deployment](/guide/artifacts) — precompile templates to files
- [Props and Slots](/guide/props) — the full slot reference
- [Troubleshooting](/guide/troubleshooting) — debugging a shape that will not compile
