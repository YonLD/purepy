# SVG 类

**本页内容**：`SVG` 类——SVG 元素的创建、命名空间与文档根、自闭合规则，以及常用示例。

`pure.core.SVG.SVG` 继承 `pure.core.XML.XML`，用于 SVG 标签。它会为部分无子元素
的元素选择自闭合输出，但不会自动补上 SVG 命名空间。

## 创建 SVG 元素

标准 SVG 标签来自 `pure.svg` 模块；其它标签名从类上读取：

```python
from pure.svg import circle, rect, svg

c = circle().cx('50').cy('50').r('40').fill('red')
box = rect().x('10').y('10').width('80').height('80').fill('blue')
graphic = svg(c, box).width('100').height('100')
```

```python
from pure.core.SVG import SVG

# 任意标签名都可以，包括自定义元素
custom = SVG.customShape(SVG.innerPath('M10,10 L90,90'))
```

与 purephp 不同，`<use>` 和 `<switch>` 不需要别名——它们都不是 Python 关键字，所以
`pure.svg.use()` 和 `pure.svg.switch()` 直接使用原名。

## 命名空间与文档根

SVG 通常是内联片段，所以 `isDocumentRoot()` 返回 `false`，`render()` 只输出元素本身。
类名不会推导出 `xmlns` 属性。要写独立的 SVG 文件，请自行声明：

```python
from pure.svg import path, svg

icon = svg(
    path('M3 12l2-2m0 0l7-7 7 7')
).xmlns('http://www.w3.org/2000/svg').viewBox('0 0 24 24')

icon.save('icon.svg')
```

`save()` 和 `documentHeader()` 仍会为 SVG 类提供 XML 声明；需要其它文档序言时传入
显式的 header。内联片段请用 `render()`，因为 `renderXML()` 也会补上 XML 声明。
命名空间属于文档层面的问题，不是转义问题，应该在模板里写死，而不是由不可信数据
提供。

## 自闭合标签

SVG 没有空元素：`<feTile />` 和 `<feTile></feTile>` 描述的是同一份文档，所以自闭合
在这里是一种输出风格，而不是内容规则。创建时没有子节点的以下元素，SVG 类会输出
自闭合形式：

- `animate`、`animateMotion`、`animateTransform`、`circle`、`ellipse`、
  `feBlend`、`feColorMatrix`、`feComposite`、`feConvolveMatrix`、
  `feDistantLight`、`feDisplacementMap`、`feDropShadow`、`feFlood`、`feFuncA`、
  `feFuncB`、`feFuncG`、`feFuncR`、`feGaussianBlur`、`feImage`、`feMergeNode`、
  `feMorphology`、`feOffset`、`fePointLight`、`feSpotLight`、`feTile`、
  `feTurbulence`、`image`、`line`、`mpath`、`path`、`polygon`、`polyline`、
  `rect`、`set`、`stop`、`use`、`view`

传入子节点会保持元素开启，所以动画元素可以嵌套 `<mpath>`
（`animateMotion(mpath().href('#p'))`），`<use>` 可以嵌套描述性元素；`<g>`、
`<text>`、`<feMerge>` 这样的容器永远不会被自闭合。`set_self_close(True)` 仍然
强制短形式（并拒绝子节点），`set_self_close(False)` 强制成对标签。

```python
from pure.svg import svg, circle, rect

graphic = svg(
    circle().cx('50').cy('50').r('40').fill('red'),
    rect().x('10').y('10').width('80').height('80').fill('blue')
).width('100').height('100')
```

## 示例

### 基础形状

```python
from pure.svg import svg, circle, rect, line, polygon

shapes = svg(
    # 圆形
    circle()
        .cx('50')
        .cy('50')
        .r('40')
        .fill('red')
        .stroke('black')
        .stroke_width('2'),

    # 矩形
    rect()
        .x('120')
        .y('10')
        .width('80')
        .height('80')
        .fill('blue')
        .rx('10'),

    # 直线
    line()
        .x1('220')
        .y1('10')
        .x2('280')
        .y2('90')
        .stroke('green')
        .stroke_width('3'),

    # 多边形（三角形）
    polygon()
        .points('300,10 340,90 260,90')
        .fill('yellow')
        .stroke('orange')
        .stroke_width('2')
).width('400').height('100').viewBox('0 0 400 100')

print(shapes.render())
```

### 图标

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

### 动画

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

### 渐变与滤镜

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

### 自定义 SVG 元素

```python
from pure.core.SVG import SVG

# 从类上读取标签名即可创建自定义 SVG 元素
custom_element = SVG.customShape(
    SVG.innerPath('M10,10 L90,90'),
    SVG.customAttribute('special-value')
).dataType('custom').class_('special-svg')

print(custom_element.render())
```

::: tip 下划线写法对应连字符
属性名以连字符存储，所以 `stroke_width()` 写出 `stroke-width`。少数确实是驼峰的
SVG 和 HTML 属性就按驼峰写：`viewBox()`、`attributeName()`、`repeatCount()`、
`stopColor()`、`dataType()`。其它属性的两种拼写在 purephp 和 purepy 中产生相同的
字节。
:::
