# SVG Class

`pure.core.SVG.SVG` extends `pure.core.XML.XML` for SVG tags. It chooses
self-closing rendering for selected childless elements, but it does not add an
SVG namespace automatically.

## Creating SVG Elements

Standard SVG tags come from the `pure.svg` functions; other tag names come from
reading the name off the class:

```python
from pure.svg import circle, rect, svg

c = circle().cx('50').cy('50').r('40').fill('red')
box = rect().x('10').y('10').width('80').height('80').fill('blue')
graphic = svg(c, box).width('100').height('100')
```

```python
from pure.core.SVG import SVG

# Any tag name, including custom elements
custom = SVG.customShape(SVG.innerPath('M10,10 L90,90'))
```

Unlike purephp, no alias is needed for `<use>` or `<switch>`: neither is a
Python keyword, so `pure.svg.use()` and `pure.svg.switch()` carry their own
names.

## Namespace and Document Roots

SVG is normally an inline fragment, so `isDocumentRoot()` returns `false` and
`render()` emits only the element. No `xmlns` attribute is inferred from the
class name. Declare it yourself when writing a standalone SVG file:

```python
from pure.svg import path, svg

icon = svg(
    path('M3 12l2-2m0 0l7-7 7 7')
).xmlns('http://www.w3.org/2000/svg').viewBox('0 0 24 24')

icon.save('icon.svg')
```

`save()` and `documentHeader()` still provide the XML declaration for the SVG
class; pass an explicit header when a different document prologue is required.
`renderXML()` also prepends that declaration, so use `render()` for an inline
fragment. The namespace is a document concern, not an escaping concern, and
should be fixed in the template rather than supplied by untrusted data.

## Self-Closing Tags

SVG has no void elements: `<feTile />` and `<feTile></feTile>` describe the same
document, so self-closing is a rendering style here, not a content rule. The
SVG class renders these elements self-closed when they are created without
children:

- `animate`, `animateMotion`, `animateTransform`, `circle`, `ellipse`,
  `feBlend`, `feColorMatrix`, `feComposite`, `feConvolveMatrix`,
  `feDistantLight`, `feDisplacementMap`, `feDropShadow`, `feFlood`, `feFuncA`,
  `feFuncB`, `feFuncG`, `feFuncR`, `feGaussianBlur`, `feImage`, `feMergeNode`,
  `feMorphology`, `feOffset`, `fePointLight`, `feSpotLight`, `feTile`,
  `feTurbulence`, `image`, `line`, `mpath`, `path`, `polygon`, `polyline`,
  `rect`, `set`, `stop`, `use`, `view`

Passing children keeps the element open, so animation elements can nest
`<mpath>` (`animateMotion(mpath().href('#p'))`) and `<use>` can nest
descriptive elements; containers such as `<g>`, `<text>` or `<feMerge>` are
never self-closed. `set_self_close(True)` still forces the short form (and
rejects children), `set_self_close(False)` forces the open/close pair.

```python
from pure.svg import svg, circle, rect

graphic = svg(
    circle().cx('50').cy('50').r('40').fill('red'),
    rect().x('10').y('10').width('80').height('80').fill('blue')
).width('100').height('100')
```

## Examples

### Basic Shapes

```python
from pure.svg import svg, circle, rect, line, polygon

shapes = svg(
    # Circle
    circle()
        .cx('50')
        .cy('50')
        .r('40')
        .fill('red')
        .stroke('black')
        .stroke_width('2'),

    # Rectangle
    rect()
        .x('120')
        .y('10')
        .width('80')
        .height('80')
        .fill('blue')
        .rx('10'),

    # Line
    line()
        .x1('220')
        .y1('10')
        .x2('280')
        .y2('90')
        .stroke('green')
        .stroke_width('3'),

    # Polygon (triangle)
    polygon()
        .points('300,10 340,90 260,90')
        .fill('yellow')
        .stroke('orange')
        .stroke_width('2')
).width('400').height('100').viewBox('0 0 400 100')

print(shapes.render())
```

### Icons

```python
from pure.svg import svg, path


def home_icon():
    return svg(
        path('M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6')
            .stroke('currentColor')
            .stroke_width('2')
            .fill('none')
            .stroke_linecap('round')
            .stroke_linejoin('round')
    ).width('24').height('24').viewBox('0 0 24 24')


print(home_icon().class_('icon').render())
```

### Animations

```python
from pure.core.SVG import SVG

animated_circle = SVG.svg(
    SVG.circle()
        .cx('50')
        .cy('50')
        .r('40')
        .fill('red'),
    SVG.animate()
        .attributeName('r')
        .values('40;45;40')
        .dur('2s')
        .repeatCount('indefinite')
).width('100').height('100')

print(animated_circle.render())
```

### Gradients and Filters

```python
from pure.svg import svg, defs, linearGradient, stop, rect

gradient_rect = svg(
    defs(
        linearGradient(
            stop().offset('0%').stopColor('#ff0000'),
            stop().offset('100%').stopColor('#0000ff')
        ).id('gradient1')
    ),
    rect()
        .x('10')
        .y('10')
        .width('80')
        .height('80')
        .fill('url(#gradient1)')
).width('100').height('100')

print(gradient_rect.render())
```

### Custom SVG Elements

```python
from pure.core.SVG import SVG

# Create custom SVG elements by reading the tag name off the class
custom_element = SVG.customShape(
    SVG.innerPath('M10,10 L90,90'),
    SVG.customAttribute('special-value')
).dataType('custom').class_('special-svg')

print(custom_element.render())
```

::: tip Snake case is spelled with a hyphen
An attribute name is stored with hyphens, so `stroke_width()` writes
`stroke-width`. The handful of SVG and HTML attributes that are genuinely
camelCase are written that way: `viewBox()`, `attributeName()`,
`repeatCount()`, `stopColor()`, `dataType()`. Both spellings of every other
attribute produce the same bytes in purephp and in purepy.
:::
