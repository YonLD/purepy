# HTML Class

`pure.core.HTML.HTML` extends the Tag class, specifically for HTML tags.

## Creating HTML Elements

Standard tags come from the `pure.html` functions. Any other tag name works by
reading the tag name off the class: `HTML.myWidget('x')` builds
`<myWidget>x</myWidget>`, and a name that is not a valid Python identifier goes
through the dynamic form, `getattr(HTML, 'user-card')('x')`.

### 1. Functions (Standard tags)

```python
from pure.html import div, p, span

d = div('Content')
paragraph = p('Paragraph')
highlighted = span('Text').class_('highlight')
```

Functions follow tag names one to one. A tag whose name is a Python keyword
cannot name a function, so `<class>` has no module-level function; the dynamic
form on the class covers it, as it does in purephp.

Unlike purephp, no alias is needed for `<var>`, `<use>` or `<switch>`: none of
those is a Python keyword, so `pure.html.var()`, `pure.svg.use()` and
`pure.svg.switch()` carry their own names.

### 2. Tag names read off the class

```python
from pure.core.HTML import HTML

# Works with any tag name: the attribute read is the tag name
element = HTML.customTag('Content').class_('custom')
# <customTag class="custom">Content</customTag>

component = HTML.myWebComponent(HTML.header('Header'))

# A hyphenated custom element goes through the dynamic form
web_component = getattr(HTML, 'user-card')('Content')
# <user-card>Content</user-card>
```

**Use cases:**
- Custom HTML tags
- Web components
- Non-standard HTML elements

::: tip
`div` and `HTML.div` build the same element. The class form reads better where
the tag name is computed, since a module-level function has to be looked up by
name as well.
:::

## Save Methods

### `save(path, header=None)`

Saves the HTML element to a file. When `header` is omitted, `<!DOCTYPE html>`
is written first.

```python
from pure.html import html, head, title, body, div

page = html(
    head(title('Page Title')),
    body(div('Page Content'))
)

written = page.save('output.html')
if written is not None:
    print('File saved successfully, wrote {} bytes'.format(written))
```

The return value is the number of bytes written, and the file is UTF-8 whatever
the locale says, so the count is the count the file holds.

## Self-Closing Tags

The HTML class automatically recognizes the following self-closing tags:
- `area`, `base`, `br`, `col`, `embed`, `hr`, `img`, `input`, `link`, `meta`, `source`, `track`, `wbr`

```python
from pure.html import img, br, hr

# These tags are automatically set as self-closing
img().src('image.jpg').alt('Image')
br()
hr()
```

## Examples

### Basic HTML Structure

```python
from pure.html import html, head, meta, title, body, div, h1, p
from pure.utils import renderHTML

page = html(
    head(
        meta().charset('UTF-8'),
        meta().name('viewport').content('width=device-width, initial-scale=1.0'),
        title('My Page')
    ),
    body(
        div(
            h1('Welcome'),
            p('This is my website.')
        ).class_('container')
    )
).lang('en')

print(renderHTML(page))
```

### Form Creation

```python
from pure.html import form, div, label, input, textarea, button
from pure.utils import renderHTML

contact_form = form(
    div(
        label('Name:').for_('name'),
        input().type('text').id('name').name('name').required(True)
    ).class_('form-group'),
    div(
        label('Email:').for_('email'),
        input().type('email').id('email').name('email').required(True)
    ).class_('form-group'),
    div(
        label('Message:').for_('message'),
        textarea('').id('message').name('message').rows('5').required(True)
    ).class_('form-group'),
    button('Send Message').type('submit')
).method('POST').action('/contact')

print(renderHTML(contact_form))
```

::: tip Two spellings for a keyword
`for_` is the trailing-underscore escape for the Python keyword and writes
`for="name"`, which is what the element needs. `htmlFor` is an alias for the
same thing. Neither is `html_for`: that is an ordinary attribute name and
renders as `html-for="name"`, exactly as it does in purephp.
:::

::: tip `required` is a boolean attribute here
`required(True)` renders `required="required"` and `required(False)` drops the
attribute, which is the rule every boolean attribute follows. A boolean written
into a *text* position is different: it is cast the way PHP casts it, so
`div(True)` renders `1` and `div(False)` renders nothing.
:::

### Custom Elements

```python
from pure.core.HTML import HTML

card = HTML.cardComponent(
    HTML.cardHeader('Card Title'),
    HTML.cardBody('Card content goes here'),
    HTML.cardFooter('Card footer')
).data_component('card').class_('custom-card')

print(card.render())
```

### Large Lists

```python
from pure.html import li, ul
from pure.utils import renderHTML

# A list is passed as one child, so the whole list is built in one pass
items = [li('Item {}'.format(i)) for i in range(1, 1001)]

print(renderHTML(ul(items)))
```
