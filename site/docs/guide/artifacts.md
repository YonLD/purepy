# Artifacts & Deployment

**Prerequisites**: [Compiled Rendering](/guide/compiled), [Components](/guide/components) · **On this page**: `pure compile` artifacts, `pure check`, plain views, and deployment caching.

The disk cache still rebuilds the shape tree on every request. To deploy
without building shapes at all, compile them ahead of time with the `pure`
command.

## Precompiled Artifacts

```bash
pure compile src
```

Every `*.cmp.py` unit is compiled into a sibling `*.pure.py` artifact. An
artifact declares the shape fingerprint and exposes a `Renderer`, so it needs
neither the shape tree nor the compile cache:

```python
from pure.compile.Internal.ArtifactCompiler import ArtifactCompiler

page = ArtifactCompiler.loadRenderer('page.pure.py')

data = {'title': 'Users', 'items': [{'label': 'Ada'}]}

print(page.render(data))
page.save('out.html', data)
```

::: tip Advanced: standalone `*.shape.py` templates
Besides units, `pure compile` also discovers `*.shape.py` files that expose a
`shape` attribute — a template with no call function. Components are the
recommended form; reach for a shape file only when there is no component to own
the template.
:::

- `pure compile <path>...` accepts files and directories (searched
  recursively), discovers both `*.cmp.py` units and `*.shape.py` templates, and
  skips files whose content is already current: the shape is still loaded and
  compiled (so a change in anything it pulls in is picked up), but an
  up-to-date file is reported as `unchanged:` instead of rewritten. A typical
  `--list` line is `Card -> components/Card.cmp.py (component)`; a standalone
  template is reported as `views/page.shape.py (shape)`, and a `@Template()`
  builder as `pageShape -> views/page.cmp.py (template)`.
- `--list` prints those labels without compiling. `--check` writes nothing and
  exits with code 1 when an artifact is stale or missing, which fits a CI step.
  `--plain` also writes the dependency-free view described below, and
  `--check --plain` covers both flavours.
- Artifacts render the same output as the runtime compiler — the test suite
  asserts this byte for byte — and an artifact carries the root slot manifest
  (`Renderer.slots`), so the development guard can report bindings the template
  never reads without rebuilding the shape tree.
- `Renderer.source` is empty for artifacts: the file itself is the source.

The generated artifact is illustrative, not an application API. Its
`SlotRuntime` import is emitted by `pure compile`; application code should
continue to call `renderer.render()`:

```python
# generated shape of the template above — for reading, not for calling
from pure.compile.Internal.SlotRuntime import SlotRuntime


def render(v):
    out = []
    out.append('<div')
    out.append(' class="card"')
    out.append('>')
    out.append('<h1>')
    out.append(SlotRuntime.text(v, 'title'))
    out.append('</h1>')
    out.append('<ul>')
    for v1 in SlotRuntime.items(v, 'items'):
        out.append('<li>')
        out.append(SlotRuntime.text(v1, 'label'))
        out.append('</li>')
    out.append('</ul>')
    out.append('</div>')
    return ''.join(out)
```

Dynamic values read their slot through `SlotRuntime`, which keeps the compiled
semantics in one place: a required slot raises
`pure.core.MissingSlotException.MissingSlotException`, an optional slot falls
back to its compiled default, and values are escaped or coerced exactly like the
flat renderer does.

## Plain Views

`--plain` writes a second artifact, a `*.plain.py` view: a self-contained
`view()` function with no dependency on purepy at all.

```bash
pure compile --plain src
```

```python title="page.plain.py"
from html import escape as _escape
from typing import Any, Dict, Iterable, List, Optional


def _text(value):
    """Escape a value for a text position, like the compiled renderer."""
    return '' if value is None else _escape(str(value), quote=False)


def view(title: Optional[str] = None, items: Optional[Iterable[Any]] = None) -> str:
    out = []
    out.append('<div')
    out.append(' class="card"')
    out.append('>')
    out.append('<h1>')
    out.append(_text(title))
    out.append('</h1>')
    out.append('<ul>')
    for i1 in (items or ()):
        out.append('<li>')
        out.append(_text(i1.get('label')))
        out.append('</li>')
    out.append('</ul>')
    out.append('</div>')
    return ''.join(out)
```

A plain view is a drop-in for a server-rendered template in a host that
supports Python and has no purepy installed. It renders the same bytes as the
compiled renderer, and the test suite asserts that for every shape the project
covers.

::: warning A plain view is not a component
A plain view binds its root slots as **parameters**. A slot name that cannot be
a parameter — `user-name` — falls back to a `data` offset, so the view takes it
from `data.get('user-name')` instead. Rendered child components cannot appear in
a plain view: a component is purepy runtime behaviour, and the view has to run
without purepy. :::

## The Contract Check

`pure check` verifies the contract of a unit without rendering anything. It
loads every unit, walks its shape and reports a conflict between what the
template reads and what the call site binds:

```bash
pure check src
```

```
checked 23 unit(s): 0 error(s), 0 warning(s).
```

The checks include:

| Check | Reported as |
| --- | --- |
| A required slot is never provided | `slot 'title' is required but was not provided` |
| A declared prop does not match the shape's slots | `prop $x declares ... but slot 'x' reads ...` |
| A list slot receives a non-list | `slot 'items' must be an array, string given` |
| A unit file registers nothing, or more than one unit | `no component unit is registered here` / `2 component units are registered here` |
| Two files claim the same artifact | `is claimed by both ... and ...` |

It exits 1 when anything is wrong, which makes it a CI step:

```yaml
- run: pure check src --strict
```

## Deploying

A deployment that compiles ahead of time needs three things:

1. **Artifacts on disk.** Run `pure compile src` during the build, and ship the
   `*.pure.py` files with the release.
2. **A writable cache directory**, or no cache at all. If `Compile.cachePath()`
   is not set, nothing is written at request time and the artifacts are the only
   compiled code in play.
3. **A version match.** An artifact records the `Compile.CACHE_VERSION` it was
   built with and refuses to load under a different one, saying
   `stale purepy artifact ... run 'pure compile' to rebuild` rather than failing
   somewhere deeper. Bump the cache version whenever the generated code changes
   shape.

```python
from pure.compile.Compile import Compile

# The artifacts are precompiled; no request-time cache needed.
Compile.cachePath(None)
```

A typical deploy then looks like:

```bash
pure check src                 # fail the build on a contract error
pure compile src --check       # artifacts are current
```

## Freshness

The registry serves a `*.pure.py` artifact when it exists and is **not older
than** the unit file. The unit factory then does not run at all. If you edit a
unit, recompile — otherwise the stale artifact keeps serving, which is what makes
the deployment story fast but easy to get wrong locally.

```bash
pure compile src --check       # reports `stale:` and exits 1
```

## Where to go next

- [Compiled Rendering](/guide/compiled) — how the renderer is produced
- [Troubleshooting](/guide/troubleshooting) — when a check or a compile fails
- [CLI Reference](/api/) — every `pure` flag
