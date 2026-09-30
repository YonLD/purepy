# SVG 与 XML 支持

**前置**：[基本用法](/zh/guide/basic-usage)；**本页内容**：构建 SVG 图形与 XML 文档，并为其编译用于导出。

Purepy 用与 HTML 同样优雅的语法提供了完整的 SVG 图形与 XML 文档支持。

::: tip SVG 与 XML 的两条路径
HTML、SVG 和 XML 的标签实例都继承 `Tag`，所以它们都可以包进
`Compile.shape()` 并带数据渲染——见[编译渲染](/zh/guide/compiled)。下面 SVG
部分是标签 API 参考，用 `render()` / `print()` 立即输出；XML 部分走编译路径。
:::

## SVG 支持

### 基础 SVG 创建

用 `pure.svg` 的函数创建 SVG 图形，自定义标签则从类上读取标签名：

```python
from pure.svg import svg, circle, rect

graphic = svg(
    circle()
        .cx('50')
        .cy('50')
        .r('40')
        .fill('red'),
    rect()
        .x('10')
        .y('10')
        .width('80')
        .height('80')
        .fill('blue')
).width('100').height('100')

print(graphic.render())  # 输出 SVG 标记
```

### 函数与类上构造器

**适合用函数：**
- 标签是预定义的 HTML/SVG 标签
- 处理动态值（子节点与属性）

**适合从类上读取标签名：**
- 创建自定义或非标准标签
- 标签名需要动态决定

两者构建的是同一个 `Tag` 对象；函数是常用名字的轻量显式包装。自定义标签用类上
的形式：

```python
from pure.core.SVG import SVG

# 很适合非标准或自定义的 SVG 元素
custom_element = SVG.customTag(SVG.innerElement('content')) \
    .customAttribute('value')

# 动态标签名也可以
tag = 'myCustomSvgElement'
web_component = getattr(SVG, tag)() \
    .data_id('unique') \
    .class_('custom-svg')
```

### 复杂 SVG 示例

#### 创建图标

```python
from pure.svg import svg, path

ROTATIONS = {
    'up': 'rotate(-90 12 12)',
    'down': 'rotate(90 12 12)',
    'left': 'rotate(180 12 12)',
}


def chevron_icon(direction='right'):
    return svg(
        path('M9 18l6-6-6-6')
            .stroke('currentColor')
            .stroke_width('2')
            .fill('none')
            .stroke_linecap('round')
            .stroke_linejoin('round')
            .transform(ROTATIONS.get(direction, ''))
    ).width('24').height('24').viewBox('0 0 24 24')


print(chevron_icon('down').class_('icon').render())
```

#### 动画 SVG

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

## XML 支持

XML 标签同样继承 `Tag`，所以文档是作为编译后的 shape 构建的：树和它的 slot 每个
进程创建一次，每次导出只需绑定数据并保存或打印。

### 编译后的 XML 文档

下面的 `address` 渲染一条记录；`city` 是可选的，只有数据提供了它才出现：

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot
from pure.core.XML import XML

address = Compile.shape(
    XML.address(
        XML.street(Slot.value('street')),
        Slot.if_('city', XML.city(Slot.value('city'))),
        XML.state(Slot.value('state')),
        XML.zip(Slot.value('zip'))
    )
)

customers = Compile.shape(
    XML.customers(
        XML.customer(
            XML.name('Charter Group'),
            Slot.raw('addresses')
        ).id('55000')
    )
)

body = ''.join(address(data) for data in [
    {'street': '100 Main', 'city': 'Framingham', 'state': 'MA', 'zip': '01701'},
    {'street': '720 Prospect', 'city': 'Framingham', 'state': 'MA', 'zip': '01701'},
    {'street': '120 Ridge', 'state': 'MA', 'zip': '01760'},
])

print(customers({'addresses': body}))
```

`Slot.if_()` 会为缺少 `city` 的记录跳过 `city` 元素——缺失的键为假值，永远不会抛错。
要写入文件请用 `Shape.save()`，它默认会补上根标签的文档头（自定义 header 是它的
第三个参数）。

::: tip 调用 shape 就等于渲染
一个 `Shape` 是可调用的：`address(data)` 直接返回渲染结果，所以构建一次、多次渲染，
不必把渲染器存进变量里。需要字节数或写入文件时用 `address.save(path, data)`。
:::

### 数据驱动的元素

标签名在构建期就固定了，所以动态的键和值要成为 slot——这里是一组设置项的 `key`
属性与文本内容：

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot
from pure.core.XML import XML

setting = Compile.shape(
    XML.setting(Slot.value('value')).key(Slot.value('key'))
)

config = Compile.shape(
    XML.configuration(Slot.each('settings', setting))
)

print(config({'settings': [
    {'key': 'host', 'value': 'localhost'},
    {'key': 'port', 'value': '3306'},
    {'key': 'debug', 'value': 'true'},
]}))
```

当结构本身也要随数据变化时，请用 `Slot.if_()` 或在数据层做分发——shape 的标签集合
是固定的。

## 重要：字符串内容会被转义

⚠️ **安全提示**：字符串内容总是被转义，所以看起来像 XML/SVG 的文本是安全的，
而且仍然可见：

```python
from pure.core.Raw import Raw
from pure.core.XML import XML

# ✅ 字符串里的 XML 标签被转义，不会被解析
print(XML.root('<item>This stays visible</item>').render())
# 输出: <root>&lt;item&gt;This stays visible&lt;/item&gt;</root>

# ✅ 用 Raw.of 输出 XML 内容
print(XML.root(Raw.of('<item>This is preserved</item>')).render())
# 输出: <root><item>This is preserved</item></root>
```

**什么时候用 `Raw.of()`：**
- 包含 CDATA 段
- 嵌入外部的 XML/SVG 内容
- 处理预格式化的标记
- 包含复杂的嵌套结构

两条渲染路径的行为一致：绑定数据由 `Slot.value()` 转义，而 `Slot.raw()` 是
`Raw.of()` 的逐字版本——当数据需要保留自身标记时使用。

## 最佳实践

1. **预定义的 HTML/SVG 标签用函数** — 在性能和可读性之间取得最好平衡
2. **自定义标签从类上读取** — 需要动态创建标签时
3. **可信内容用 `Raw.of()`** — 需要保留标记结构时
4. **按需组合** — 可以根据具体场景混用

## 下一步

- [API 参考](/zh/api/) — 完整 API 文档
- [组件](/zh/guide/components) — 学习如何创建可复用组件
- [工具函数](/zh/guide/utils) — 了解辅助函数
