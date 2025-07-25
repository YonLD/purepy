# Core Classes

Purepy's core classes provide the foundation for creating and manipulating HTML, SVG, and XML elements.

## Tag Class

`Tag` is the base class for all elements, providing basic element manipulation functionality.

### Basic Usage

```python
from pure.core.Tag import Tag

# Create basic tag
tag = Tag('div', ('Content'))
```

### Main Methods

#### Attribute Setting

```python
# Set CSS class
tag.class_name('container')

# Set ID
tag.id('main-content')

# Set data attributes
tag.data_id('123')
tag.data_type('card')

# Set ARIA attributes
tag.aria_label('Button')
tag.aria_hidden('true')

# Set styles
tag.style({'color': 'red', 'font-size': '16px'})
```

#### Content Operations

```python
# Get child elements
children = tag.get_children()

# Add children using function call
tag(child_element1, child_element2)

# Create element with children directly
tag = Tag('div', ('Child 1', 'Child 2'))
```

#### Output Methods

```python
# Convert to HTML string
html_string = str(tag)

# Print HTML
tag.to_print()

# Convert to JSON
json_data = tag.to_JSON()
```

## HTML Class

`HTML` class extends `Tag`, specifically for HTML elements, providing additional HTML-specific functionality.

### Basic Usage

```python
from pure.core.HTML import HTML

# Create HTML element
html_element = HTML('div', 'Content')
```

### HTML-specific Methods

#### Document Saving

```python
from pure.html import html, head, title, body, div

# Create complete HTML document
page = html(
    head(title('Page Title')),
    body(div('Page Content'))
)

# Save as HTML file (with DOCTYPE)
page.to_save('output.html')
```

#### Form Element Support

```python
from pure.html import form, input, button

# Form elements with special attributes
form_element = form(
    input().type('text').name('username').required(True),
    button('Submit').type('submit')
).action('/submit').method('post')
```

#### Media Element Support

```python
from pure.html import img, video, audio

# Image element
img_element = img().src('image.jpg').alt('Description').width('300').height('200')

# Video element
video_element = video().src('video.mp4').controls(True).autoplay(False)

# Audio element
audio_element = audio().src('audio.mp3').controls(True)
```

## SVG Class

`SVG` class is used for creating SVG graphic elements.

### Basic Usage

```python
from pure.core.SVG import SVG

# Create SVG element
svg_element = SVG('circle')
```

### SVG-specific Methods

#### Geometric Attributes

```python
from pure.svg import svg, circle, rect, line

# Circle
circle_element = circle().cx('50').cy('50').r('40').fill('red')

# Rectangle
rect_element = rect().x('10').y('10').width('100').height('50').fill('blue')

# Line
line_element = line().x1('0').y1('0').x2('100').y2('100').stroke('black')
```

#### SVG Container

```python
from pure.svg import svg, g

# SVG root element
svg_root = svg(
    circle().cx('50').cy('50').r('40').fill('red'),
    rect().x('10').y('10').width('100').height('50').fill('blue')
).width('200').height('200').viewBox('0 0 200 200')

# Group element
group = g(
    circle().cx('25').cy('25').r('20'),
    circle().cx('75').cy('25').r('20')
).transform('translate(10, 10)')
```

#### Save SVG

```python
# Save as SVG file
svg_root.to_save('image.svg')
```

## XML Class

`XML` class is used for creating arbitrary XML elements.

### Basic Usage

```python
from pure.core.XML import XML

# Create custom XML element
xml_element = XML('custom-tag', 'Content')
```

### XML-specific Features

#### Namespace Support

```python
# Element with namespace
xml_element = XML('ns:element', 'Content').xmlns_ns('http://example.com/namespace')
```

#### Custom Attributes

```python
# Use dynamic attribute methods (underscore converts to dash)
xml_element = XML('item') \
    .data_id('123') \
    .data_type('card')

# Or use set_attrs for batch setting
xml_element = XML('item').set_attrs({
    'custom-attr': 'value',
    'another_attr': 'another_value'
})
```

## Utility Functions

### clx Function

For handling conditional CSS class names:

```python
from pure.clx import clx

# Basic usage
classes = clx('btn', 'btn-primary')  # "btn btn-primary"

# Conditional classes
is_active = True
is_disabled = False
classes = clx('btn', {
    'active': is_active,      # includes 'active'
    'disabled': is_disabled   # excludes 'disabled'
})  # "btn active"

# Mixed usage
classes = clx(
    'btn',                    # always included
    'btn-primary',           # always included
    {
        'active': is_active,
        'disabled': is_disabled
    }
)
```

### sty Function

For handling style objects:

```python
from pure.sty import sty

# Convert dictionary to CSS string
styles = sty({
    'color': 'red',
    'font-size': '16px',
    'background-color': '#f0f0f0',
    'margin': '10px 20px'
})
# Returns: "color: red; font-size: 16px; background-color: #f0f0f0; margin: 10px 20px;"

# Use in elements
from pure.html import div
div('Content').style(styles)
```

### Raw Class

For inserting raw HTML content:

```python
from pure.raw import Raw

# Insert raw HTML
raw_content = Raw('<strong>Bold text</strong>')

# Use in elements
from pure.html import div
div('Prefix ', raw_content, ' Suffix').to_print()
# Output: <div>Prefix <strong>Bold text</strong> Suffix</div>
```

## Method Chaining

All core classes support method chaining for fluent API calls:

```python
from pure.html import div
from pure.clx import clx
from pure.sty import sty

# Method chaining example
element = div('Content') \
    .class_name(clx('card', {'active': True})) \
    .style(sty({'padding': '20px', 'margin': '10px'})) \
    .id('main-card') \
    .data_component('card') \
    .aria_label('Main card')

element.to_print()
```

## Self-closing Tags

Certain HTML tags automatically self-close:

```python
from pure.html import img, br, hr, input, meta, link

# These tags automatically self-close
img().src('image.jpg').alt('Image')     # <img src="image.jpg" alt="Image" />
br()                                    # <br />
hr()                                    # <hr />
input().type('text').name('username')  # <input type="text" name="username" />
meta().charset('UTF-8')                # <meta charset="UTF-8" />
link().rel('stylesheet').href('style.css') # <link rel="stylesheet" href="style.css" />
```

## Error Handling

Core classes provide basic error handling:

```python
try:
    # Create element
    element = div('Content').class_name('container')

    # Set attributes
    element.id('main').data_value('123')

    # Output
    element.to_print()

except Exception as e:
    print(f"Error creating element: {e}")
```

## Performance Considerations

### Element Reuse

```python
# Define reusable component function
def base_button(text='Button'):
    return button(text).class_name('btn')

# Create variations
primary_button = base_button('Primary Button').class_name('btn btn-primary')
secondary_button = base_button('Secondary Button').class_name('btn btn-secondary')
```

### Batch Operations

```python
# Batch attribute setting
element = div('Content')
attributes = {
    'class': 'container',
    'id': 'main',
    'data-component': 'layout'
}

for key, value in attributes.items():
    if key == 'class':
        element.class_name(value)
    elif key == 'id':
        element.id(value)
    else:
        element.set_attr(key, value)
```

## Next Steps

- [HTML Tags](/en/api/html-tags) - Learn about all available HTML tags
- [SVG Tags](/en/api/svg-tags) - Learn about SVG graphic elements
- [Basic Usage](/en/guide/basic-usage) - Learn basic syntax
