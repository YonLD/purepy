# Purepy

Purepy is a Python templating engine inspired by ReactJS functional components.

## Why use Purepy?

To enjoy pure Python programming.

In traditional approaches, mixing HTML code, Python code, and other template syntax in the view layer can be frustrating for developers.

However, with Purepy:
+ Everything is 100% native Python code.
+ Encapsulate components to eliminate repetitive HTML code.
+ The syntax closely resembles HTML.

## Install

```bash
pip install purepy
```

## Basic usage

Here is a simple example that will show how to use `Purepy`:

```python
from pure.html import div, a

div(
    'Hello ',
    a('Python').href('https://www.python.org')
).class_name('container').style('background: #fff;').data_key('primary').to_print()
```

The above code will output:

```html
<div class="container" style="background: #fff;" data-key="primary">Hello <a href="https://www.python.org">Python</a></div>
```

## Component

You can use Purepy to encapsulate repeated code snippets into a functional component, which looks a lot like a React functional component:

```python
from pure.html import div, h2, p, a

# Function component
def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')
    link = props.get('link', '#')

    return div(
        h2(title).class_name('card-title'),
        p(content).class_name('card-content'),
        a('Read more').href(link).class_name('card-link')
    ).class_name('card')

# Usage
Card({
    'title': 'Welcome to Purepy',
    'content': 'A Python templating engine inspired by React',
    'link': 'https://github.com/YonLD/purepy'
}).to_print()
```

## Features

- **Pure Python**: Everything is 100% native Python code
- **Component-based**: Create reusable components like React
- **HTML-like syntax**: Familiar syntax for web developers
- **Type hints support**: Full type hints for better IDE support
- **Zero dependencies**: No external dependencies required
- **SVG support**: Built-in SVG element support
- **Lightweight**: Small footprint and fast performance

## Examples

For more usage examples see [here](https://github.com/YonLD/purepy/tree/master/examples).

## Development

### Setup development environment

```bash
git clone https://github.com/YonLD/purepy.git
cd purepy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

### Code formatting

```bash
black pure tests
```

## License

MIT © YonLD
