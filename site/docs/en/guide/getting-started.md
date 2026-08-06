# Getting Started

This guide will help you get started with Purepy quickly.

## Installation

Install Purepy using pip:

```bash
pip install yonld-purepy
```

## Your First Purepy Application

Let's create a simple HTML page using Purepy:

```python
from pure.html import html, head, title, body, div, h1, p

def create_page():
    return html(
        head(
            title('My First Purepy Page')
        ),
        body(
            div(
                h1('Welcome to Purepy!'),
                p('This is your first page created with Purepy.')
            ).class_name('container')
        )
    )

# Generate and save the page
page = create_page()
page.to_save('index.html')
print("Page created: index.html")
```

Run this script and you'll get an `index.html` file with the following content:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My First Purepy Page</title>
</head>
<body>
    <div class="container">
        <h1>Welcome to Purepy!</h1>
        <p>This is your first page created with Purepy.</p>
    </div>
</body>
</html>
```

## Basic Concepts

### 1. Function-based Elements

Every HTML tag is a function that returns an element object:

```python
from pure.html import div, h1, p

# Create elements
title = h1('Page Title')
content = p('Page content')
container = div(title, content)
```

### 2. Method Chaining

Set attributes using method chaining:

```python
from pure.html import div

element = div('Content') \
    .class_name('my-class') \
    .id('my-id') \
    .data_value('123')
```

### 3. Nested Elements

Elements can contain other elements:

```python
from pure.html import div, ul, li

menu = div(
    ul(
        li('Home'),
        li('About'),
        li('Contact')
    )
).class_name('navigation')
```

## Working with Attributes

### CSS Classes

Use `class_name()` method (since `class` is a Python keyword):

```python
from pure.html import div

div('Content').class_name('btn btn-primary')
```

### Data Attributes

Use underscore instead of dash for attribute names:

```python
from pure.html import div

div('Content') \
    .data_id('123') \
    .data_type('card') \
    .aria_label('Button')
```

This generates:
```html
<div data-id="123" data-type="card" aria-label="Button">Content</div>
```

## Using Utility Functions

### Class Names with clx

```python
from pure.html import div
from pure.clx import clx

is_active = True
is_large = False

classes = clx('btn', {
    'active': is_active,
    'large': is_large
})

div('Button').class_name(classes)
```

### Styles with sty

```python
from pure.html import div
from pure.sty import sty

styles = sty({
    'color': 'red',
    'font-size': '16px',
    'padding': '10px'
})

div('Styled content').style(styles)
```

## Creating Components

Organize your code by creating reusable components:

```python
from pure.html import div, h2, p, a

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')
    link = props.get('link', '#')

    return div(
        h2(title).class_name('card-title'),
        p(content).class_name('card-content'),
        a('Read More').href(link).class_name('card-link')
    ).class_name('card')

# Use the component
my_card = Card({
    'title': 'Welcome',
    'content': 'This is a sample card.',
    'link': '/welcome'
})

my_card.to_print()
```

## Building a Complete Page

Here's a more complete example:

```python
from pure.html import html, head, meta, title, link, body, header, nav, ul, li, a, main, div, h1, p, footer

def create_website():
    return html(
        head(
            meta().charset('UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1.0'),
            title('My Website'),
            link().rel('stylesheet').href('styles.css')
        ),
        body(
            header(
                nav(
                    ul(
                        li(a('Home').href('/')),
                        li(a('About').href('/about')),
                        li(a('Contact').href('/contact'))
                    ).class_name('nav-list')
                ).class_name('navbar')
            ),

            main(
                div(
                    h1('Welcome to My Website'),
                    p('This website was built using Purepy, a Python template engine inspired by ReactJS.')
                ).class_name('hero')
            ),

            footer(
                p('© 2024 My Website. All rights reserved.')
            ).class_name('footer')
        )
    )

# Generate the website
website = create_website()
website.to_save('website.html')
```

## Working with Lists

Generate dynamic content using Python's list comprehensions:

```python
from pure.html import div, ul, li

def create_todo_list(items):
    return div(
        ul(
            *[li(item) for item in items]
        ).class_name('todo-list')
    ).class_name('todo-container')

# Usage
todos = ['Learn Purepy', 'Build a website', 'Deploy to production']
todo_list = create_todo_list(todos)
todo_list.to_print()
```

## Conditional Rendering

Use Python's conditional expressions for dynamic content:

```python
from pure.html import div, p

def welcome_message(user=None):
    return div(
        p(f'Welcome back, {user}!') if user else p('Please log in'),
        p('This is the main content area.')
    ).class_name('welcome')

# Usage
logged_in_view = welcome_message('John')
guest_view = welcome_message()
```

## Next Steps

Now that you've learned the basics, explore these topics:

- [Basic Usage](/en/guide/basic-usage) - Detailed syntax and features
- [TailwindCSS Integration](/en/guide/tailwindcss) - Style your components
- [API Reference](/en/api/) - Complete API documentation

## Tips for Success

1. **Think in Components**: Break your UI into reusable functions
2. **Use Python Features**: Leverage list comprehensions, conditionals, and loops
3. **Keep it Simple**: Start with basic elements and gradually add complexity
4. **Test Frequently**: Use `to_print()` to see your HTML output during development
