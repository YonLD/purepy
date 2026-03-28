"""
Test package imports and basic functionality.

This test ensures that the package can be imported correctly
and basic functionality works as expected.
"""

import unittest
import sys
from pathlib import Path

# Add the parent directory to the path so we can import pure
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestPackageImports(unittest.TestCase):
    """Test that all package components can be imported correctly."""
    
    def test_import_main_package(self):
        """Test importing the main package."""
        import pure
        
        # Check version is available
        self.assertTrue(hasattr(pure, '__version__'))
        self.assertIsInstance(pure.__version__, str)
        
        # Check author info
        self.assertTrue(hasattr(pure, '__author__'))
        self.assertTrue(hasattr(pure, '__email__'))
        self.assertTrue(hasattr(pure, '__license__'))
    
    def test_import_html_module(self):
        """Test importing HTML functions."""
        from pure.html import div, h1, p, a
        
        # Test basic HTML creation
        element = div(
            h1('Test Title'),
            p('Test paragraph'),
            a('Test link').href('https://example.com')
        )
        
        # Should be able to convert to string
        html_str = str(element)
        self.assertIsInstance(html_str, str)
        self.assertIn('Test Title', html_str)
        self.assertIn('Test paragraph', html_str)
        self.assertIn('https://example.com', html_str)
    
    def test_import_svg_module(self):
        """Test importing SVG functions."""
        from pure.svg import svg, circle, rect
        
        # Test basic SVG creation
        element = svg(
            circle().cx(50).cy(50).r(40),
            rect().x(10).y(10).width(80).height(80)
        )
        
        # Should be able to convert to string
        svg_str = str(element)
        self.assertIsInstance(svg_str, str)
        self.assertIn('circle', svg_str)
        self.assertIn('rect', svg_str)
    
    def test_import_core_classes(self):
        """Test importing core classes."""
        from pure.core import HTML, SVG, XML, Tag, Raw

        # Test HTML class
        html_element = HTML('div')
        self.assertIsInstance(html_element, Tag)

        # Test SVG class
        svg_element = SVG('svg', ())
        self.assertIsInstance(svg_element, Tag)

        # Test XML class
        xml_element = XML('root', ())
        self.assertIsInstance(xml_element, Tag)
    
    def test_import_utility_functions(self):
        """Test importing utility functions."""
        from pure.clx import clx
        from pure.sty import sty
        from pure.raw import raw_html
        
        # Test clx function
        classes = clx('class1', 'class2', None, 'class3')
        self.assertIsInstance(classes, str)
        self.assertIn('class1', classes)
        self.assertIn('class2', classes)
        self.assertIn('class3', classes)
        
        # Test sty function
        styles = sty({'color': 'red', 'font-size': '16px'})
        self.assertIsInstance(styles, str)
        self.assertIn('color: red', styles)
        self.assertIn('font-size: 16px', styles)
        
        # Test raw_html function
        raw = raw_html('<strong>Bold text</strong>')
        self.assertIsNotNone(raw)

class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality of the package."""
    
    def test_html_element_creation(self):
        """Test creating HTML elements."""
        from pure.html import div, h1, p
        
        element = div(
            h1('Hello World'),
            p('This is a test paragraph.')
        ).class_name('container').id('main')
        
        html_str = str(element)
        
        # Check structure
        self.assertIn('<div', html_str)
        self.assertIn('class="container"', html_str)
        self.assertIn('id="main"', html_str)
        self.assertIn('<h1>Hello World</h1>', html_str)
        self.assertIn('<p>This is a test paragraph.</p>', html_str)
        self.assertIn('</div>', html_str)
    
    def test_method_chaining(self):
        """Test method chaining for attributes."""
        from pure.html import div
        
        element = div('Content').class_name('test').id('test-id').style('color: red;')
        html_str = str(element)
        
        self.assertIn('class="test"', html_str)
        self.assertIn('id="test-id"', html_str)
        self.assertIn('style="color: red;"', html_str)
    
    def test_nested_elements(self):
        """Test nested element creation."""
        from pure.html import div, ul, li, a
        
        nav = div(
            ul(
                li(a('Home').href('/')),
                li(a('About').href('/about')),
                li(a('Contact').href('/contact'))
            )
        ).class_name('navigation')
        
        html_str = str(nav)
        
        self.assertIn('<div class="navigation">', html_str)
        self.assertIn('<ul>', html_str)
        self.assertIn('<li>', html_str)
        self.assertIn('href="/"', html_str)
        self.assertIn('href="/about"', html_str)
        self.assertIn('href="/contact"', html_str)

if __name__ == '__main__':
    unittest.main()
