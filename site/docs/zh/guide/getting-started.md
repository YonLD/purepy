# 快速开始

**本页内容**：安装、从零写出一个 Purepy 应用，以及你会反复用到的核心概念。

## 安装

```bash
pip install -e .
```

## 你的第一个 Purepy 应用

新建一个文件，写下几行代码，然后运行它。

## 基本概念

### 1. 基于函数的元素

Purepy 里每个 HTML 标签都是一个函数，调用它就创建一个元素。

```python
from pure.html import div, h1, p

page = div(
    h1('Hello, Purepy!'),
    p('欢迎来到纯 Python 模板世界。'),
)

print(page)
```

### 2. 方法链式调用

每个元素都返回自身，因此调用可以一路串下去。

```python
from pure.html import div, h1

h1('标题').class_name('title').id('main-title')
div('内容').style('color: #333;')
```

### 3. 嵌套元素

把元素作为另一个元素的子节点，就得到了嵌套结构。

```python
from pure.html import div, h1, p, ul, li

page = div(
    h1('用户列表'),
    ul(
        li('Ada'),
        li('Grace'),
    ),
).class_name('container')

print(page)
```

## 使用属性

属性通过方法调用来设置；未知的方法名会直接变成一个属性名。

### CSS 类名

```python
from pure.html import div, span

div('内容').class_name('card')
span('标签').class_name('badge', 'badge-primary')
```

多个类名用空格连接。`class_()` 与 `class_name()` 等价。

### data 属性

下划线会变成连字符，因此 `data_id()` 渲染出 `data-id`。

```python
from pure.html import div

div('卡片').data_id('7').data_role('banner')
```

## 使用工具函数

### 用 clx 处理类名

`clx()` 接收一个基础类名和一组条件类名，只输出条件为真的那些。

```python
from pure.clx import clx
from pure.html import div

is_active = True
is_large = False

classes = clx('container', {'active': is_active, 'large': is_large})

print(div('内容').class_name(classes))
```

输出：

```html
<div class="container active">内容</div>
```

### 用 sty 处理样式

`sty()` 把一个字典渲染成 `style` 属性。

```python
from pure.sty import sty
from pure.html import div

styles = sty({
    'color': 'red',
    'font-size': '16px',
    'background-color': '#f0f0f0',
})

print(div('内容').style(styles))
```

输出：

```html
<div style="color: red; font-size: 16px; background-color: #f0f0f0;">内容</div>
```

## 创建组件

组件就是一个返回元素的函数。

```python
from pure.html import div, h2, p


def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')

    return div(
        h2(title).class_name('card-title'),
        p(content),
    ).class_name('card')


print(Card({'title': '标题', 'content': '正文'}))
```

::: tip 组件还有更完整的形式
上面的函数式组件足以应对单文件模板。当你想给组件一个名字、一份声明的数据契约，
以及预编译和静态检查能力时，把它升级为**注册单元**——见
[组件](/zh/guide/components#注册组件)。 :::

## 构建一个完整页面

把上面的零件拼起来，就得到一份完整的文档。

```python
from pure.html import body, div, h1, html, p

page = html(
    body(
        div(
            h1('欢迎'),
            p('这是一个用 Purepy 构建的页面。'),
        ).class_name('content'),
    )
)

page.save('index.html')
```

`save()` 会自动为 HTML 文档根补上 `<!DOCTYPE html>`。

## 处理列表

列表推导式可以自然地配合元素使用。

```python
from pure.html import li, ul

items = ['项目 1', '项目 2', '项目 3']

print(ul(*[li(item) for item in items]))
```

## 条件渲染

用条件表达式决定渲染什么。

```python
from pure.html import div, p

is_logged_in = True

print(
    div(
        p('欢迎回来') if is_logged_in else p('请先登录'),
    )
)
```

## 下一步

- [核心概念](/zh/guide/concepts)——元素、属性与渲染
- [组件](/zh/guide/components)——注册单元与数据契约
- [属性与槽位](/zh/guide/props)——slot 速查
- [故障排查](/zh/guide/troubleshooting)——出错时怎么办

## 实践建议

- **先渲染，再排版。** 输出不会被重新缩进，需要缩进时用 `Raw` 或 CSS 格式化工具。
- **记住 trait 是数据契约。** 模板读什么，`prepare()` 就声明什么；`pure check` 会帮你核对。
- **在开发环境打开守卫。** `Compile.guard(True)` 会告诉你模板读了什么、调用绑了什么。
- **shape 只建一次。** 把它记住，别在请求里反复构建。
