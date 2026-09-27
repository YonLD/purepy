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
    ).class_name('container').print()
"""

# The installed distribution metadata is the single source of truth, so
# bumping `version` in pyproject.toml is enough. The literal is the fallback
# for running straight from a checkout, where no distribution is installed.
from importlib.metadata import PackageNotFoundError, version as _dist_version

try:
    __version__ = _dist_version("yonld-purepy")
except PackageNotFoundError:
    __version__ = "1.0.2"

__author__ = "YonLD"
__email__ = "istintin@outlook.com"
__license__ = "MIT"

from . import html, svg, clx, sty, raw
from .core import (
    HTML,
    SVG,
    XML,
    Tag,
    Raw,
    Slot,
    SlotKind,
    Escaper,
    Markup,
    ShapeContract,
    DevMode,
)
from .compile import Compile, Shape, Template, Renderer
from .component import Call, Registry, register, component
from .utils import renderHTML, renderXML
from .loader import load_module

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
    "Slot",
    "SlotKind",
    "Escaper",
    "Markup",
    "ShapeContract",
    "DevMode",
    "Compile",
    "Shape",
    "Template",
    "Renderer",
    "Call",
    "Registry",
    "register",
    "component",
    "renderHTML",
    "renderXML",
    "load_module",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
