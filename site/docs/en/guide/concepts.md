# Core Concepts

This chapter introduces the core concepts of Purepy to help you better understand and use this template engine.

## Elements

In Purepy, every HTML tag is a function, and calling these functions creates element objects.

### Creating Elements

```python
from pure.html import div, h1, p

# Create a div element
container = div()

# Create elements with content
title = h1('Page Title')
content = p('This is paragraph content')
```

### Element Structure

Each element consists of the following parts:

- **Tag Name**: The name of the HTML tag (like 'div', 'h1', 'p')
- **Attributes**: Element attributes (like class, id, data-* etc.)
- **Children**: Other elements or text nested inside the element

```python
# Element structure example
element = div(                    # Tag name: div
    h1('Title'),                  # Child element: h1
    p('Content')                  # Child element: p
).class_name('container')         # Attribute: class="container"
```

## Attributes

Attributes are used to configure element behavior and appearance.

### Setting Attributes

```python
from pure.html import div, input

# Use method chaining to set attributes
element = div('Content') \
    .class_name('container') \
    .id('main') \
    .data_value('123')

# Form element attributes
field = input() \
    .type('text') \
    .name('username') \
    .placeholder('Enter username') \
    .required(True)
```

### Special Attribute Handling

#### class Attribute

Since `class` is a Python keyword, use the `class_name` method:

```python
div('Content').class_name('btn btn-primary')
```

#### data and aria Attributes

Use underscores instead of hyphens:

```python
div('Content') \
    .data_id('123') \          # data-id="123"
    .data_type('card') \       # data-type="card"
    .aria_label('Button')      # aria-label="Button"
```

#### Boolean Attributes

```python
input() \
    .type('checkbox') \
    .checked(True) \           # checked="checked"
    .disabled(False)           # won't add disabled attribute
```

## Children

Elements can contain other elements or text content.

### Adding Children

```python
from pure.html import div, h1, p, ul, li

# Single child element
container = div(h1('Title'))

# Multiple child elements
container = div(
    h1('Title'),
    p('Content'),
    ul(
        li('Item 1'),
        li('Item 2'),
        li('Item 3')
    )
)
```

### Dynamic Children

```python
# Using list comprehensions
items = ['Apple', 'Banana', 'Orange']
list_element = ul(
    *[li(item) for item in items]
)

# Conditional children
is_logged_in = True
header = div(
    h1('Website Title'),
    p('Welcome back!') if is_logged_in else p('Please log in')
)
```

## Components

Components are reusable functions that return element structures.

### Basic Components

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

### Component Composition

```python
def Header(props):
    return header(
        h1(props.get('title', '')),
        nav(
            *[a(item['text']).href(item['url']) 
              for item in props.get('nav_items', [])]
        )
    ).class_name('header')

def Footer(props):
    return footer(
        p(props.get('copyright', ''))
    ).class_name('footer')

def Layout(props):
    return div(
        Header(props.get('header', {})),
        main(props.get('content', '')),
        Footer(props.get('footer', {}))
    ).class_name('layout')
```

## Props

Props are data passed to components.

### Props Types

```python
def Button(props):
    # String props
    text = props.get('text', 'Button')
    
    # Boolean props
    is_primary = props.get('primary', False)
    is_disabled = props.get('disabled', False)
    
    # Function props (though not commonly used in HTML)
    on_click = props.get('onClick', '')
    
    # Object props
    style_props = props.get('style', {})
    
    return button(text) \
        .class_name('btn btn-primary' if is_primary else 'btn') \
        .disabled(is_disabled) \
        .onclick(on_click)
```

### Default Props

```python
def Card(props):
    # Set default values
    defaults = {
        'title': 'Default Title',
        'content': 'Default Content',
        'variant': 'default'
    }
    
    # Merge props with defaults
    merged_props = {**defaults, **props}
    
    return div(
        h2(merged_props['title']),
        p(merged_props['content'])
    ).class_name(f'card card-{merged_props["variant"]}')
```

## Conditional Rendering

Render different content based on conditions.

### Simple Conditions

```python
def UserGreeting(props):
    user = props.get('user')
    
    return div(
        h1('Welcome back!') if user else h1('Please log in'),
        p(f'Hello, {user.name}!') if user else None
    )
```

### Complex Conditions

```python
def StatusMessage(props):
    status = props.get('status', 'loading')
    
    if status == 'loading':
        return div('Loading...').class_name('loading')
    elif status == 'error':
        return div('An error occurred').class_name('error')
    elif status == 'success':
        return div('Operation successful').class_name('success')
    else:
        return div('Unknown status').class_name('unknown')
```

## List Rendering

Render dynamic list content.

### Basic Lists

```python
def TodoList(props):
    todos = props.get('todos', [])
    
    return ul(
        *[li(todo['text']) for todo in todos]
    ).class_name('todo-list')
```

### Lists with Keys

```python
def UserList(props):
    users = props.get('users', [])
    
    return div(
        *[
            div(
                h3(user['name']),
                p(user['email'])
            ).class_name('user-card')
            for user in users
        ]
    ).class_name('user-list')
```

## Style Handling

Purepy provides multiple ways to handle styles.

### Inline Styles

```python
from pure.sty import sty

styles = sty({
    'color': 'red',
    'font-size': '16px',
    'background-color': '#f0f0f0'
})

div('Content').style(styles)
```

### CSS Classes

```python
from pure.clx import clx

# Static classes
div('Content').class_name('btn btn-primary')

# Dynamic classes
is_active = True
classes = clx('btn', {'active': is_active, 'disabled': False})
div('Content').class_name(classes)
```

## Event Handling

While Purepy is primarily used for generating static HTML, you can still add event attributes:

```python
def InteractiveButton(props):
    return button(props.get('text', 'Click')) \
        .onclick(props.get('onClick', '')) \
        .class_name('interactive-btn')

# Usage
btn = InteractiveButton({
    'text': 'Click me',
    'onClick': 'alert("Button clicked!")'
})
```

## Lifecycle

In Purepy, component "lifecycle" is mainly reflected in data processing and rendering:

### Data Preparation

```python
def DataCard(props):
    # 1. Data preparation phase
    raw_data = props.get('data', {})
    
    # 2. Data processing
    processed_data = {
        'title': raw_data.get('title', '').upper(),
        'content': raw_data.get('content', '')[:100],  # First 100 characters
        'date': format_date(raw_data.get('date'))
    }
    
    # 3. Rendering phase
    return div(
        h2(processed_data['title']),
        p(processed_data['content']),
        small(processed_data['date'])
    ).class_name('data-card')
```

## Error Handling

Handle potential error conditions:

```python
def SafeCard(props):
    try:
        title = props['title']  # Required prop
        content = props.get('content', '')
        
        return div(
            h2(title),
            p(content) if content else p('No content available')
        ).class_name('card')
    
    except KeyError:
        return div(
            p('Error: Missing required title prop')
        ).class_name('error-card')
```

## Performance Considerations

### Avoid Repeated Calculations

```python
def ExpensiveComponent(props):
    # Cache calculation results
    if not hasattr(ExpensiveComponent, '_cache'):
        ExpensiveComponent._cache = {}
    
    cache_key = str(props)
    if cache_key in ExpensiveComponent._cache:
        return ExpensiveComponent._cache[cache_key]
    
    # Perform expensive calculation
    result = div(
        # ... complex rendering logic
    )
    
    ExpensiveComponent._cache[cache_key] = result
    return result
```

## Next Steps

Now that you understand the core concepts of Purepy, you can continue learning:

- [Basic Usage](/en/guide/basic-usage) - Detailed syntax explanation
- [Components](/en/guide/components) - Deep dive into component development
- [Props](/en/guide/props) - Master the props system
