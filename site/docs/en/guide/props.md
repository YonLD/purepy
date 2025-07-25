# Props

Props (Properties) are the inputs to components, used to configure component behavior and appearance. This guide will detail how to use props in Purepy.

## What are Props?

Props are data passed to components, typically as a dictionary. Components receive external data through props and render corresponding content based on this data.

## Basic Props Usage

### Passing Props

```python
from pure.html import div, h1, p

def Greeting(props):
    name = props.get('name', 'Guest')
    message = props.get('message', 'Welcome!')
    
    return div(
        h1(f'Hello, {name}!'),
        p(message)
    ).class_name('greeting')

# Use component and pass props
greeting = Greeting({
    'name': 'John',
    'message': 'Welcome to our website!'
})
```

### Props Types

Props can be any Python data type:

```python
def UserCard(props):
    # String props
    name = props.get('name', '')
    
    # Number props
    age = props.get('age', 0)
    
    # Boolean props
    is_premium = props.get('isPremium', False)
    
    # List props
    hobbies = props.get('hobbies', [])
    
    # Dictionary props
    address = props.get('address', {})
    
    return div(
        h2(name),
        p(f'Age: {age}'),
        p('Premium User' if is_premium else 'Regular User'),
        div(
            h3('Hobbies:'),
            ul(*[li(hobby) for hobby in hobbies])
        ) if hobbies else None,
        div(
            h3('Address:'),
            p(f"{address.get('city', '')} {address.get('street', '')}")
        ) if address else None
    ).class_name('user-card')
```

## Default Props

Provide default values for props to make components more robust:

```python
from pure.html import button, div, h2, p

def Button(props):
    # Use get() method to provide default values
    text = props.get('text', 'Button')
    variant = props.get('variant', 'primary')
    size = props.get('size', 'medium')
    disabled = props.get('disabled', False)
    
    return button(text) \
        .class_name(f'btn btn-{variant} btn-{size}') \
        .disabled(disabled)

# You can also use dictionary merging
def Card(props):
    defaults = {
        'title': 'Default Title',
        'content': 'Default Content',
        'variant': 'default',
        'shadow': True
    }
    
    # Merge defaults with passed props
    merged_props = {**defaults, **props}
    
    return div(
        h2(merged_props['title']),
        p(merged_props['content'])
    ).class_name(f"card card-{merged_props['variant']}" + 
                 (' card-shadow' if merged_props['shadow'] else ''))
```

## Props Validation

While Python is dynamically typed, we can add props validation to improve code quality:

```python
def validateProps(props, required=None, types=None):
    """Simple props validation function"""
    required = required or []
    types = types or {}
    
    # Check required props
    for prop in required:
        if prop not in props:
            raise ValueError(f"Missing required prop: {prop}")
    
    # Check prop types
    for prop, expected_type in types.items():
        if prop in props and not isinstance(props[prop], expected_type):
            raise TypeError(f"Prop {prop} should be of type {expected_type.__name__}")

def SafeButton(props):
    # Validate props
    validateProps(props, 
                  required=['text'],
                  types={'text': str, 'disabled': bool})
    
    return button(props['text']) \
        .class_name('btn') \
        .disabled(props.get('disabled', False))
```

## Props Passing Patterns

### 1. Props Pass-through

Pass props to child components:

```python
def Card(props):
    # Extract card-specific props
    title = props.get('title', '')
    content = props.get('content', '')
    
    # Pass button-related props to Button component
    button_props = {
        'text': props.get('buttonText', 'Learn More'),
        'variant': props.get('buttonVariant', 'primary'),
        'disabled': props.get('buttonDisabled', False)
    }
    
    return div(
        h2(title),
        p(content),
        Button(button_props)
    ).class_name('card')
```

### 2. Props Destructuring

Extract specific values from props:

```python
def UserProfile(props):
    user = props.get('user', {})
    
    # Destructure user object
    name = user.get('name', '')
    email = user.get('email', '')
    avatar = user.get('avatar', '')
    bio = user.get('bio', '')
    
    return div(
        div(
            img().src(avatar).alt(name) if avatar else None,
            h2(name),
            p(email)
        ).class_name('user-header'),
        div(
            p(bio)
        ).class_name('user-bio') if bio else None
    ).class_name('user-profile')
```

### 3. Props Grouping

Group related props for passing:

```python
def Form(props):
    # Form configuration
    form_config = props.get('config', {})
    
    # Field definitions
    fields = props.get('fields', [])
    
    # Submit configuration
    submit_config = props.get('submit', {})
    
    return form(
        *[FormField(field) for field in fields],
        button(submit_config.get('text', 'Submit')) \
            .type('submit') \
            .class_name(submit_config.get('className', 'btn btn-primary'))
    ) \
    .action(form_config.get('action', '')) \
    .method(form_config.get('method', 'post')) \
    .class_name(form_config.get('className', 'form'))
```

## Conditional Props

Set different props based on conditions:

```python
def Alert(props):
    alert_type = props.get('type', 'info')
    message = props.get('message', '')
    dismissible = props.get('dismissible', False)
    
    # Set different icons based on type
    icons = {
        'info': 'ℹ️',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    }
    
    icon = icons.get(alert_type, icons['info'])
    
    return div(
        span(icon).class_name('alert-icon'),
        span(message).class_name('alert-message'),
        button('×').class_name('alert-close') if dismissible else None
    ).class_name(f'alert alert-{alert_type}')
```

## Function Props

While not commonly used when generating static HTML, you can pass functions as props:

```python
def DataTable(props):
    data = props.get('data', [])
    columns = props.get('columns', [])
    row_renderer = props.get('rowRenderer', None)
    
    def default_row_renderer(row, index):
        return tr(
            *[td(str(row.get(col['key'], ''))) for col in columns]
        )
    
    renderer = row_renderer or default_row_renderer
    
    return table(
        thead(
            tr(*[th(col['title']) for col in columns])
        ),
        tbody(
            *[renderer(row, i) for i, row in enumerate(data)]
        )
    ).class_name('data-table')

# Use custom renderer
def custom_row_renderer(row, index):
    return tr(
        td(row.get('name', '')),
        td(row.get('email', '')),
        td(
            button('Edit').class_name('btn btn-sm'),
            button('Delete').class_name('btn btn-sm btn-danger')
        )
    ).class_name('table-row')

table = DataTable({
    'data': users,
    'columns': [
        {'key': 'name', 'title': 'Name'},
        {'key': 'email', 'title': 'Email'},
        {'key': 'actions', 'title': 'Actions'}
    ],
    'rowRenderer': custom_row_renderer
})
```

## Props Best Practices

### 1. Use Descriptive Prop Names

```python
# Bad naming
def Card(props):
    t = props.get('t')  # Unclear what 't' is
    c = props.get('c')  # Unclear what 'c' is
    
# Good naming
def Card(props):
    title = props.get('title')
    content = props.get('content')
```

### 2. Keep Props Structure Simple

```python
# Avoid over-nesting
# Bad practice
props = {
    'user': {
        'profile': {
            'personal': {
                'name': {
                    'first': 'John',
                    'last': 'Doe'
                }
            }
        }
    }
}

# Good practice
props = {
    'firstName': 'John',
    'lastName': 'Doe',
    'email': 'john@example.com'
}
```

### 3. Use Type Hints

```python
from typing import Dict, Any, List, Optional

def UserList(props: Dict[str, Any]) -> 'HTML':
    users: List[Dict[str, Any]] = props.get('users', [])
    title: str = props.get('title', 'User List')
    show_email: bool = props.get('showEmail', True)
    
    return div(
        h2(title),
        ul(
            *[UserItem({
                'user': user,
                'showEmail': show_email
            }) for user in users]
        )
    ).class_name('user-list')
```

### 4. Document Props

```python
def Button(props):
    """
    Button component
    
    Props:
        text (str): Button text, defaults to 'Button'
        variant (str): Button style, options: 'primary', 'secondary', 'danger'
        size (str): Button size, options: 'small', 'medium', 'large'
        disabled (bool): Whether disabled, defaults to False
        fullWidth (bool): Whether full width, defaults to False
        onClick (str): Click event handler
    """
    # Component implementation...
```

## Props Pattern Examples

### Configuration Object Pattern

```python
def Chart(props):
    config = props.get('config', {})
    data = props.get('data', [])
    
    # Extract settings from config
    chart_type = config.get('type', 'bar')
    width = config.get('width', 400)
    height = config.get('height', 300)
    colors = config.get('colors', ['#blue', '#red', '#green'])
    
    return div(
        # Chart implementation...
    ).class_name(f'chart chart-{chart_type}') \
     .style(f'width: {width}px; height: {height}px;')
```

### Render Props Pattern

```python
def List(props):
    items = props.get('items', [])
    render_item = props.get('renderItem', None)
    
    def default_render(item, index):
        return li(str(item))
    
    renderer = render_item or default_render
    
    return ul(
        *[renderer(item, i) for i, item in enumerate(items)]
    ).class_name('list')
```

## Next Steps

Now that you've mastered using props, you can continue learning:

- [TailwindCSS Integration](/en/guide/tailwindcss) - Learn how to style components
- [API Reference](/en/api/) - View complete API documentation
- [Basic Usage](/en/guide/basic-usage) - Review basic syntax
