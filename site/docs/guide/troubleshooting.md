# Troubleshooting

**On this page**: the errors you are most likely to hit, what causes them, and
a short diagnostic checklist at the end.

## Installation and import errors

### `ModuleNotFoundError: No module named 'pure'`

The package is not installed in the interpreter you are running:

```bash
pip install -e .
```

`pure.__version__` resolves through the installed distribution metadata, so an
install is also what makes `pure --version` report the version from
`pyproject.toml`.

### `ModuleNotFoundError: No module named 'components.Card'`

A `*.cmp.py` file is **not** importable under its own name — the dot is part of
the file name, not a package path. Load one explicitly:

```python
from pure.loader import load_module

card = load_module('components/Card.cmp.py', 'Card')
```

or let `pure compile` and the component registry find it, which is what the CLI
and `pure check` do.

### `SyntaxError: invalid syntax` naming a function like `view(user-name_: ...)`

You are looking at generated plain-view source with a slot name that is not a
valid Python identifier. The generator already handles this: such a slot falls
back to a `data` offset, read as `data.get('user-name')`. If you are seeing it
in a hand-written view, rename the slot or pass the data offset.

## Slot and binding errors

### `MissingSlotException: slot '...' is required but was not provided`

A required slot had nothing to bind. The message names the full path, suggests
the closest key you did provide, or lists the keys the scope did provide:

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import h1

shape = Compile.shape(h1(Slot.value('title')))
shape({'titel': 'Users'})
# MissingSlotException: slot 'title' is required but was not provided;
#   did you mean 'titel'?
```

For data that really is optional, say so in the shape:

```python
from pure.core.Slot import Slot

h1(Slot.value('subtitle').required(False))          # omitted when absent
h1(Slot.value('subtitle').default('(none)'))        # falls back to a value
```

### A child or each-slot value is rejected

`Slot.child()` and `Slot.each()` each open a nested data scope, and the value
must have the shape the template reads:

```python
from pure.core.Slot import Slot

from pure.html import div

Compile.shape(div(Slot.child('meta', inner_shape)))
# bind meta={'label': 'm'} — one dict, with the child shape's own slots
```

For an `each` slot the value must be a list of such objects. A string is
rejected on purpose: `str` is iterable in Python, so accepting it would turn a
typo into a silent character-by-character render.

### `did you mean '...'?` in a message

Two different checks produce this, and they fire at different times:

- **Static** — `pure check` reports it before anything renders, from the shape
  versus the declared `Prop`.
- **Runtime** — the development guard reports a misspelled standard attribute
  name, or a data key the template never reads. See
  [Development Guard](#development-guard).

### A rendered child component is missing

A `Markup` value cannot be baked into a shape. A shape is data-free: a rendered
child component is runtime behaviour, so it enters through `Slot.raw()`, and a
plain view cannot contain one at all.

## Escaping and markup

### Markup shows up as escaped text

By design. `Slot.value()` escapes; `Slot.raw()` does not. If trusted markup
arrives through `Slot.value()` you will see its tags as text — pass it as raw
instead.

```python
from pure.compile.Compile import Compile
from pure.core.Raw import Raw
from pure.core.Slot import Slot

from pure.html import p

print(Compile.shape(p(Slot.raw('body')))({'body': Raw.of('<b>x</b>')}))
# <p><b>x</b></p>  emitted verbatim

print(Compile.shape(p(Slot.value('body')))({'body': '<b>x</b>'}))
# <p>&lt;b&gt;x&lt;/b&gt;</p>  escaped
```

## Artifacts, cache, and performance

### The output is old, or an artifact asks you to run `pure compile`

The registry serves a `*.pure.py` artifact when it is not older than the unit
file. Two different messages mean two different things:

- **`stale purepy artifact ... run 'pure compile' to rebuild`** — the artifact
  was built against a different `Compile.CACHE_VERSION`. Rebuild it; do not edit
  it.
- **Your edit did not take effect** — you changed the unit but the artifact is
  still newer than it. Recompile.

```bash
pure compile src --check     # reports `stale:` and exits 1
```

### A shape is rebuilt on every request

Turn on the development guard; it warns once per call site once a call site has
reached twenty calls, which is the signature of a shape that is not memoized:

```python
from pure.compile.Compile import Compile

Compile.guard(True)
```

Then build each shape once:

```python
_shape = None


def shape():
    global _shape
    if _shape is None:
        _shape = Compile.shape(tree)
    return _shape
```

## Development Guard

`Compile.guard(True)` — or the `PURE_COMPILE_GUARD=1` environment variable —
turns on three development checks. Each finding is reported once per subject,
so a loop does not produce a wall of warnings.

| Warning | Meaning |
| --- | --- |
| `unknown data key 'x' (did you mean 'y'?)` | The call bound a key the template never reads |
| `Element 'div' has no standard attribute 'hreff'; did you mean 'href'?` | A near-miss attribute name; off for custom and `data-*` names |
| `Compile.shape() was called 20 times from <file>:<line>` | A call site is rebuilding a shape instead of memoizing it |

The guard is off by default and never affects output — it only warns. Turn it on
in development and in CI, not in production.

::: warning `Compile.guard(False)` is not the same as a clean state
`DevMode.reset()` returns the switch to "resolve from the environment", which
undoes a `guard(True)` that came before it. If a test sets the guard and then
resets, it will silently stop guarding. :::

## CLI and check errors

### `pure compile` reports `is claimed by both ... and ...`

Two files resolve to the same artifact name — typically `Box.shape.py` and
`Box.cmp.py` in one directory, since `box.pure.py` would be written twice. The
run fails and neither file is compiled; rename one base name.

### `pure check` reports `no component unit is registered here`

The file is a `*.cmp.py` unit but calls `register()` never ran — usually a
missing import, or a factory defined but not registered.

### `pure compile` needs the component registry

A `*.cmp.py` unit can only be compiled by the CLI, which wires the registry in.
`ArtifactCommand()` constructed directly cannot resolve one; that is why the
library tells you to go through `bin/pure`.

## A short diagnostic checklist

1. **Run the contract check.** `pure check src` catches most binding problems
   statically, before anything renders.
2. **Turn on the guard.** `Compile.guard(True)` and re-run; the warnings name
   the file and line.
3. **Compare the paths.** For one shape, `shape(data)` and
   `shape.compile().render(data)` must produce identical output. If they do
   not, it is a purepy bug — please report it with the shape.
4. **Check artifact freshness.** `pure compile src --check`.
5. **Bisect the data.** Render with the smallest input that still fails; the
   exception message names the full slot path.

## Where to go next

- [Compiled Rendering](/guide/compiled) — how shapes become renderers
- [Artifacts & Deployment](/guide/artifacts) — the compile pipeline
- [Props and Slots](/guide/props) — the full slot reference
