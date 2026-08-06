# Installation

This guide covers different ways to install and set up Purepy.

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Installation Methods

### 1. Install from PyPI (Recommended)

The easiest way to install Purepy is using pip:

```bash
pip install yonld-purepy
```

### 2. Install from Source

If you want the latest development version:

```bash
git clone https://github.com/YonLD/purepy.git
cd purepy
pip install -e .
```

### 3. Install in Virtual Environment (Recommended)

It's recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv purepy-env

# Activate virtual environment
# On Windows:
purepy-env\Scripts\activate
# On macOS/Linux:
source purepy-env/bin/activate

# Install Purepy
pip install yonld-purepy
```

## Verify Installation

After installation, verify that Purepy is working correctly:

```python
# test_purepy.py
from pure.html import div, h1, p

def test_installation():
    element = div(
        h1('Purepy Installation Test'),
        p('If you can see this, Purepy is working correctly!')
    ).class_name('test-container')

    print("HTML Output:")
    element.to_print()

    # Save to file
    element.to_save('test.html')
    print("\nHTML file saved as 'test.html'")

if __name__ == "__main__":
    test_installation()
```

Run the test:

```bash
python test_purepy.py
```

Expected output:
```html
<div class="test-container">
    <h1>Purepy Installation Test</h1>
    <p>If you can see this, Purepy is working correctly!</p>
</div>
```

## Development Setup

If you plan to contribute to Purepy or need the development version:

### 1. Clone the Repository

```bash
git clone https://github.com/YonLD/purepy.git
cd purepy
```

### 2. Create Development Environment

```bash
python -m venv dev-env
source dev-env/bin/activate  # On Windows: dev-env\Scripts\activate
```

### 3. Install in Development Mode

```bash
pip install -e .
```

### 4. Install Development Dependencies

```bash
pip install -r requirements-dev.txt  # If available
```

### 5. Run Tests

```bash
python -m pytest tests/  # If tests are available
```

## IDE Setup

### Visual Studio Code

For the best development experience with VS Code:

1. Install the Python extension
2. Set up your virtual environment
3. Configure Python interpreter

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./purepy-env/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

### PyCharm

1. Open your project in PyCharm
2. Go to File → Settings → Project → Python Interpreter
3. Add your virtual environment interpreter
4. Enable code completion and type hints

## Project Structure

When starting a new Purepy project, consider this structure:

```
my-purepy-project/
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── header.py
│   │   ├── footer.py
│   │   └── card.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home.py
│   │   └── about.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── output/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── requirements.txt
└── main.py
```

Example `requirements.txt`:

```txt
yonld-purepy>=1.0.0
```

Example `main.py`:

```python
from src.pages.home import create_home_page
from src.pages.about import create_about_page

def build_site():
    # Generate pages
    home = create_home_page()
    about = create_about_page()

    # Save pages
    home.to_save('output/index.html')
    about.to_save('output/about.html')

    print("Site built successfully!")

if __name__ == "__main__":
    build_site()
```

## Common Issues

### Import Errors

If you get import errors:

```python
# Wrong
from purepy.html import div  # This won't work

# Correct
from pure.html import div
```

### Module Not Found

If you get "Module not found" errors:

1. Ensure Purepy is installed: `pip list | grep yonld-purepy`
2. Check your Python path: `python -c "import sys; print(sys.path)"`
3. Verify virtual environment is activated

### Permission Errors

On some systems, you might need to use `pip install --user yonld-purepy` or run with elevated privileges.

## Updating Purepy

To update to the latest version:

```bash
pip install --upgrade yonld-purepy
```

To check your current version:

```python
import pure
print(pure.__version__)  # If version info is available
```

## Uninstalling

To remove Purepy:

```bash
pip uninstall yonld-purepy
```

## Next Steps

Now that Purepy is installed:

1. [Getting Started](/en/guide/getting-started) - Create your first Purepy application
2. [Basic Usage](/en/guide/basic-usage) - Learn the core concepts
3. [API Reference](/en/api/) - Explore all available features

## Getting Help

If you encounter issues:

1. Check the [documentation](/en/guide/)
2. Search existing [GitHub issues](https://github.com/YonLD/purepy/issues)
3. Create a new issue if needed

## System Requirements

### Minimum Requirements

- Python 3.8+
- 50MB disk space
- Any operating system (Windows, macOS, Linux)

### Recommended Requirements

- Python 3.9+
- Virtual environment
- Code editor with Python support
- Git (for development)
