# Flask Integration

Purepy integrates seamlessly with the Flask framework, providing component-based template rendering capabilities.

## Why Choose This Combination?

- **Purepy**: Provides component-based Python template rendering
- **Flask**: Provides lightweight web framework
- **Perfect Complement**: Purepy handles the view layer, Flask handles routing and business logic

## Quick Start

### 1. Install Dependencies

```bash
pip install flask purepy
```

### 2. Basic Integration

```python
from flask import Flask
from pure.html import html, head, title, body, div, h1, p, a

app = Flask(__name__)

def Layout(props):
    page_title = props.get('title', 'Purepy + Flask')
    content = props.get('content', '')
    
    return html(
        head(
            title(page_title)
        ),
        body(
            div(
                content
            ).class_name('container')
        )
    )

@app.route('/')
def index():
    content = div(
        h1('Welcome to Purepy + Flask'),
        p('This is an application built with Purepy and Flask'),
        a('Learn more').href('/about')
    )
    
    page = Layout({
        'title': 'Home',
        'content': content
    })
    
    return str(page)

@app.route('/about')
def about():
    content = div(
        h1('About Us'),
        p('Purepy is a Python template engine inspired by ReactJS.')
    )
    
    page = Layout({
        'title': 'About Us',
        'content': content
    })
    
    return str(page)

if __name__ == '__main__':
    app.run(debug=True)
```

### 3. Component-Based Development

```python
from flask import Flask, request, jsonify
from pure.html import html, head, title, body, div, h1, h2, p, form, input, button, ul, li, style

app = Flask(__name__)

# Layout component
def Layout(props):
    page_title = props.get('title', 'Purepy App')
    content = props.get('content', '')
    
    return html(
        head(
            title(page_title),
            # Add styles
            style("""
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                .container { max-width: 800px; margin: 0 auto; }
                .card { background: #f5f5f5; padding: 20px; margin: 10px 0; border-radius: 8px; }
                .form-group { margin: 10px 0; }
                .form-group input { width: 100%; padding: 8px; }
                .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            """)
        ),
        body(
            div(
                content
            ).class_name('container')
        )
    )

# Card component
def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')
    
    return div(
        h2(title),
        p(content)
    ).class_name('card')

# Form component
def ContactForm():
    return form(
        div(
            input().type('text').name('name').placeholder('Name').required()
        ).class_name('form-group'),
        div(
            input().type('email').name('email').placeholder('Email').required()
        ).class_name('form-group'),
        div(
            input().type('text').name('message').placeholder('Message').required()
        ).class_name('form-group'),
        button('Submit').type('submit').class_name('btn')
    ).method('POST').action('/contact')

# Routes
@app.route('/')
def index():
    content = div(
        h1('Welcome to Purepy + Flask'),
        Card({
            'title': 'Component-Based Development',
            'content': 'Use Purepy to create reusable components for easier maintenance.'
        }),
        Card({
            'title': 'Flask Integration',
            'content': 'Purepy integrates perfectly with Flask for powerful template rendering.'
        })
    )
    
    return str(Layout({
        'title': 'Home',
        'content': content
    }))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Here you can save to database or send email
        
        content = div(
            h1('Contact Us'),
            p(f'Thank you {name}, we have received your message!')
        )
    else:
        content = div(
            h1('Contact Us'),
            ContactForm()
        )
    
    return str(Layout({
        'title': 'Contact Us',
        'content': content
    }))

if __name__ == '__main__':
    app.run(debug=True)
```

## Advanced Usage

### 1. Template Inheritance

```python
# templates.py
from pure.html import html, head, title, meta, body, div, nav, ul, li, a, footer, p

def BaseTemplate(props):
    page_title = props.get('title', 'Purepy App')
    content = props.get('content', '')
    nav_items = props.get('nav_items', [])
    
    return html(
        head(
            meta().charset('UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1.0'),
            title(page_title)
        ),
        body(
            nav(
                ul(
                    *[li(a(item['text']).href(item['url'])) for item in nav_items]
                )
            ).class_name('navbar'),
            div(
                content
            ).class_name('main-content'),
            footer(
                p('© 2024 Purepy App')
            ).class_name('footer')
        )
    )

# app.py
from templates import BaseTemplate

@app.route('/')
def index():
    nav_items = [
        {'text': 'Home', 'url': '/'},
        {'text': 'About', 'url': '/about'},
        {'text': 'Contact', 'url': '/contact'}
    ]
    
    content = div(
        h1('Home Content')
    )
    
    return str(BaseTemplate({
        'title': 'Home',
        'content': content,
        'nav_items': nav_items
    }))
```

### 2. Data Binding

```python
from flask import Flask, render_template_string
from pure.html import div, h1, ul, li, p

app = Flask(__name__)

def UserList(users):
    return div(
        h1('User List'),
        ul(
            *[li(
                p(f'Name: {user["name"]}'),
                p(f'Email: {user["email"]}')
            ) for user in users]
        )
    )

@app.route('/users')
def users():
    # Simulate getting user data from database
    users_data = [
        {'name': 'John Doe', 'email': 'john@example.com'},
        {'name': 'Jane Smith', 'email': 'jane@example.com'},
        {'name': 'Bob Johnson', 'email': 'bob@example.com'}
    ]
    
    content = UserList(users_data)
    
    return str(Layout({
        'title': 'User List',
        'content': content
    }))
```

### 3. API Responses

```python
from flask import jsonify

@app.route('/api/component')
def api_component():
    # Return component HTML string for AJAX updates
    component = Card({
        'title': 'Dynamic Content',
        'content': 'This content was loaded via API'
    })
    
    return jsonify({
        'html': str(component),
        'status': 'success'
    })
```

## Best Practices

### 1. Component Organization

```python
# components/
#   __init__.py
#   layout.py
#   forms.py
#   cards.py

# components/layout.py
from pure.html import html, head, title, body, div

def Layout(props):
    # Layout component implementation
    pass

# components/forms.py
from pure.html import form, input, button

def ContactForm(props):
    # Form component implementation
    pass

# app.py
from components.layout import Layout
from components.forms import ContactForm
```

### 2. Error Handling

```python
@app.errorhandler(404)
def not_found(error):
    content = div(
        h1('Page Not Found'),
        p('Sorry, the page you are looking for does not exist.'),
        a('Return Home').href('/')
    )
    
    return str(Layout({
        'title': '404 - Page Not Found',
        'content': content
    })), 404
```

### 3. Performance Optimization

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_component(data_hash):
    # Cache static components
    return str(SomeComponent(data))
```

## Next Steps

- [Django Integration](/en/guide/django) - Learn how to work with Django
- [Components](/en/guide/components) - Deep dive into component development
- [API Documentation](/en/api/) - View complete API reference
