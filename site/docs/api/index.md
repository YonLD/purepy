# API Reference

Purepy provides complete HTML, SVG, and XML tag support, along with useful utility functions.

## Core Modules

### HTML Tags

```python
from pure.html import div, h1, p, a, img, button, input, form
```

All HTML5 tags are available through the `pure.html` module.

### SVG Tags

```python
from pure.svg import svg, circle, rect, path, g
```

Complete SVG tag support for creating vector graphics.

### XML Tags

```python
from pure.core.XML import XML
```

Dynamic XML tag creation supporting arbitrary tag names.

### Utility Functions {#core-modules-utility-functions}

```python
from pure.clx import clx
from pure.sty import sty
from pure.raw import Raw

# Using utility functions
classes = clx('btn', {'active': is_active, 'primary': is_primary})
styles = sty({'color': 'red', 'font-size': '16px'})
raw_content = Raw('<strong>Bold text</strong>')

# Using in elements
div('Content') \
    .class_name(classes) \
    .style(styles) \
    .print()
```

## Basic Usage

### Creating Elements

```python
from pure.html import div, h1, p

# Create basic elements
element = div(
    h1('Title'),
    p('Paragraph content')
)
```

### Setting Attributes

```python
from pure.html import div
from pure.sty import sty

element = div('Content') \
    .class_name('container') \
    .id('main') \
    .style(sty({'color': 'red'})) \
    .data_id('123')
```

### HTML Output

```python
# Convert to string
html_string = str(element)

# Direct print
element.print()

# Save to file (HTML elements)
from pure.html import html, head, title, body

page = html(
    head(title('Page Title')),
    body(element)
)
page.save('output.html')
```

## Common Tags

### Document Structure

- `html()` - HTML document root element
- `head()` - Document head
- `body()` - Document body
- `meta()` - Metadata
- `title()` - Document title
- `link()` - External resource link
- `style()` - Inline styles

### Text Content

- `h1()`, `h2()`, `h3()`, `h4()`, `h5()`, `h6()` - Headings
- `p()` - Paragraph
- `span()` - Inline text
- `strong()` - Strong emphasis
- `em()` - Emphasis
- `code()` - Code snippet
- `pre()` - Preformatted text

### Layout

- `div()` - Generic container
- `section()` - Document section
- `article()` - Article content
- `header()` - Header section
- `footer()` - Footer section
- `nav()` - Navigation
- `aside()` - Sidebar content
- `main()` - Main content

### Lists

- `ul()` - Unordered list
- `ol()` - Ordered list
- `li()` - List item
- `dl()` - Description list
- `dt()` - Description term
- `dd()` - Description details

### Forms

- `form()` - Form container
- `input()` - Input field
- `textarea()` - Text area
- `button()` - Button
- `select()` - Select dropdown
- `option()` - Select option
- `label()` - Form label
- `fieldset()` - Field grouping
- `legend()` - Fieldset caption

### Media

- `img()` - Image
- `video()` - Video content
- `audio()` - Audio content
- `source()` - Media source
- `canvas()` - Drawing canvas
- `svg()` - SVG graphics

### Tables

- `table()` - Table container
- `thead()` - Table header
- `tbody()` - Table body
- `tfoot()` - Table footer
- `tr()` - Table row
- `th()` - Table header cell
- `td()` - Table data cell

## Core Classes

### Tag Class

The base class for all HTML elements:

```python
from pure.core.Tag import Tag

# All HTML elements inherit from Tag
# Common methods:
element.class_name('css-class')  # Set CSS class
element.id('element-id')         # Set ID
element.style(styles)            # Set inline styles
element.data_key('value')        # Set data attributes
element.print()               # Print HTML
element.to_JSON()                # Convert to JSON
str(element)                     # Convert to HTML string
```

### HTML Class

Extends Tag with HTML-specific functionality:

```python
from pure.core.HTML import HTML

# HTML elements support:
html_element.save('file.html')  # Save with DOCTYPE
```

### SVG Class

For SVG elements:

```python
from pure.core.SVG import SVG

# SVG-specific functionality
svg_element.save('image.svg')  # Save as SVG file
```

## Utility Functions

### clx Function

Conditional class name utility:

```python
from pure.clx import clx

# Basic usage
classes = clx('btn', 'btn-primary')  # "btn btn-primary"

# Conditional classes
is_active = True
classes = clx('btn', {'active': is_active})  # "btn active"

# Mixed usage
classes = clx('btn', 'btn-primary', {'active': is_active, 'disabled': False})
```

### sty Function

Style object utility:

```python
from pure.sty import sty

# Convert dict to CSS string
styles = sty({
    'color': 'red',
    'font-size': '16px',
    'background-color': '#f0f0f0'
})
# Returns: "color: red; font-size: 16px; background-color: #f0f0f0;"
```

### Raw Class

For inserting raw HTML:

```python
from pure.raw import Raw

# Insert raw HTML content
raw_html = Raw('<strong>Bold text</strong>')
div('Content: ', raw_html).print()
```

## Method Chaining

All elements support method chaining for fluent API:

```python
from pure.html import div, h1, p
from pure.clx import clx
from pure.sty import sty

div(
    h1('Welcome').class_name('title'),
    p('Description').class_name('subtitle')
) \
.class_name(clx('container', {'active': True})) \
.style(sty({'padding': '20px'})) \
.id('main-content') \
.data_component('hero') \
.print()
```

## Self-Closing Tags

Some HTML tags are automatically self-closing:

- `area`, `base`, `br`, `col`, `embed`
- `hr`, `img`, `input`, `link`, `meta`
- `source`, `track`, `wbr`

```python
from pure.html import img, br, input

# These automatically self-close
img().src('image.jpg').alt('Description')  # <img src="image.jpg" alt="Description" />
br()  # <br />
input().type('text').name('username')  # <input type="text" name="username" />
```

## Next Steps

- [Basic Usage](/guide/basic-usage) - Learn the fundamentals
- [TailwindCSS Integration](/guide/tailwindcss) - Style your components
