---
title: Examples
description: Run the Purepy bootstrap, event-counter, and XML examples, including strict, plain, and cover routes.
---

# Examples

The repository keeps runnable examples under `examples/`. They use the same
component, compiled, and plain-view paths so you can compare a small production
shape with a dependency-free view.

## Start with a small snippet

```python
from pure.html import a, div

div(
    'Hello ',
    a('Python').href('https://www.python.org')
).class_('container').print()
```

A component adds a typed prop contract and a data-free shape. `register()` takes
the call function itself, which is where the component's name comes from:

```python
from pure.component import component, register
from pure.component.Call import Call
from pure.core.Slot import Slot
from pure.html import div, h2, p


def Card() -> Call:
    return component('Card')


register(
    Card,
    factory=lambda: div(
        h2(Slot.value('title')),
        p(Slot.value('content'))
    ).class_('card'),
    prepare=lambda title, content: {'title': title, 'content': content},
)

print(Card().title('Card Title').content('Card Content').render())
```

::: tip Why the function, not the result
The registry keys a component by the name of the function it is given, so
`register(Card, ...)` and not `register(Card(), ...)`. A lambda is rejected for
the same reason: it has no name to register under. See
[Components](/guide/components).
:::

## Children, lists, and buttons

This unit shows all three common data paths in one shape: children
through the reserved raw slot, repeated records through `Slot.each()`, and
button attributes through value slots.

```python
from pure.component import component, register
from pure.component.Call import Call
from pure.core.Slot import Slot
from pure.html import button, div, h2, li, ul


def PricingCard(*children) -> Call:
    return component('PricingCard', *children)


register(
    PricingCard,
    factory=lambda: div(
        Slot.raw('children'),
        h2(Slot.value('type')).class_('card-title'),
        ul(Slot.each('features', li(Slot.value('value')))),
        button(Slot.value('text')).class_(Slot.value('class'))
    ).class_('card'),
    prepare=lambda **props: {
        'type': props['type'],
        'features': props['features'],
        'text': props['text'],
        'class': props['class'],
    },
)

print(div(
    PricingCard(h2('Pro'))
        .type('Free')
        .features([{'value': '10 users'}, {'value': '2 GB'}])
        .text('Sign up for free')
        .class_('btn btn-lg btn-block btn-outline-primary')
).render())
```

::: warning `type` and `class` are Python built-ins
`prepare` is called with the props as keyword arguments, so it cannot spell a
parameter named `type` or `class` — those would be a syntax error, not a
shadowing one. The `**props` form above is how a prop with a built-in name is
bound. The prop names themselves are unaffected at the call site.
:::

Children are passed to the call, lists can be bound with `Slot.each()`, and
component calls implement `pure.core.Markup.Markup`, so they nest in a tag tree.
For the complete vocabulary, start with [Getting Started](/guide/getting-started)
and then [Components](/guide/components).

## Prepare the repository

The examples are not shipped in the wheel, so clone the repository and run the
commands below from its root:

```bash
git clone https://github.com/YonLD/purepy.git
cd purepy
python3 -m pip install -e .
python3 bin/pure compile --plain examples/bootstrap
python3 bin/pure compile --plain examples/event-counter
python3 bin/pure compile --plain examples/xml
```

Use `--list` to inspect discovered units. The output labels are `(component)`,
`(shape)`, and `(template)`; a page is not a separate file type:

```bash
python3 bin/pure compile --list examples
```

## Bootstrap MVC example

`examples/bootstrap` is a small MVC-style application. Controllers stay thin,
DAOs read data, services turn records into bindings, and component units own
their markup. The `features` and `pricing` pages have both a strict artifact and
a plain view. The cover page is static markup and intentionally has neither
variant.

| Route | What it renders |
| --- | --- |
| `/cover` | Static `views/cover.py`; no compile step. |
| `/pure/features` | Page function plus `*.pure.py` component artifacts. |
| `/plain/features` | `features.plain.py` after component bindings are rendered. |
| `/pure/pricing` | Page function plus `*.pure.py` component artifacts. |
| `/plain/pricing` | `pricing.plain.py` after component bindings are rendered. |

Run its front controller from the repository root:

```bash
python3 examples/bootstrap/public/index.py --serve
```

Visit `http://localhost:8000/cover`, then compare `/pure/features` with
`/plain/features` and `/pure/pricing` with `/plain/pricing`. An unknown path
returns a 404 page that lists all five routes. The same entry prints a single
page on stdout, which is the quickest way to compare the two variants without
starting a server:

```bash
python3 examples/bootstrap/public/index.py /pure/features > /tmp/strict.html
python3 examples/bootstrap/public/index.py /plain/features > /tmp/plain.html
diff /tmp/strict.html /tmp/plain.html
```

The plain loader passes the data to the generated `view()` by name. A `Call`
binding is converted to markup before that view loads, which is why the plain
file itself does not need Purepy at render time.

## Event counter example

`examples/event-counter` demonstrates a small page with a random initial value
(`random.randint(0, 100)`) and browser-side `+` / `-` controls. It has the same
strict and plain variants:

| Route | What it renders |
| --- | --- |
| `/` or `/index.py` | Redirects to `/plain`. |
| `/pure` | The page function and `counter.pure.py`. |
| `/plain` | `counter.plain.py`, with no library call in the view. |

Run it with:

```bash
python3 examples/event-counter/public/index.py --serve
```

Open `http://localhost:8000/pure` or `/plain`, then use the counter buttons. The
JavaScript and CSS are static files in `public/`; the front controller hands them
back to the built-in server, which delivers them directly.

## XML example

`examples/xml` shows XML roots, nested item shapes, optional fields, and a
`Template` builder. It exercises the `XML.state` and `XML.address` branches;
its response is XML rather than HTML:

| Route or command | What it does |
| --- | --- |
| `/` or `/index.py` | Redirects to `/plain`. |
| `/pure` | The page function and `xml.pure.py`. |
| `/plain` | `xml.plain.py`, rendered as a document. |
| `python3 examples/xml/write.py` | Writes `examples/xml/example.xml` and prints its byte count. |

Run the web version with:

```bash
python3 examples/xml/public/index.py --serve
```

Or write the file from the repository root:

```bash
python3 examples/xml/write.py
```

The XML declaration is supplied by `renderXML()`; the template itself describes
the tree. The XML shape demonstrates `Slot.each()` for a list and `Slot.if_()`
for an optional city.

## Compare strict and plain output

For ordinary data, a generated plain view is byte-identical to the strict
artifact, with the document header included when the root is an HTML or XML
document. The plain path is useful when the deployment ships only `public/` and
`views/` and does not install Purepy. It is an include-based view, not a
second template language.

For troubleshooting a missing route, stale artifact, or escaped fragment, see
[Troubleshooting](/guide/troubleshooting). For release-specific rebuild steps,
see [Upgrading](/guide/upgrading).
