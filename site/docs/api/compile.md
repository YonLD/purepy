# Compile API

**On this page**: `Compile`, `Shape`, `Renderer`, the slot kinds, the structure
fingerprint, the on-disk cache, the development guard, and the errors.

## Classes

| Class | What it is |
| --- | --- |
| `Compile` | Static entry points: build a shape, compile a tree, control the cache and the guard |
| `Shape` | A data-free tree: `shape(data)`, `compile()`, `id()`, `tree()`, `print(data)`, `save(path, data)` |
| `Renderer` | A compiled renderer: `render(data)`, `save(path, data)`, and `id` / `slots` |
| `ShapeIndex` | The structural fingerprint behind `Shape.id()` |

## `Compile`

| Member | Signature | What it does |
| --- | --- | --- |
| `Compile.shape` | `(tree: Tag) -> Shape` | Wrap a tag tree as a data-free shape |
| `Compile.renderer` | `(tree: Tag) -> Renderer` | Compile a tree straight to a renderer |
| `Compile.toShape` | `(result) -> Optional[Shape]` | Accept a `Tag` or a `Shape` and return a `Shape`, or `None` |
| `Compile.cachePath` | `(dir) -> None` | Enable or disable the on-disk cache |
| `Compile.clearCache` | `() -> int` | Delete the files the library wrote; returns how many |
| `Compile.flush` | `() -> None` | Drop in-memory renderers |
| `Compile.guard` | `(enabled: bool = True) -> None` | Turn the development checks on or off |
| `Compile.CACHE_VERSION` | `int` | Bumped whenever the generated code changes |
| `Compile.MEMO_BYTES` | `int` | The in-memory source-memo budget |

`flush()` is what a long-running worker calls after a deploy; `guard()` is what
a test or a development server turns on.

## Shape vs. Data

A `Shape` is a tree with placeholders. Data arrives when you call it.

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div, h1, ul, li

item = Compile.shape(li(Slot.value('title')))

root = Compile.shape(
    div(
        h1(Slot.value('heading')),
        ul(Slot.each('items', item)),
    ).class_('card')
)

print(root({'heading': 'Users', 'items': [{'title': 'Ada'}]}))
```

`Compile.toShape()` is the adapter that makes the two interchangeable, and it
is what a factory's return value goes through:

```python
Compile.toShape(tag_tree)        # -> Shape
Compile.toShape(shape)           # -> the same Shape
Compile.toShape(render_result)   # -> None  (a component call is not a tree)
```

That last case is why a rendered child component cannot be baked into a shape:
`toShape()` returns `None` for it, and the error says so.

## Slot Kinds

| Kind | Helper | Value it binds |
| --- | --- | --- |
| `Value` | `Slot.value(name)` | A scalar, escaped; also valid in attribute position |
| `Raw` | `Slot.raw(name)` | Markup, or any iterable joined verbatim; never escaped |
| `Child` | `Slot.child(name, shape)` | One dict, read against the inner shape |
| `Each` | `Slot.each(name, shape)` | A list; the inner shape runs once per item |
| `If` | `Slot.if_(name, then[, else])` | A boolean; the branch shares the current scope |

Every slot takes modifiers:

| Modifier | Effect |
| --- | --- |
| `.required(False)` | Optional; omitted when the key is absent |
| `.default(value)` | Optional, with a fallback |
| `Slot.if_` branches | `then` and `else` are both shapes |

A `str` is iterable in Python, so an `Each` slot rejects one on purpose:
accepting it would turn a typo into a character-by-character render. `Raw` is
the exception — it does join any iterable, because joining markup is its job.

## Structure Fingerprint

`Shape.id()` is a SHA-1 fingerprint of the structure.

```python
a = Compile.shape(div(Slot.value('x')))
b = Compile.shape(div(Slot.value('x')))
c = Compile.shape(div(Slot.value('y')))

assert a.id() == b.id()
assert a.id() != c.id()
```

The fingerprint covers the tag names, the self-closing flag, every attribute,
every slot's kind, path, required flag and default, and every branch label. It
mixes in `Compile.CACHE_VERSION` and the Python minor version, so a runtime
upgrade never reuses a renderer built for the old one.

`ShapeIndex` computes it by walking the tree through the same `ShapeWalker` the
code generator uses, so "the same shape" means the same thing to both.

## `Renderer` API

```python
renderer = root.compile()

renderer.render(data)     # -> str
renderer.id               # the structure fingerprint
renderer.slots            # the root slot manifest, for the guard
renderer.source           # the generated source (empty for a prebuilt artifact)
```

`Renderer.save(path, data)` writes the rendered output to a file.

## On-Disk Cache

```python
from pure.compile.Compile import Compile

Compile.cachePath('/var/cache/purepy')   # enable
Compile.cachePath(None)                  # disable (the default)
```

- Files are content-addressed by `Shape.id()`, so a changed shape writes a new
  file rather than overwriting a live one.
- Writes are atomic: a temporary file plus `os.rename`, so concurrent workers
  cannot read a half-written renderer.
- `cachePath()` creates a missing directory with mode `0700` and refuses a
  group- or other-writable one. It does **not** check that the path is outside
  the web root — keep the cache in a dedicated directory, not `/tmp`.
- `Compile.clearCache()` returns the number of files it removed.
- `Compile.flush()` only drops the in-memory renderers; it does not touch disk.

## Per-Request Guard

```python
Compile.guard(True)
```

The guard is off by default and never changes output — it only warns, once per
subject. It reports a data key the template never reads, a near-miss standard
attribute name, and a call site that has rebuilt a shape twenty times. Turn it
on in development and in CI. See
[Troubleshooting](/guide/troubleshooting#development-guard).

## Errors

| Exception | Raised when |
| --- | --- |
| `pure.core.MissingSlotException.MissingSlotException` | A required slot had nothing to bind |
| `pure.compile.CompileException.CompileException` | A structural problem found while compiling |
| `pure.component.Registry` errors | A duplicate name, a missing file, or a factory that does not return a tree |

A `MissingSlotException` names the full slot path and either suggests the
closest key you did provide or lists the keys the scope did provide:

At the top level the message suggests the closest key you did provide:

```
slot 'title' is required but was not provided; did you mean 'titel'?
```

Inside a nested scope there is no single closest key, so it lists what the
scope did provide:

```
slot 'items.label' is required but was not provided; provided keys: 'text'.
```

## Trees with Slots Cannot Use Other Output Paths

`save()`, `print()` and the plain view all bind data through a `Shape`. A bare
tag tree that still contains `Slot` placeholders is not renderable on its own —
`Tag.render()` takes no data, and a `Slot` is not markup. Go through
`Compile.shape()` first.

## Where to go next

- [Compiled Rendering](/guide/compiled) — the model in practice
- [Artifacts & Deployment](/guide/artifacts) — the compile pipeline
- [Props and Slots](/guide/props) — the full slot reference
