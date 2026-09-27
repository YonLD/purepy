# Tag API

**On this page**: the base element class — attribute setters, getters, the
output methods, and how dynamic attributes work.

`Tag` is the class every element class derives from: `HTML`, `SVG` and `XML`.
The per-tag functions (`div()`, `span()`, `path()`, …) all return a `Tag`
subclass instance.

```python
from pure.html import div, span

tag = div(span('x')).class_('card')
```

## Attribute Setters

Attributes are set by method call, and an unknown method name becomes an
attribute:

```python
from pure.html import a, div

div().id('main').data_id('7').title('a tip')
a('x').href('/target').rel('help')
```

`data_id` becomes `data-id`, `aria_label` becomes `aria-label` — an underscore
becomes a hyphen. Two exceptions:

- A **trailing** underscore escapes a Python keyword: `for_()` renders
  `for="…"`, `class_()` renders `class="…"`, `is_()` renders `is="…"`. A
  trailing underscore anywhere else is still a keyword check, so `data_id()`
  keeps working.
- The exact names purephp uses are available as methods: `class_name()` and
  `className()` both render `class`.

### Values

| Value | Rendered as |
| --- | --- |
| `str`, `int`, `float` | The escaped value |
| `True` | The bare name, so `checked` |
| `False` or `None` | The attribute is omitted |
| `Slot` | The slot's value, escaped in attribute position |
| `Raw` | Emitted verbatim |

```python
from pure.html import input, label

input().type('checkbox').checked(True).disabled(False)
# <input type="checkbox" checked="checked" />

label().class_('a', 'b', 'c')     # space-joined
```

An array-valued attribute uses a `Slot`, or `style()` / `class_()`; passing a
list to a plain attribute is rejected rather than silently joined.

### Batch

```python
div().set_attrs({'data-id': '7', 'id': 'main', 'hidden': True})
```

`set_attrs(props: dict) -> Tag` sets many at once and returns the tag, so it
chains. It is the right call when the keys are computed.

## Getters

| Method | Returns |
| --- | --- |
| `get_tag_name()` | The tag name, e.g. `'div'` |
| `get_attrs()` | The attribute dict, `Slot` values included |
| `get_attr(key)` | One value, or `None` |
| `get_children()` | The children list: `str`, `Raw`, `Tag` or `Slot` |
| `get_self_close()` | Whether the tag is self-closing |
| `export()` | The whole tree as a dict — what the compiler walks |
| `to_JSON()` | The tree as a JSON string |
| `tree()` | The underlying `Tag` node |

## Output

```text
render() -> str
save(path: str, header: Optional[str] = None) -> None
print() -> None
```

- `render()` returns the HTML. It takes no data: a tag tree that still holds
  `Slot` placeholders is not renderable on its own — go through
  `Compile.shape()`.
- `save(path, header=None)` writes to a file, prefixed with the class's default
  header: `<!DOCTYPE html>` for `HTML`, `<?xml version="1.0"?>` for `SVG` and
  `XML`. That prefix is **unconditional** — saving a bare `div()` still writes
  the doctype, which is what purephp does too. Pass `header=''` for a bare
  fragment, or `header='...'` to supply your own.
- `print()` writes the rendering to stdout.

```python
from pure.html import div, html, body

page = html(body(div('content')))
page.save('index.html')
# <!DOCTYPE html><html><body><div>content</div></body></html>

div('a fragment').save('fragment.html', '')
# a fragment
```

::: tip Output is never re-indented
Purepy emits exactly the bytes it renders. Markup you wrote on several lines
comes out on one line. :::

## Development Guards

| Method | What it does |
| --- | --- |
| `guardAttributeName(key)` | Hook called before an attribute is set; a no-op on the base class |
| `guardStandardAttribute(key)` | Warns once per name on a near-miss standard attribute, under the guard |

`HTML` and `SVG` override the first to call the second; `XML` leaves it a no-op
because an XML tree names its own attributes. See
[Troubleshooting](/guide/troubleshooting#development-guard).

## Document Roots

| Method | What it does |
| --- | --- |
| `isDocumentRoot()` | Whether this tag starts a document |
| `documentHeader()` | The header a document root needs |
| `defaultHeader()` | The subclass's own default header |

## Subclass notes

| Class | Header | Notes |
| --- | --- | --- |
| `HTML` | `<!DOCTYPE html>` | Void elements reject children; renders self-closing as `<br />` |
| `SVG` | `<?xml version="1.0"?>` | Attributes keep their camelCase (`viewBox`) |
| `XML` | `<?xml version="1.0"?>` | Any element name; no standard attribute list |

## Related pages

- [HTML Tags](/api/html-tags) — the full element list
- [Core Classes](/api/core) — `Slot`, `Raw`, `Escaper`
- [Basic Usage](/guide/basic-usage) — attributes in practice
