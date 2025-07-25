# Components

Components are one of the core concepts in Purepy, allowing you to split the UI into independent, reusable pieces. This guide will introduce how to create and use components.

## What are Components?

In Purepy, components are functions that return element structures. Components receive parameters (called "props") and return elements that describe the interface.

## Basic Components

### Creating Components

A component is a function that receives props and returns an element:

```python
from pure.html import div, h2, p

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')

    return div(
        h2(title).class_name('card-title'),
        p(content).class_name('card-content')
    ).class_name('card')
```

### Using Components

```python
# Use the component
my_card = Card({
    'title': 'Welcome to Purepy',
    'content': 'This is a Python-based template engine'
})

# Render the component
my_card.to_print()
```

Output:

```html
<div class="card">
    <h2 class="card-title">Welcome to Purepy</h2>
    <p class="card-content">This is a Python-based template engine</p>
</div>
```

## Component Design Patterns

### 1. Single Responsibility

Each component should do only one thing:

```python
# Bad: One component doing too many things
def Page(props):
    return div(
        # Header
        div(
            h1('Website Title'),
            nav(
                a('Home').href('/'),
                a('About').href('/about'),
                a('Contact').href('/contact')
            )
        ).class_name('header'),

        # Content
        div(
            h2(props.get('title')),
            p(props.get('content'))
        ).class_name('content'),

        # Footer
        div(
            p('Copyright © 2024')
        ).class_name('footer')
    )

# Good: Split into multiple components
def Header():
    return div(
        h1('Website Title'),
        nav(
            a('Home').href('/'),
            a('About').href('/about'),
            a('Contact').href('/contact')
        )
    ).class_name('header')

def Content(props):
    return div(
        h2(props.get('title')),
        p(props.get('content'))
    ).class_name('content')

def Footer():
    return div(
        p('Copyright © 2024')
    ).class_name('footer')

def Page(props):
    return div(
        Header(),
        Content(props),
        Footer()
    )
```

### 2. Composition over Inheritance

Use composition to build complex components:

```python
def Button(props):
    variant = props.get('variant', 'primary')
    size = props.get('size', 'medium')
    text = props.get('text', '')

    return button(text).class_name(f'btn btn-{variant} btn-{size}')

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')

    return div(
        h2(title),
        p(content),
        Button({
            'text': 'Learn More',
            'variant': 'secondary',
            'size': 'small'
        })
    ).class_name('card')
```

### 3. Container Components

Create components that can contain other content:

```python
def Container(props):
    children = props.get('children', [])

    return div(
        *children
    ).class_name('container')

# Usage
Container({
    'children': [
        h1('Title'),
        p('Content'),
        button('Click')
    ]
})
```

## Component Communication

### 1. Passing Data via Props

Pass data from parent to child components:

```python
def Parent():
    data = {
        'title': 'Title',
        'content': 'Content'
    }

    return div(
        Child(data)
    )

def Child(props):
    return div(
        h2(props.get('title')),
        p(props.get('content'))
    )
```

### 2. Component Composition

Achieve complex UI through component composition:

```python
def Layout(props):
    return div(
        Header(props.get('header', {})),
        main(props.get('children', [])),
        Footer()
    ).class_name('layout')

def App():
    return Layout({
        'header': {
            'title': 'My App',
            'nav_items': [
                {'text': 'Home', 'url': '/'},
                {'text': 'About', 'url': '/about'}
            ]
        },
        'children': [
            h1('Welcome'),
            p('This is the homepage content')
        ]
    })
```

## Conditional Rendering

Render different content based on conditions:

```python
def UserGreeting(props):
    user = props.get('user')
    is_admin = props.get('is_admin', False)

    if not user:
        return div(
            p('Please log in')
        ).class_name('guest-message')

    return div(
        h2(f'Welcome, {user["name"]}!'),
        p('Admin Control Panel') if is_admin else p('User Panel')
    ).class_name('user-message')
```

## List Rendering

Render list data:

```python
def TodoList(props):
    todos = props.get('todos', [])

    if not todos:
        return div(p('No todos yet')).class_name('empty-list')

    return div(
        h2('Todo List'),
        ul(
            *[TodoItem(todo) for todo in todos]
        )
    ).class_name('todo-list')

def TodoItem(props):
    return li(
        input().type('checkbox').checked(props.get('completed', False)),
        span(props.get('text', '')).class_name(
            'completed' if props.get('completed', False) else ''
        )
    ).class_name('todo-item')
```

## Component Library Example

Here's a simple component library example:

### Button Component

```python
from pure.html import button
from pure.clx import clx

def Button(props):
    # Extract props
    text = props.get('text', '')
    variant = props.get('variant', 'primary')
    size = props.get('size', 'medium')
    disabled = props.get('disabled', False)
    full_width = props.get('fullWidth', False)

    # Build class names
    classes = clx(
        'btn',
        f'btn-{variant}',
        f'btn-{size}',
        {'btn-disabled': disabled, 'btn-full': full_width}
    )

    # Return button element
    return button(text) \
        .class_name(classes) \
        .disabled(disabled) \
        .type(props.get('type', 'button')) \
        .onclick(props.get('onClick', ''))
```

### Card Component

```python
from pure.html import div, h2, p, img

def Card(props):
    # Extract props
    title = props.get('title', '')
    content = props.get('content', '')
    image_url = props.get('image', '')

    # Build card content
    card_content = []

    if image_url:
        card_content.append(
            img().src(image_url).alt(title).class_name('card-image')
        )

    card_content.extend([
        h2(title).class_name('card-title'),
        p(content).class_name('card-content')
    ])

    # Add action buttons
    actions = props.get('actions', [])
    if actions:
        action_buttons = div(
            *[Button(action) for action in actions]
        ).class_name('card-actions')
        card_content.append(action_buttons)

    # Return card element
    return div(
        *card_content
    ).class_name('card')
```

### Form Component

```python
from pure.html import form, div, label, input, textarea, button

def TextField(props):
    id = props.get('id', '')
    label_text = props.get('label', '')

    return div(
        label(label_text).for_(id) if label_text else None,
        input() \
            .type(props.get('type', 'text')) \
            .id(id) \
            .name(props.get('name', id)) \
            .placeholder(props.get('placeholder', '')) \
            .value(props.get('value', '')) \
            .required(props.get('required', False))
    ).class_name('form-field')

def Form(props):
    fields = props.get('fields', [])
    submit_text = props.get('submitText', 'Submit')

    return form(
        *[TextField(field) for field in fields],
        button(submit_text).type('submit').class_name('btn btn-primary')
    ) \
    .action(props.get('action', '')) \
    .method(props.get('method', 'post')) \
    .class_name('form')
```

## Best Practices

### 1. Keep Components Simple

Each component should do only one thing and do it well. If a component becomes complex, consider splitting it into smaller components.

### 2. Use Meaningful Names

Use descriptive names for components and props:

```python
# Bad naming
def C(p):
    return div(p.get('t'))

# Good naming
def Card(props):
    return div(props.get('title'))
```

### 3. Provide Default Values

Provide reasonable default values for props to make components easier to use:

```python
def Button(props):
    # Provide default values
    text = props.get('text', 'Button')
    variant = props.get('variant', 'primary')

    return button(text).class_name(f'btn btn-{variant}')
```

### 4. Document Components

Add docstrings to components explaining their purpose and parameters:

```python
def Alert(props):
    """
    Component for displaying alert messages

    Args:
        type (str): Alert type, options: 'info', 'success', 'warning', 'error'
        message (str): Message to display
        dismissible (bool): Whether the alert can be dismissed
    """
    alert_type = props.get('type', 'info')
    message = props.get('message', '')
    dismissible = props.get('dismissible', False)

    return div(
        message,
        button('×').class_name('close-btn') if dismissible else None
    ).class_name(f'alert alert-{alert_type}')
```

## Component Testing

Test components to ensure they work correctly:

```python
def test_button_component():
    # Test default button
    default_button = Button({})
    assert 'btn' in default_button.get_attr('class')
    assert 'btn-primary' in default_button.get_attr('class')

    # Test disabled button
    disabled_button = Button({'disabled': True})
    assert disabled_button.get_attr('disabled') == 'disabled'

    # Test custom button
    custom_button = Button({
        'text': 'Click me',
        'variant': 'danger',
        'size': 'large'
    })
    assert custom_button.get_children()[0] == 'Click me'
    assert 'btn-danger' in custom_button.get_attr('class')
    assert 'btn-large' in custom_button.get_attr('class')
```

## Next Steps

Now that you understand how to create and use components, you can continue learning:

- [Props](/en/guide/props) - Deep dive into the props system
- [TailwindCSS Integration](/en/guide/tailwindcss) - Learn how to style components
- [API Reference](/en/api/) - View complete API documentation
