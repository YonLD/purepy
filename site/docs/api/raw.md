# Raw API

**On this page**: the `Raw` marker and the `Raw` module functions.

## The class

```text
Raw(value: str)
```

`Raw` wraps a string and marks it as **already-safe markup**. Everywhere
purepy escapes — a text slot, a `Slot.value()` — a `Raw` value is emitted
verbatim instead.

| Member | What it is |
| --- | --- |
| `Raw.of(value)` | The idiomatic constructor |
| `.value` | The wrapped string, readable |
| `str(raw)` | The wrapped string |

```python
from pure.core.Raw import Raw

raw = Raw.of('<b>bold</b>')

assert raw.value == '<b>bold</b>'
assert str(raw) == '<b>bold</b>'
```

## Where it matters

`Slot.raw()` is the slot kind that takes markup. `Raw` is the *value* you hand
it, or hand to a trusted prop.

```python
from pure.compile.Compile import Compile
from pure.core.Raw import Raw
from pure.core.Slot import Slot

from pure.html import div, p

# Escaped: the tags come out as text.
escaped = Compile.shape(p(Slot.value('body')))
print(escaped({'body': '<b>x</b>'}))

# Raw: the tags come out as markup.
verbatim = Compile.shape(p(Slot.raw('body')))
print(verbatim({'body': Raw.of('<b>x</b>')}))
```

Output:

```html
<p>&lt;b&gt;x&lt;/b&gt;</p>
<p><b>x</b></p>
```

::: warning `Raw` is a promise, not a sanitizer
`Raw` disables escaping. Pass it content you produced — never request input.
For untrusted HTML, sanitize before wrapping. :::

## Iterables

`Slot.raw()` joins **any** iterable, not just a list, so a generator works:

```python
from pure.compile.Compile import Compile
from pure.core.Raw import Raw
from pure.core.Slot import Slot

from pure.html import div


def pieces():
    yield Raw.of('<b>a</b>')
    yield Raw.of('<i>b</i>')


print(Compile.shape(div(Slot.raw('items')))({'items': pieces()}))
# <div><b>a</b><i>b</i></div>
```

A `str` is iterable in Python, so it is treated as one value rather than joined
character by character — that is deliberate, and it is the opposite of what an
`each` slot does with a string.

## A rendered child component

The usual way to fill a raw slot is to render another component into it:

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div, span

badge = Compile.shape(span('New').class_('badge'))

print(Compile.shape(div(Slot.raw('body')))({'body': badge({})}))
```

A shape is data-free, so a rendered child cannot be baked into the tree
directly — `Slot.raw()` is the seam. A *plain view* cannot contain one at all,
because a plain view runs without purepy.

## Related pages

- [Props and Slots](/guide/props) — `Slot.raw()` against the other slot kinds
- [Core Classes](/api/core) — `Tag`, `Slot`, `Markup`
