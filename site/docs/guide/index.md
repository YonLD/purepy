# What is Purepy?

Purepy is a Python template engine inspired by ReactJS functional components. It uses Python objects to represent HTML elements, providing a declarative way to build user interfaces that makes code more concise, maintainable, and reusable.

## Features

### 1. Declarative Rendering

With Purepy, you can describe your UI in a declarative way:

```python
from pure.html import div, h1, p

div(
    h1('Welcome to Purepy'),
    p('This is a Python template engine')
).class_name('container').print()
```

### 2. Component-based Development

Break down UI into independent, reusable Python functions:

```python
from pure.html import div, h2, p

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')

    return div(
        h2(title),
        p(content)
    ).class_name('card')

# Use components
div(
    Card({
        'title': 'Title 1',
        'content': 'Content 1'
    }),
    Card({
        'title': 'Title 2',
        'content': 'Content 2'
    })
).class_name('card-grid').print()
```

### 3. XML Support

Purepy provides powerful XML processing capabilities:

```python
from pure.core.XML import XML

# Create XML elements
xml = XML.customers(
    XML.customer(
        XML.name('Charter Group'),
        XML.address(
            XML.street('100 Main'),
            XML.city('Framingham'),
            XML.state('MA'),
            XML.zip('01701')
        )
    ).id('55000')
)

# Save to file
xml.toSave('./example.xml')
```

### 4. SVG Support

Built-in complete SVG tag support:

```python
from pure.svg import svg, circle, rect

svg(
    rect()
        .x(10)
        .y(10)
        .width(80)
        .height(80)
        .fill('none')
        .stroke('blue')
        .stroke_width(2),
    circle()
        .cx(50)
        .cy(50)
        .r(30)
        .fill('red')
).width(100).height(100).print()
```

## Why Choose Purepy?

### 1. Simple and Easy

Purepy's API is designed to be simple and intuitive with a gentle learning curve. You only need to know Python to get started quickly.

### 2. Excellent Performance

Through efficient object conversion algorithms, Purepy provides excellent rendering performance.

### 3. Component-based

Component-based development makes code easier to maintain and reuse, improving development efficiency.

### 4. Type Safety

Purepy fully supports Python's type hint system, providing a better development experience.

### 5. Lightweight

The core library is small and has no unnecessary dependencies, making it easy to integrate into existing projects.

## Quick Start

### Installation

```bash
pip install yonld-purepy
```

### Basic Usage

```python
from pure.html import div, h1, p

# Create page
div(
    h1('Welcome'),
    p('Start using Purepy!')
).class_name('container').print()
```

## Next Steps

- [Quick Start](/guide/getting-started) - Learn how to create your first Purepy application
- [Installation](/guide/installation) - Learn how to install and configure Purepy
- [Core Concepts](/guide/concepts) - Understand Purepy's core concepts in depth
