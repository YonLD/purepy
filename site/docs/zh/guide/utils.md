# 工具函数

Purepy 提供了一些实用的工具函数来简化开发，这些函数在设置元素属性时会自动使用。

## clx 函数

`clx` 函数用于合并类名，支持字符串、数组和条件类名。

### 基本用法 {#clx-basic-usage}

```python
from pure.clx import clx

# 合并多个字符串类名
classes = clx('btn', 'btn-primary', 'large')
print(classes)  # 输出: btn btn-primary large
```

### 条件类名

```python
from pure.clx import clx

is_active = True
is_disabled = False

classes = clx(
    'btn',
    'active' if is_active else None,
    'disabled' if is_disabled else None
)
print(classes)  # 输出: btn active
```

### 字典支持

```python
from pure.clx import clx

classes = clx(
    'btn',
    {
        'btn-primary': True,
        'active': True,
        'disabled': False,
        'large': None
    }
)
print(classes)  # 输出: btn btn-primary active
```

### 在 class_name() 方法中的内置使用

`class_name()` 方法内置了 `clx` 函数，可以直接传递多个参数：

```python
from pure.html import div

is_active = True
size = 'large'

div('内容').class_name('btn', 'btn-primary', 'active' if is_active else None, size).print()

# 等同于
from pure.clx import clx

classes = clx('btn', 'btn-primary', 'active' if is_active else None, size)
div('内容').class_name(classes).print()
```

## sty 函数

`sty` 函数用于将样式字典转换为 CSS 字符串。

### 基本用法 {#sty-basic-usage}

```python
from pure.sty import sty

styles = sty({
    'background-color': 'red',
    'height': '36px',
    'border': '1px solid #fff'
})
print(styles)  # 输出: background-color: red; height: 36px; border: 1px solid #fff;
```

### 条件样式

```python
from pure.sty import sty

is_visible = True
color = 'blue'

styles = sty({
    'color': color,
    'display': 'block' if is_visible else 'none',
    'opacity': 1 if is_visible else 0,
    'margin': None,  # 会被忽略
    'padding': False # 会被忽略
})
print(styles)  # 输出: color: blue; display: block; opacity: 1;
```

### 在 style() 方法中的内置使用

`style()` 方法内置了 `sty` 函数，可以直接传递字典：

```python
from pure.html import div

div('内容').style({
    'background-color': '#f0f0f0',
    'padding': '20px',
    'border-radius': '8px',
    'margin': '10px 0'
}).print()

# 等同于
from pure.sty import sty

styles = sty({
    'background-color': '#f0f0f0',
    'padding': '20px',
    'border-radius': '8px',
    'margin': '10px 0'
})
div('内容').style(styles).print()
```

## raw_html 函数

`raw_html` 函数用于插入原始 HTML 内容，不会被转义。

### 基本用法 {#raw-html-basic-usage}

```python
from pure.html import div
from pure.raw import raw_html

div(
    raw_html('<strong>这是粗体文本</strong>'),
    raw_html('<em>这是斜体文本</em>')
).print()
```

### 注意事项

使用 `raw_html` 时要确保内容是安全的，避免 XSS 攻击：

```python
from pure.html import div
from pure.raw import raw_html
import html

# 安全的使用方式
user_input = "<script>alert('xss')</script>"
safe_html = html.escape(user_input)
div(raw_html(safe_html)).print()

# 或者使用已知安全的 HTML
icon_html = '<svg><path d="..."/></svg>'
div(raw_html(icon_html)).print()
```

## raw_xml 函数

`raw_xml` 函数用于插入原始 XML 内容：

```python
from pure.raw import raw_xml

xml_content = raw_xml('<item id="1">内容</item>')
```

## 实际应用示例

### 动态按钮组件

```python
from pure.html import button

def Button(props):
    text = props.get('text', '')
    variant = props.get('variant', 'primary')
    size = props.get('size', 'medium')
    disabled = props.get('disabled', False)
    loading = props.get('loading', False)

    return button(
        '加载中...' if loading else text
    ).class_name(
        'btn',
        f'btn-{variant}',
        f'btn-{size}',
        'disabled' if disabled else None,
        'loading' if loading else None
    ).style({
        'opacity': 0.6 if disabled else 1,
        'cursor': 'not-allowed' if disabled else 'pointer'
    }).disabled(disabled)

# 使用示例
Button({
    'text': '提交',
    'variant': 'success',
    'size': 'large',
    'loading': False
}).print()
```

### 响应式卡片组件

```python
from pure.html import div, h3, p

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')
    featured = props.get('featured', False)
    theme = props.get('theme', 'light')

    return div(
        h3(title).class_name('card-title'),
        p(content).class_name('card-content')
    ).class_name(
        'card',
        f'card-{theme}',
        'card-featured' if featured else None
    ).style({
        'border-width': '2px' if featured else '1px',
        'box-shadow': '0 4px 12px rgba(0,0,0,0.15)' if featured else '0 2px 4px rgba(0,0,0,0.1)',
        'background-color': '#333' if theme == 'dark' else '#fff',
        'color': '#fff' if theme == 'dark' else '#333'
    })

# 使用示例
Card({
    'title': '特色卡片',
    'content': '这是一个特色卡片的内容',
    'featured': True,
    'theme': 'dark'
}).print()
```

## 下一步

- [基本用法](/zh/guide/basic-usage) - 学习基础语法和用法
- [组件](/zh/guide/components) - 学习如何创建和使用组件
- [TailwindCSS 集成](/zh/guide/tailwindcss) - 了解如何与 TailwindCSS 配合使用
