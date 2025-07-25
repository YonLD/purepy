"""
Purepy - A Python templating engine inspired by ReactJS functional components.

Purepy allows you to create HTML/XML/SVG content using pure Python code,
with a syntax that closely resembles HTML while providing the full power
of Python for logic and data processing.

Example:
    from pure.html import div, h1, p, a

    div(
        h1('Welcome to Purepy'),
        p('A Python templating engine'),
        a('Learn more').href('https://github.com/YonLD/purepy')
    ).class_name('container').to_print()
"""

__version__ = "1.0.0"
__author__ = "YonLD"
__email__ = "istintin@outlook.com"
__license__ = "MIT"

# Import main modules for convenience
from . import html, svg, clx, sty, raw
from .core import HTML, SVG, XML, Tag, Raw

__all__ = [
    "html",
    "svg",
    "clx",
    "sty",
    "raw",
    "HTML",
    "SVG",
    "XML",
    "Tag",
    "Raw",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
