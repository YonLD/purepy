# Introduction

Welcome to Purepy! This is a Python template engine inspired by ReactJS that allows you to create HTML, SVG, and XML content in a functional way.

## What is Purepy?

Purepy is a modern Python template engine that borrows the component-based thinking from ReactJS, enabling you to:

- **Functional Programming**: Every HTML tag is a function
- **Component-based Development**: Break UI into reusable components
- **Type Safety**: Complete type hint support
- **Method Chaining**: Fluent API design
- **Utility Functions**: Built-in style and class name processing tools

## Core Features

### 1. Intuitive Syntax

```python
from pure.html import div, h1, p

# Creating HTML structure is as simple as calling functions
content = div(
    h1('Welcome to Purepy'),
    p('This is a modern Python template engine')
).class_name('welcome')
```

### 2. Component-based Thinking

```python
def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')
    
    return div(
        h1(title).class_name('card-title'),
        p(content).class_name('card-content')
    ).class_name('card')

# Using components
my_card = Card({
    'title': 'Card Title',
    'content': 'Card Content'
})
```

### 3. Powerful Utility Functions

```python
from pure.clx import clx
from pure.sty import sty

# Conditional class names
classes = clx('btn', {'active': is_active, 'disabled': is_disabled})

# Style objects
styles = sty({
    'color': 'red',
    'font-size': '16px',
    'padding': '10px'
})
```

## Design Philosophy

### Function-first

Purepy adopts a functional programming paradigm where every HTML tag is a pure function, bringing the following benefits:

- **Predictability**: Same input always produces same output
- **Testability**: Functions are easy to unit test
- **Composability**: Small functions can be composed into complex structures
- **Reusability**: Components can be reused in different places

### Declarative Syntax

Unlike traditional template engines, Purepy uses declarative syntax:

```python
# Declarative: describe what you want
div(
    h1('Title'),
    p('Content')
).class_name('container')

# Instead of imperative: describe how to do it
# template = "<div class='container'><h1>Title</h1><p>Content</p></div>"
```

### Type Safety

Purepy provides complete type hint support:

```python
from typing import Dict, Any
from pure.html import div, h1, p

def Card(props: Dict[str, Any]) -> 'HTML':
    title: str = props.get('title', '')
    content: str = props.get('content', '')
    
    return div(
        h1(title),
        p(content)
    ).class_name('card')
```

## Comparison with Other Template Engines

### vs Jinja2

```python
# Jinja2
template = """
<div class="card">
    <h1>{{ title }}</h1>
    <p>{{ content }}</p>
</div>
"""

# Purepy
def Card(props):
    return div(
        h1(props['title']),
        p(props['content'])
    ).class_name('card')
```

**Purepy Advantages:**
- Complete Python syntax support
- Better IDE support (auto-completion, refactoring, etc.)
- Type checking
- Easier debugging

### vs Django Templates

```html
<!-- Django Template -->
<div class="card">
    <h1>{{ title }}</h1>
    <p>{{ content }}</p>
    {% if user.is_authenticated %}
        <button>Edit</button>
    {% endif %}
</div>
```

```python
# Purepy
def Card(props):
    user = props.get('user')
    
    return div(
        h1(props['title']),
        p(props['content']),
        button('Edit') if user and user.is_authenticated else None
    ).class_name('card')
```

**Purepy Advantages:**
- Uses standard Python syntax
- Stronger logical expression capabilities
- Better code reuse

## Use Cases

Purepy is particularly suitable for the following scenarios:

### 1. Static Site Generation

```python
from pure.html import html, head, title, body, div, h1, p

def generate_blog_post(post):
    return html(
        head(title(post['title'])),
        body(
            div(
                h1(post['title']),
                p(post['content'])
            ).class_name('post')
        )
    )

# Generate multiple pages
for post in posts:
    page = generate_blog_post(post)
    page.to_save(f'posts/{post["slug"]}.html')
```

### 2. Email Templates

```python
def email_template(user, content):
    return html(
        head(title('Email Notification')),
        body(
            div(
                h1(f'Hello, {user.name}!'),
                div(content),
                p('Thank you for using our service')
            ).class_name('email-container')
        )
    )
```

### 3. Report Generation

```python
def generate_report(data):
    return html(
        head(title('Data Report')),
        body(
            div(
                h1('Monthly Report'),
                *[
                    div(
                        h2(item['title']),
                        p(f'Value: {item["value"]}')
                    ).class_name('report-item')
                    for item in data
                ]
            ).class_name('report')
        )
    )
```

### 4. Component Library Development

```python
# Create reusable UI component library
def Button(props):
    variant = props.get('variant', 'primary')
    size = props.get('size', 'medium')
    
    classes = clx('btn', f'btn-{variant}', f'btn-{size}')
    
    return button(props.get('children', '')).class_name(classes)

def Modal(props):
    return div(
        div(
            h2(props.get('title', '')),
            div(props.get('children', '')),
            Button({'children': 'Close', 'variant': 'secondary'})
        ).class_name('modal-content')
    ).class_name('modal')
```

## Learning Path

We recommend learning Purepy in the following order:

1. **[Installation](/en/guide/installation)** - Set up development environment
2. **[Getting Started](/en/guide/getting-started)** - Create your first application
3. **[Core Concepts](/en/guide/concepts)** - Understand core concepts
4. **[Basic Usage](/en/guide/basic-usage)** - Master basic syntax
5. **[Components](/en/guide/components)** - Learn component-based development
6. **[Props](/en/guide/props)** - Understand the props system
7. **[TailwindCSS Integration](/en/guide/tailwindcss)** - Style processing

## Community and Support

- **GitHub**: [https://github.com/YonLD/purepy](https://github.com/YonLD/purepy)
- **Documentation**: The documentation you're reading
- **Issue Reporting**: Report issues through GitHub Issues

## Next Steps

Now that you understand the basic concepts of Purepy, you can start:

- [Install Purepy](/en/guide/installation)
- [Getting Started Tutorial](/en/guide/getting-started)
- [View API Documentation](/en/api/)

Let's start building amazing applications!
