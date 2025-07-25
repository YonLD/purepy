# 基本用法

本指南介绍 Purepy 的基本用法和语法。

## 创建元素

### 1. 基本元素

使用函数调用创建 HTML 元素：

```python
from pure.html import div, h1, p

# 创建简单元素
div('Hello World')
h1('标题')
p('段落内容')
```

### 2. 设置属性

使用链式调用设置元素属性：

```python
from pure.html import div

div('内容') \
    .class_name('container') \
    .id('main') \
    .data_key('primary') \
    .to_print()
```

## 重要用法说明

### 1. class_name 方法

由于 `class` 是 Python 的关键字，Purepy 使用 `class_name` 方法来设置 CSS 类：

```python
from pure.html import div

# 设置 CSS 类
div('内容').class_name('container').to_print()
```

### 2. 属性命名规则

由于 `-` 在 Python 中有特殊含义，类似 `data-id` 这种属性需要改成 `data_id`：

```python
from pure.html import div

div('内容') \
    .data_id('123') \
    .data_type('card') \
    .aria_label('按钮') \
    .to_print()
```

输出：
```html
<div data-id="123" data-type="card" aria-label="按钮">内容</div>
```

### 3. 样式处理

可以使用字典来设置样式：

```python
from pure.html import div
from pure.sty import sty

# 使用字典设置样式
styles = sty({
    'color': 'red',
    'font-size': '16px',
    'background-color': '#f0f0f0'
})

div('内容').style(styles).to_print()
```

### 4. 类名处理

使用 clx 函数处理条件类名：

```python
from pure.html import div
from pure.clx import clx

is_active = True
is_large = False

# 条件类名
classes = clx('btn', {'active': is_active, 'large': is_large})
div('按钮').class_name(classes).to_print()
```

## 嵌套元素

### 1. 基本嵌套

```python
from pure.html import div, h1, p

div(
    h1('标题'),
    p('内容')
).to_print()
```

### 2. 复杂嵌套

```python
from pure.html import div, header, nav, ul, li, a, main, section, h2, p

div(
    header(
        nav(
            ul(
                li(a('首页').href('/')),
                li(a('关于').href('/about')),
                li(a('联系').href('/contact'))
            )
        )
    ),
    main(
        section(
            h2('欢迎'),
            p('这是主要内容区域。')
        )
    )
).class_name('layout').to_print()
```

## 条件渲染

### 1. 使用条件表达式

```python
from pure.html import div, p

is_logged_in = True

div(
    p('欢迎回来！') if is_logged_in else p('请登录'),
    p('这是公共内容')
).to_print()
```

### 2. 使用列表推导

```python
from pure.html import div, ul, li

items = ['苹果', '香蕉', '橙子']

div(
    ul(
        *[li(item) for item in items]
    )
).to_print()
```

## 输出方法

### 1. 转换为字符串

```python
from pure.html import div

element = div('Hello World')
html_string = str(element)
print(html_string)
```

### 2. 直接打印

```python
from pure.html import div

div('Hello World').to_print()
```

### 3. 保存到文件

```python
from pure.html import html, head, title, body, div

page = html(
    head(title('我的页面')),
    body(div('Hello World'))
)

page.to_save('output.html')
```

## 最佳实践

### 1. 组件化

将重复的代码封装成函数：

```python
from pure.html import div, h2, p, a

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')
    link = props.get('link', '#')

    return div(
        h2(title),
        p(content),
        a('了解更多').href(link)
    ).class_name('card')

# 使用组件
Card({
    'title': '标题',
    'content': '内容',
    'link': '/more'
}).to_print()
```

### 2. 数据驱动

使用数据来生成内容：

```python
from pure.html import div, ul, li

def ItemList(items):
    return div(
        ul(
            *[li(item) for item in items]
        )
    ).class_name('item-list')

# 使用
items = ['项目1', '项目2', '项目3']
ItemList(items).to_print()
```

## 下一步

- [组件](/guide/components) - 学习如何创建和使用组件
- [API 参考](/api/) - 了解所有可用的标签和方法
