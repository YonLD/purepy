# Basic Usage

This guide introduces the basic usage and syntax of Purepy.

## Creating Elements

### 1. Basic Elements

Create HTML elements using function calls:

```python
from pure.html import div, h1, p

# Create simple elements
div('Hello World')
h1('Title')
p('Paragraph content')
```

### 2. Setting Attributes

Use method chaining to set element attributes:

```python
from pure.html import div

div('Content') \
    .class_name('container') \
    .id('main') \
    .data_key('primary') \
    .to_print()
```

## Important Usage Notes

### 1. class_name Method

Since `class` is a Python keyword, Purepy uses the `class_name` method to set CSS classes:

```python
from pure.html import div

# Set CSS class
div('Content').class_name('container').to_print()
```

### 2. Attribute Naming Rules

Since `-` has special meaning in Python, attributes like `data-id` need to be written as `data_id`:

```python
from pure.html import div

div('Content') \
    .data_id('123') \
    .data_type('card') \
    .aria_label('Button') \
    .to_print()
```

Output:
```html
<div data-id="123" data-type="card" aria-label="Button">Content</div>
```

### 3. Style Handling

Use dictionaries to set styles:

```python
from pure.html import div
from pure.sty import sty

# Use sty function to handle styles
styles = sty({
    'color': 'red',
    'font-size': '16px',
    'background-color': '#f0f0f0'
})

div('Content').style(styles).to_print()
```

### 4. Class Name Handling

Use clx function to handle conditional class names:

```python
from pure.html import div
from pure.clx import clx

is_active = True
is_large = False

# Conditional classes
classes = clx('btn', {'active': is_active, 'large': is_large})
div('Button').class_name(classes).to_print()
```

## Nested Elements

### 1. Basic Nesting

```python
from pure.html import div, h1, p

div(
    h1('Title'),
    p('Content')
).to_print()
```

### 2. Complex Nesting

```python
from pure.html import div, header, nav, ul, li, a, main, section, h2, p

div(
    header(
        nav(
            ul(
                li(a('Home').href('/')),
                li(a('About').href('/about')),
                li(a('Contact').href('/contact'))
            )
        )
    ),
    main(
        section(
            h2('Welcome'),
            p('This is the main content area.')
        )
    )
).class_name('layout').to_print()
```

## Conditional Rendering

### 1. Using Conditional Expressions

```python
from pure.html import div, p

is_logged_in = True

div(
    p('Welcome back!') if is_logged_in else p('Please log in'),
    p('This is public content')
).to_print()
```

### 2. Using List Comprehensions

```python
from pure.html import div, ul, li

items = ['Apple', 'Banana', 'Orange']

div(
    ul(
        *[li(item) for item in items]
    )
).to_print()
```

## Output Methods

### 1. Convert to String

```python
from pure.html import div

element = div('Hello World')
html_string = str(element)
print(html_string)
```

### 2. Direct Print

```python
from pure.html import div

div('Hello World').to_print()
```

### 3. Save to File

```python
from pure.html import html, head, title, body, div

page = html(
    head(title('My Page')),
    body(div('Hello World'))
)

# Save to file using to_save method
page.to_save('output.html')
```

## Style Processing

### 1. Using sty Function

```python
from pure.html import div
from pure.sty import sty

# Use sty function to handle styles
styles = sty({
    'color': 'red',
    'font-size': '16px',
    'background-color': '#f0f0f0'
})

div('Content').style(styles).to_print()
```

### 2. CSS Classes

```python
from pure.html import div
from pure.clx import clx

# Use clx function to handle class names
is_active = True
is_large = False

classes = clx('container', {'active': is_active, 'large': is_large})
div('Content').class_name(classes).to_print()
```

## Best Practices

### 1. Component-based

Encapsulate repetitive code into functions:

```python
from pure.html import div, h2, p, a

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')
    link = props.get('link', '#')

    return div(
        h2(title),
        p(content),
        a('Learn More').href(link)
    ).class_name('card')

# Use component
Card({
    'title': 'Title',
    'content': 'Content',
    'link': '/more'
}).to_print()
```

### 2. Data-driven

Use data to generate content:

```python
from pure.html import div, ul, li

def ItemList(items):
    return div(
        ul(
            *[li(item) for item in items]
        )
    ).class_name('item-list')

# Usage
items = ['Item 1', 'Item 2', 'Item 3']
ItemList(items).to_print()
```

## Next Steps

- [API Reference](/en/api/) - Learn about all available tags and methods
- [TailwindCSS Integration](/en/guide/tailwindcss) - Style your components with TailwindCSS
