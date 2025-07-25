# Utility Functions

Purepy provides several utility functions to simplify development. These functions are automatically used when setting element attributes.

## clx Function

The `clx` function is used to merge class names, supporting strings, arrays, and conditional class names.

### Basic Usage

```python
from pure.clx import clx

# Merge multiple string class names
classes = clx('btn', 'btn-primary', 'large')
print(classes)  # Output: btn btn-primary large
```

### Conditional Class Names

```python
from pure.clx import clx

is_active = True
is_disabled = False

classes = clx(
    'btn',
    'active' if is_active else None,
    'disabled' if is_disabled else None
)
print(classes)  # Output: btn active
```

### Dictionary Support

```python
from pure.clx import clx

classes = clx(
    'btn',
    {
        'btn-primary': True,
        'active': True,
        'disabled': False,
        'large': None
    }
)
print(classes)  # Output: btn btn-primary active
```

### Built-in Usage in class_name() Method

The `class_name()` method has built-in `clx` function support, allowing you to pass multiple arguments directly:

```python
from pure.html import div

is_active = True
size = 'large'

div('content').class_name('btn', 'btn-primary', 'active' if is_active else None, size).to_print()

# Equivalent to
from pure.clx import clx

classes = clx('btn', 'btn-primary', 'active' if is_active else None, size)
div('content').class_name(classes).to_print()
```

## sty Function

The `sty` function is used to convert style dictionaries to CSS strings.

### Basic Usage

```python
from pure.sty import sty

styles = sty({
    'background-color': 'red',
    'height': '36px',
    'border': '1px solid #fff'
})
print(styles)  # Output: background-color: red; height: 36px; border: 1px solid #fff;
```

### Conditional Styles

```python
from pure.sty import sty

is_visible = True
color = 'blue'

styles = sty({
    'color': color,
    'display': 'block' if is_visible else 'none',
    'opacity': 1 if is_visible else 0,
    'margin': None,  # Will be ignored
    'padding': False # Will be ignored
})
print(styles)  # Output: color: blue; display: block; opacity: 1;
```

### Built-in Usage in style() Method

The `style()` method has built-in `sty` function support, allowing you to pass dictionaries directly:

```python
from pure.html import div

div('content').style({
    'background-color': '#f0f0f0',
    'padding': '20px',
    'border-radius': '8px',
    'margin': '10px 0'
}).to_print()

# Equivalent to
from pure.sty import sty

styles = sty({
    'background-color': '#f0f0f0',
    'padding': '20px',
    'border-radius': '8px',
    'margin': '10px 0'
})
div('content').style(styles).to_print()
```

## raw_html Function

The `raw_html` function is used to insert raw HTML content that won't be escaped.

### Basic Usage

```python
from pure.html import div
from pure.raw import raw_html

div(
    raw_html('<strong>This is bold text</strong>'),
    raw_html('<em>This is italic text</em>')
).to_print()
```

### Security Considerations

When using `raw_html`, ensure the content is safe to avoid XSS attacks:

```python
from pure.html import div
from pure.raw import raw_html
import html

# Safe usage
user_input = "<script>alert('xss')</script>"
safe_html = html.escape(user_input)
div(raw_html(safe_html)).to_print()

# Or use known safe HTML
icon_html = '<svg><path d="..."/></svg>'
div(raw_html(icon_html)).to_print()
```

## raw_xml Function

The `raw_xml` function is used to insert raw XML content:

```python
from pure.raw import raw_xml

xml_content = raw_xml('<item id="1">content</item>')
```

## Practical Examples

### Dynamic Button Component

```python
from pure.html import button

def Button(props):
    text = props.get('text', '')
    variant = props.get('variant', 'primary')
    size = props.get('size', 'medium')
    disabled = props.get('disabled', False)
    loading = props.get('loading', False)

    return button(
        'Loading...' if loading else text
    ).class_name(
        'btn',
        f'btn-{variant}',
        f'btn-{size}',
        'disabled' if disabled else None,
        'loading' if loading else None
    ).style({
        'opacity': 0.6 if disabled else 1,
        'cursor': 'not-allowed' if disabled else 'pointer'
    }).disabled(disabled)

# Usage example
Button({
    'text': 'Submit',
    'variant': 'success',
    'size': 'large',
    'loading': False
}).to_print()
```

### Responsive Card Component

```python
from pure.html import div, h3, p

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')
    featured = props.get('featured', False)
    theme = props.get('theme', 'light')

    return div(
        h3(title).class_name('card-title'),
        p(content).class_name('card-content')
    ).class_name(
        'card',
        f'card-{theme}',
        'card-featured' if featured else None
    ).style({
        'border-width': '2px' if featured else '1px',
        'box-shadow': '0 4px 12px rgba(0,0,0,0.15)' if featured else '0 2px 4px rgba(0,0,0,0.1)',
        'background-color': '#333' if theme == 'dark' else '#fff',
        'color': '#fff' if theme == 'dark' else '#333'
    })

# Usage example
Card({
    'title': 'Featured Card',
    'content': 'This is a featured card content',
    'featured': True,
    'theme': 'dark'
}).to_print()
```

## Next Steps

- [Basic Usage](/en/guide/basic-usage) - Learn basic syntax and usage
- [Components](/en/guide/components) - Learn how to create and use components
- [TailwindCSS Integration](/en/guide/tailwindcss) - Learn how to work with TailwindCSS
