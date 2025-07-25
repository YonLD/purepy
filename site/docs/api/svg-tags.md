# SVG 标签

Purepy 提供了完整的 SVG（可缩放矢量图形）标签支持。所有 SVG 标签都可以通过 `pure.svg` 模块导入。

## SVG 根元素

### svg 元素

```python
from pure.svg import svg

# 基本 SVG 容器
svg_container = svg(
    # SVG 内容
).width('200').height('200').viewBox('0 0 200 200')

# 带命名空间的 SVG
svg_with_namespace = svg(
    # SVG 内容
).xmlns('http://www.w3.org/2000/svg').version('1.1')
```

## 基本形状

### 矩形

```python
from pure.svg import rect

# 基本矩形
basic_rect = rect().x('10').y('10').width('100').height('50').fill('blue')

# 圆角矩形
rounded_rect = rect() \
    .x('10').y('10').width('100').height('50') \
    .rx('5').ry('5') \
    .fill('blue').stroke('black').stroke_width('2')
```

### 圆形

```python
from pure.svg import circle

# 基本圆形
basic_circle = circle().cx('50').cy('50').r('40').fill('red')

# 带边框的圆形
circle_with_stroke = circle() \
    .cx('50').cy('50').r('40') \
    .fill('red').stroke('black').stroke_width('3')
```

### 椭圆

```python
from pure.svg import ellipse

# 椭圆
ellipse_shape = ellipse() \
    .cx('100').cy('50').rx('80').ry('30') \
    .fill('green').stroke('blue').stroke_width('2')
```

### 直线

```python
from pure.svg import line

# 基本直线
basic_line = line() \
    .x1('0').y1('0').x2('100').y2('100') \
    .stroke('black').stroke_width('2')

# 虚线
dashed_line = line() \
    .x1('0').y1('50').x2('200').y2('50') \
    .stroke('red').stroke_width('3') \
    .stroke_dasharray('5,5')
```

### 折线

```python
from pure.svg import polyline

# 折线
polyline_shape = polyline() \
    .points('0,0 50,25 100,0 150,25 200,0') \
    .fill('none').stroke('blue').stroke_width('2')
```

### 多边形

```python
from pure.svg import polygon

# 三角形
triangle = polygon() \
    .points('50,0 0,100 100,100') \
    .fill('yellow').stroke('red').stroke_width('2')

# 五角星
star = polygon() \
    .points('50,0 61,35 98,35 68,57 79,91 50,70 21,91 32,57 2,35 39,35') \
    .fill('gold').stroke('orange').stroke_width('1')
```

## 路径

### path 元素

```python
from pure.svg import path

# 基本路径
basic_path = path() \
    .d('M 10 10 L 90 90 L 10 90 Z') \
    .fill('purple').stroke('black').stroke_width('2')

# 贝塞尔曲线
bezier_curve = path() \
    .d('M 10 80 Q 52.5 10, 95 80 T 180 80') \
    .fill('none').stroke('blue').stroke_width('3')

# 圆弧
arc_path = path() \
    .d('M 10 50 A 40 40 0 0 1 90 50') \
    .fill('none').stroke('green').stroke_width('4')
```

## 文本

### text 元素

```python
from pure.svg import text, tspan

# 基本文本
basic_text = text('Hello SVG') \
    .x('50').y('50') \
    .font_family('Arial').font_size('16').fill('black')

# 多行文本
multiline_text = text(
    tspan('第一行').x('50').dy('0'),
    tspan('第二行').x('50').dy('20'),
    tspan('第三行').x('50').dy('20')
).font_family('Arial').font_size('14').fill('blue')

# 路径上的文本
from pure.svg import textPath

text_on_path = text(
    textPath('沿路径的文本').href('#path1')
).font_family('Arial').font_size('12').fill('red')
```

## 分组和结构

### g 元素（分组）

```python
from pure.svg import g

# 基本分组
basic_group = g(
    circle().cx('25').cy('25').r('20').fill('red'),
    rect().x('5').y('5').width('40').height('40').fill('none').stroke('blue')
).transform('translate(50, 50)')

# 带样式的分组
styled_group = g(
    circle().cx('0').cy('0').r('10'),
    circle().cx('20').cy('0').r('10'),
    circle().cx('10').cy('15').r('10')
).fill('green').stroke('black').stroke_width('1').transform('scale(2)')
```

### defs 元素（定义）

```python
from pure.svg import defs, linearGradient, stop, pattern

# 定义渐变
gradient_defs = defs(
    linearGradient(
        stop().offset('0%').stop_color('red'),
        stop().offset('100%').stop_color('blue')
    ).id('gradient1').x1('0%').y1('0%').x2('100%').y2('0%')
)

# 使用渐变
rect_with_gradient = rect() \
    .x('10').y('10').width('100').height('50') \
    .fill('url(#gradient1)')
```

### use 元素（重用）

```python
from pure.svg import use

# 定义可重用元素
reusable_shape = g(
    circle().cx('0').cy('0').r('10').fill('blue'),
    rect().x('-5').y('-5').width('10').height('10').fill('red')
).id('shape1')

# 重用元素
use_shape1 = use().href('#shape1').x('50').y('50')
use_shape2 = use().href('#shape1').x('100').y('100').transform('scale(1.5)')
```

## 渐变和图案

### 线性渐变

```python
from pure.svg import linearGradient, stop

# 水平渐变
horizontal_gradient = linearGradient(
    stop().offset('0%').stop_color('red').stop_opacity('1'),
    stop().offset('50%').stop_color('yellow').stop_opacity('0.8'),
    stop().offset('100%').stop_color('blue').stop_opacity('1')
).id('horizontal').x1('0%').y1('0%').x2('100%').y2('0%')

# 垂直渐变
vertical_gradient = linearGradient(
    stop().offset('0%').stop_color('white'),
    stop().offset('100%').stop_color('black')
).id('vertical').x1('0%').y1('0%').x2('0%').y2('100%')
```

### 径向渐变

```python
from pure.svg import radialGradient

# 径向渐变
radial_gradient = radialGradient(
    stop().offset('0%').stop_color('white'),
    stop().offset('70%').stop_color('blue'),
    stop().offset('100%').stop_color('darkblue')
).id('radial').cx('50%').cy('50%').r('50%')
```

### 图案

```python
from pure.svg import pattern

# 重复图案
repeat_pattern = pattern(
    rect().x('0').y('0').width('10').height('10').fill('red'),
    circle().cx('5').cy('5').r('3').fill('blue')
).id('pattern1').x('0').y('0').width('20').height('20').patternUnits('userSpaceOnUse')
```

## 滤镜效果

### filter 元素

```python
from pure.svg import filter, feGaussianBlur, feOffset, feFlood, feComposite

# 阴影滤镜
shadow_filter = filter(
    feOffset().in_('SourceGraphic').dx('3').dy('3').result('offset'),
    feGaussianBlur().in_('offset').stdDeviation('2').result('blur'),
    feFlood().flood_color('black').flood_opacity('0.3').result('color'),
    feComposite().in_('color').in2('blur').operator('in').result('shadow'),
    feComposite().in_('SourceGraphic').in2('shadow').operator('over')
).id('shadow')

# 模糊滤镜
blur_filter = filter(
    feGaussianBlur().in_('SourceGraphic').stdDeviation('3')
).id('blur')
```

## 动画

### animate 元素

```python
from pure.svg import animate, animateTransform

# 属性动画
color_animation = animate() \
    .attributeName('fill') \
    .values('red;blue;red') \
    .dur('3s') \
    .repeatCount('indefinite')

# 变换动画
rotation_animation = animateTransform() \
    .attributeName('transform') \
    .type('rotate') \
    .values('0 50 50;360 50 50') \
    .dur('2s') \
    .repeatCount('indefinite')
```

### animateMotion 元素

```python
from pure.svg import animateMotion, mpath

# 路径动画
motion_animation = animateMotion(
    mpath().href('#motionPath')
).dur('5s').repeatCount('indefinite')
```

## 裁剪和遮罩

### clipPath 元素

```python
from pure.svg import clipPath

# 裁剪路径
clip_path = clipPath(
    circle().cx('50').cy('50').r('40')
).id('clip1')

# 应用裁剪
clipped_rect = rect() \
    .x('0').y('0').width('100').height('100') \
    .fill('blue').clip_path('url(#clip1)')
```

### mask 元素

```python
from pure.svg import mask

# 遮罩
mask_element = mask(
    rect().x('0').y('0').width('100').height('100').fill('white'),
    circle().cx('50').cy('50').r('30').fill('black')
).id('mask1')

# 应用遮罩
masked_rect = rect() \
    .x('0').y('0').width('100').height('100') \
    .fill('red').mask('url(#mask1)')
```

## 标记

### marker 元素

```python
from pure.svg import marker

# 箭头标记
arrow_marker = marker(
    path().d('M 0 0 L 10 5 L 0 10 Z').fill('black')
).id('arrow') \
  .markerWidth('10').markerHeight('10') \
  .refX('9').refY('5') \
  .orient('auto').markerUnits('strokeWidth')

# 带标记的线
line_with_marker = line() \
    .x1('10').y1('10').x2('100').y2('100') \
    .stroke('black').stroke_width('2') \
    .marker_end('url(#arrow)')
```

## 完整示例

### 复杂 SVG 图形

```python
from pure.svg import svg, defs, linearGradient, stop, rect, circle, text, g

# 创建完整的 SVG 图形
complete_svg = svg(
    defs(
        linearGradient(
            stop().offset('0%').stop_color('#ff7e5f'),
            stop().offset('100%').stop_color('#feb47b')
        ).id('gradient')
    ),
    
    # 背景
    rect().x('0').y('0').width('200').height('200').fill('url(#gradient)'),
    
    # 图形组
    g(
        circle().cx('100').cy('100').r('50').fill('white').stroke('#333').stroke_width('3'),
        text('SVG').x('100').y('110').text_anchor('middle').font_family('Arial').font_size('20').fill('#333')
    ).transform('translate(0, 0)')
    
).width('200').height('200').viewBox('0 0 200 200')

# 保存 SVG
complete_svg.to_save('example.svg')
```

### 响应式 SVG

```python
# 响应式 SVG 图标
responsive_icon = svg(
    path().d('M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z') \
          .fill('currentColor')
).viewBox('0 0 24 24').class_name('icon')
```

## 样式和属性

### 常用样式属性

```python
# 填充和描边
element.fill('red')                    # 填充颜色
element.stroke('blue')                 # 描边颜色
element.stroke_width('2')              # 描边宽度
element.stroke_dasharray('5,5')        # 虚线样式
element.stroke_linecap('round')        # 线端样式
element.stroke_linejoin('round')       # 线连接样式

# 透明度
element.opacity('0.8')                 # 整体透明度
element.fill_opacity('0.5')            # 填充透明度
element.stroke_opacity('0.7')          # 描边透明度

# 变换
element.transform('translate(10, 20)') # 平移
element.transform('rotate(45)')        # 旋转
element.transform('scale(1.5)')        # 缩放
element.transform('skewX(15)')         # 倾斜
```

## 下一步

- [核心类](/api/core) - 了解 SVG 类的详细功能
- [HTML 标签](/api/html-tags) - 了解 HTML 标签
- [基本用法](/guide/basic-usage) - 学习如何使用 SVG 标签
