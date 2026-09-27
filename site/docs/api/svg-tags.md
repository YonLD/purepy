# SVG Tags

Purepy provides complete SVG (Scalable Vector Graphics) tag support. All SVG tags can be imported from the `pure.svg` module.

## SVG Root Element

### svg Element

```python
from pure.svg import svg

# Basic SVG container
svg_container = svg(
    # SVG content
).width('200').height('200').viewBox('0 0 200 200')

# SVG with namespace
svg_with_namespace = svg(
    # SVG content
).xmlns('http://www.w3.org/2000/svg').version('1.1')
```

## Basic Shapes

### Rectangle

```python
from pure.svg import rect

# Basic rectangle
basic_rect = rect().x('10').y('10').width('100').height('50').fill('blue')

# Rounded rectangle
rounded_rect = rect() \
    .x('10').y('10').width('100').height('50') \
    .rx('5').ry('5') \
    .fill('blue').stroke('black').stroke_width('2')
```

### Circle

```python
from pure.svg import circle

# Basic circle
basic_circle = circle().cx('50').cy('50').r('40').fill('red')

# Circle with stroke
circle_with_stroke = circle() \
    .cx('50').cy('50').r('40') \
    .fill('red').stroke('black').stroke_width('3')
```

### Ellipse

```python
from pure.svg import ellipse

# Ellipse
ellipse_shape = ellipse() \
    .cx('100').cy('50').rx('80').ry('30') \
    .fill('green').stroke('blue').stroke_width('2')
```

### Line

```python
from pure.svg import line

# Basic line
basic_line = line() \
    .x1('0').y1('0').x2('100').y2('100') \
    .stroke('black').stroke_width('2')

# Dashed line
dashed_line = line() \
    .x1('0').y1('50').x2('200').y2('50') \
    .stroke('red').stroke_width('3') \
    .stroke_dasharray('5,5')
```

### Polyline

```python
from pure.svg import polyline

# Polyline
polyline_shape = polyline() \
    .points('0,0 50,25 100,0 150,25 200,0') \
    .fill('none').stroke('blue').stroke_width('2')
```

### Polygon

```python
from pure.svg import polygon

# Triangle
triangle = polygon() \
    .points('50,0 0,100 100,100') \
    .fill('yellow').stroke('red').stroke_width('2')

# Star
star = polygon() \
    .points('50,0 61,35 98,35 68,57 79,91 50,70 21,91 32,57 2,35 39,35') \
    .fill('gold').stroke('orange').stroke_width('1')
```

## Paths

### path Element

```python
from pure.svg import path

# Basic path
basic_path = path() \
    .d('M 10 10 L 90 90 L 10 90 Z') \
    .fill('purple').stroke('black').stroke_width('2')

# Bezier curve
bezier_curve = path() \
    .d('M 10 80 Q 52.5 10, 95 80 T 180 80') \
    .fill('none').stroke('blue').stroke_width('3')

# Arc
arc_path = path() \
    .d('M 10 50 A 40 40 0 0 1 90 50') \
    .fill('none').stroke('green').stroke_width('4')
```

## Text

### text Element

```python
from pure.svg import text, tspan

# Basic text
basic_text = text('Hello SVG') \
    .x('50').y('50') \
    .font_family('Arial').font_size('16').fill('black')

# Multiline text
multiline_text = text(
    tspan('First line').x('50').dy('0'),
    tspan('Second line').x('50').dy('20'),
    tspan('Third line').x('50').dy('20')
).font_family('Arial').font_size('14').fill('blue')

# Text on path
from pure.svg import textPath

text_on_path = text(
    textPath('Text along path').href('#path1')
).font_family('Arial').font_size('12').fill('red')
```

## Grouping and Structure

### g Element (Grouping)

```python
from pure.svg import g

# Basic grouping
basic_group = g(
    circle().cx('25').cy('25').r('20').fill('red'),
    rect().x('5').y('5').width('40').height('40').fill('none').stroke('blue')
).transform('translate(50, 50)')

# Styled group
styled_group = g(
    circle().cx('0').cy('0').r('10'),
    circle().cx('20').cy('0').r('10'),
    circle().cx('10').cy('15').r('10')
).fill('green').stroke('black').stroke_width('1').transform('scale(2)')
```

### defs Element (Definitions)

```python
from pure.svg import defs, linearGradient, stop, pattern

# Define gradient
gradient_defs = defs(
    linearGradient(
        stop().offset('0%').stop_color('red'),
        stop().offset('100%').stop_color('blue')
    ).id('gradient1').x1('0%').y1('0%').x2('100%').y2('0%')
)

# Use gradient
rect_with_gradient = rect() \
    .x('10').y('10').width('100').height('50') \
    .fill('url(#gradient1)')
```

### use Element (Reuse)

```python
from pure.svg import use

# Define reusable element
reusable_shape = g(
    circle().cx('0').cy('0').r('10').fill('blue'),
    rect().x('-5').y('-5').width('10').height('10').fill('red')
).id('shape1')

# Reuse elements
use_shape1 = use().href('#shape1').x('50').y('50')
use_shape2 = use().href('#shape1').x('100').y('100').transform('scale(1.5)')
```

## Gradients and Patterns

### Linear Gradient

```python
from pure.svg import linearGradient, stop

# Horizontal gradient
horizontal_gradient = linearGradient(
    stop().offset('0%').stop_color('red').stop_opacity('1'),
    stop().offset('50%').stop_color('yellow').stop_opacity('0.8'),
    stop().offset('100%').stop_color('blue').stop_opacity('1')
).id('horizontal').x1('0%').y1('0%').x2('100%').y2('0%')

# Vertical gradient
vertical_gradient = linearGradient(
    stop().offset('0%').stop_color('white'),
    stop().offset('100%').stop_color('black')
).id('vertical').x1('0%').y1('0%').x2('0%').y2('100%')
```

### Radial Gradient

```python
from pure.svg import radialGradient

# Radial gradient
radial_gradient = radialGradient(
    stop().offset('0%').stop_color('white'),
    stop().offset('70%').stop_color('blue'),
    stop().offset('100%').stop_color('darkblue')
).id('radial').cx('50%').cy('50%').r('50%')
```

### Pattern

```python
from pure.svg import pattern

# Repeating pattern
repeat_pattern = pattern(
    rect().x('0').y('0').width('10').height('10').fill('red'),
    circle().cx('5').cy('5').r('3').fill('blue')
).id('pattern1').x('0').y('0').width('20').height('20').patternUnits('userSpaceOnUse')
```

## Filter Effects

### filter Element

```python
from pure.svg import filter, feGaussianBlur, feOffset, feFlood, feComposite

# Shadow filter
shadow_filter = filter(
    feOffset().in_('SourceGraphic').dx('3').dy('3').result('offset'),
    feGaussianBlur().in_('offset').stdDeviation('2').result('blur'),
    feFlood().flood_color('black').flood_opacity('0.3').result('color'),
    feComposite().in_('color').in2('blur').operator('in').result('shadow'),
    feComposite().in_('SourceGraphic').in2('shadow').operator('over')
).id('shadow')

# Blur filter
blur_filter = filter(
    feGaussianBlur().in_('SourceGraphic').stdDeviation('3')
).id('blur')
```

## Animation

### animate Element

```python
from pure.svg import animate, animateTransform

# Attribute animation
color_animation = animate() \
    .attributeName('fill') \
    .values('red;blue;red') \
    .dur('3s') \
    .repeatCount('indefinite')

# Transform animation
rotation_animation = animateTransform() \
    .attributeName('transform') \
    .type('rotate') \
    .values('0 50 50;360 50 50') \
    .dur('2s') \
    .repeatCount('indefinite')
```

### animateMotion Element

```python
from pure.svg import animateMotion, mpath

# Path animation
motion_animation = animateMotion(
    mpath().href('#motionPath')
).dur('5s').repeatCount('indefinite')
```

## Clipping and Masking

### clipPath Element

```python
from pure.svg import clipPath

# Clipping path
clip_path = clipPath(
    circle().cx('50').cy('50').r('40')
).id('clip1')

# Apply clipping
clipped_rect = rect() \
    .x('0').y('0').width('100').height('100') \
    .fill('blue').clip_path('url(#clip1)')
```

### mask Element

```python
from pure.svg import mask

# Mask
mask_element = mask(
    rect().x('0').y('0').width('100').height('100').fill('white'),
    circle().cx('50').cy('50').r('30').fill('black')
).id('mask1')

# Apply mask
masked_rect = rect() \
    .x('0').y('0').width('100').height('100') \
    .fill('red').mask('url(#mask1)')
```

## Markers

### marker Element

```python
from pure.svg import marker

# Arrow marker
arrow_marker = marker(
    path().d('M 0 0 L 10 5 L 0 10 Z').fill('black')
).id('arrow') \
  .markerWidth('10').markerHeight('10') \
  .refX('9').refY('5') \
  .orient('auto').markerUnits('strokeWidth')

# Line with marker
line_with_marker = line() \
    .x1('10').y1('10').x2('100').y2('100') \
    .stroke('black').stroke_width('2') \
    .marker_end('url(#arrow)')
```

## Complete Example

### Complex SVG Graphic

```python
from pure.svg import svg, defs, linearGradient, stop, rect, circle, text, g

# Create complete SVG graphic
complete_svg = svg(
    defs(
        linearGradient(
            stop().offset('0%').stop_color('#ff7e5f'),
            stop().offset('100%').stop_color('#feb47b')
        ).id('gradient')
    ),
    
    # Background
    rect().x('0').y('0').width('200').height('200').fill('url(#gradient)'),
    
    # Shape group
    g(
        circle().cx('100').cy('100').r('50').fill('white').stroke('#333').stroke_width('3'),
        text('SVG').x('100').y('110').text_anchor('middle').font_family('Arial').font_size('20').fill('#333')
    ).transform('translate(0, 0)')
    
).width('200').height('200').viewBox('0 0 200 200')

# Save SVG
complete_svg.save('example.svg')
```

### Responsive SVG

```python
# Responsive SVG icon
responsive_icon = svg(
    path().d('M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z') \
          .fill('currentColor')
).viewBox('0 0 24 24').class_name('icon')
```

## Styles and Attributes

### Common Style Attributes

```python
# Fill and stroke
element.fill('red')                    # Fill color
element.stroke('blue')                 # Stroke color
element.stroke_width('2')              # Stroke width
element.stroke_dasharray('5,5')        # Dash pattern
element.stroke_linecap('round')        # Line cap style
element.stroke_linejoin('round')       # Line join style

# Opacity
element.opacity('0.8')                 # Overall opacity
element.fill_opacity('0.5')            # Fill opacity
element.stroke_opacity('0.7')          # Stroke opacity

# Transform
element.transform('translate(10, 20)') # Translation
element.transform('rotate(45)')        # Rotation
element.transform('scale(1.5)')        # Scaling
element.transform('skewX(15)')         # Skewing
```

## Next Steps

- [Core Classes](/api/core) - Learn about SVG class functionality
- [HTML Tags](/api/html-tags) - Learn about HTML tags
- [Basic Usage](/guide/basic-usage) - Learn how to use SVG tags
