# Publishing Purepy to PyPI

This guide explains how to publish the Purepy package to PyPI.

## Prerequisites

1. **Python 3.8+** installed
2. **PyPI account** - Register at https://pypi.org/account/register/
3. **Test PyPI account** (optional but recommended) - Register at https://test.pypi.org/account/register/
4. **API tokens** for PyPI and Test PyPI (recommended over username/password)

## Setup

### 1. Install build tools

```bash
pip install build twine
```

### 2. Configure PyPI credentials

Create `~/.pypirc` file:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

## Publishing Process

### 1. Prepare for release

1. Update version in `pyproject.toml` and `pure/__init__.py`
2. Update `CHANGELOG.md` (if exists)
3. Commit all changes
4. Create a git tag: `git tag v1.0.0`

### 2. Build the package

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build the package
python -m build
```

This creates:
- `dist/purepy-1.0.0.tar.gz` (source distribution)
- `dist/purepy-1.0.0-py3-none-any.whl` (wheel distribution)

### 3. Check the package

```bash
python -m twine check dist/*
```

### 4. Test upload (recommended)

Upload to Test PyPI first:

```bash
python -m twine upload --repository testpypi dist/*
```

Test installation:

```bash
pip install --index-url https://test.pypi.org/simple/ yonld-purepy
```

### 5. Upload to PyPI

```bash
python -m twine upload dist/*
```

## Using the provided scripts

### Automated build

```bash
python scripts/build.py
```

### Automated release

```bash
# Release to Test PyPI
python scripts/release.py --test

# Release to PyPI
python scripts/release.py
```

## Verification

After publishing, verify the package:

1. Check the package page: https://pypi.org/project/yonld-purepy/
2. Install and test: `pip install yonld-purepy`
3. Test basic functionality:

```python
from pure.html import div, h1
print(div(h1('Hello, Purepy!')))
```

## Troubleshooting

### Common issues:

1. **Version already exists**: Increment version number
2. **Authentication failed**: Check API tokens in `~/.pypirc`
3. **Package name taken**: Choose a different name in `pyproject.toml`
4. **Build fails**: Check dependencies and Python version compatibility

### Package name considerations:

- The name "purepy" might be taken
- Consider alternatives like "purepy-template", "pure-py", etc.
- Check availability: https://pypi.org/project/your-package-name/

## Best Practices

1. **Always test on Test PyPI first**
2. **Use semantic versioning** (MAJOR.MINOR.PATCH)
3. **Keep detailed changelogs**
4. **Test installation in clean environment**
5. **Use API tokens instead of passwords**
6. **Tag releases in git**
7. **Write comprehensive documentation**

## Security

- Never commit API tokens to version control
- Use environment variables for CI/CD
- Regularly rotate API tokens
- Use 2FA on PyPI accounts
