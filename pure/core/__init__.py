"""
Core classes for Purepy templating engine.

This module contains the fundamental classes that power Purepy:
- Tag: Base class for all HTML/XML/SVG elements
- HTML: HTML-specific tag implementation
- SVG: SVG-specific tag implementation
- XML: XML-specific tag implementation
- Raw: For raw HTML/XML content
- Dom: DOM manipulation utilities
- PDom: Python DOM implementation
"""

from .Tag import Tag
from .HTML import HTML
from .SVG import SVG
from .XML import XML
from .Raw import Raw
from .Dom import Dom
from .PDom import PDom

__all__ = [
    "Tag",
    "HTML",
    "SVG",
    "XML",
    "Raw",
    "Dom",
    "PDom",
]
