# 组件

组件是 Purepy 的核心概念之一，它允许你将 UI 拆分成独立、可重用的部分。本指南将介绍如何创建和使用组件。

## 什么是组件？

在 Purepy 中，组件是返回元素结构的函数。组件接收参数（称为"props"），并返回描述界面的元素。

## 基本组件

### 创建组件

组件是一个接收 props 参数并返回元素的函数：

```python
from pure.html import div, h2, p

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')

    return div(
        h2(title).class_name('card-title'),
        p(content).class_name('card-content')
    ).class_name('card')
```

### 使用组件

```python
# 使用组件
my_card = Card({
    'title': '欢迎使用 Purepy',
    'content': '这是一个基于 Python 的模板引擎'
})

# 渲染组件
my_card.print()
```

输出：

```html
<div class="card">
    <h2 class="card-title">欢迎使用 Purepy</h2>
    <p class="card-content">这是一个基于 Python 的模板引擎</p>
</div>
```

## 注册组件

返回标签的普通函数对于单文件里的模板已经够用。**注册单元**则额外带来名字、声明的
数据契约、预编译能力和静态检查。本节讲后者。

一个注册组件由三部分组成：

| 部分 | 是什么 |
| --- | --- |
| **调用函数** | 返回 `component(name, ...)` 的函数，因此调用点是一串具名参数 |
| **factory** | 返回标签树，其中的数据位置是 `Slot` 占位符。每个进程**只运行一次** |
| **`prepare()`** | 接收调用点参数，返回 slot 读取的数据字典 |

把这三部分放进一个 `*.cmp.py` 文件：

```python [components/Card.cmp.py]
from pure.core.Slot import Slot

from pure.component import component, register

from pure.html import div, h2, p


def Card(*children):
    return component('Card', *children)


def factory():
    return div(
        h2(Slot.value('title')),
        p(Slot.value('content')),
    ).class_('card')


def prepare(title, content):
    return {'title': title, 'content': content}


register(Card, factory, prepare=prepare)
```

加载并使用：

```python
from pure.loader import load_module

card = load_module('components/Card.cmp.py', 'Card')

print(card.Card().title('Title').content('Content'))
```

输出：

```html
<div class="card"><h2>Title</h2><p>Content</p></div>
```

::: warning `*.cmp.py` 文件不能按名字 import
那个点属于文件名，因此 `import components.Card` 行不通。请用
`pure.loader.load_module()`，或者让 `pure compile` 与 `pure check` 去发现它。
:::

### 为什么要有 factory

factory 返回的是由 `Slot` 占位符组成的标签树，而不是渲染结果。正是这个分离让后面
几件事成为可能：

- 这棵树是**形状数据**，因此可以只编译一次并复用——见[编译渲染](/zh/guide/compiled)。
- 编译器能看出有哪些 slot，因此 `pure check` 能在任何渲染发生**之前**校验调用点。
- 注册表可以加载预构建的产物，而不是重建整棵树——见[产物与部署](/zh/guide/artifacts)。

### `prepare()` 就是契约

`prepare()` 是调用点参数变成 slot 数据的地方，它的签名就是组件的公开契约，
`pure check` 会读取它：

```python
from pure.component.Prop import Prop
from pure.component.Trusted import Trusted

def prepare(
    title,
    subtitle: Prop = Prop(deprecated='改传第二个 title'),
    html: Trusted = None,
):
    return {'title': title, 'subtitle': subtitle, 'body': html}
```

- 普通参数是必填的，其注解是期望的类型。
- `Prop(deprecated=...)` 保留该参数，但在开发守卫下发出警告。
- `Trusted` 标记一个值本身就是可信标记，不会再被转义。
- `Prop(slot=...)` 与 `Prop(item=...)` 声明列表或子值如何映射到模板的 slot。

不一致是静态错误，而不是运行时的意外：

```bash
$ pure check src
error: component 'Bad' -> src/Bad.cmp.py: slot 'rows' is a list slot but parameter $rows is typed str
```

### 组件内部的 Slot

factory 使用的就是任何形状都用的那套 `Slot` 词汇：

```python
from pure.core.Slot import Slot

def factory():
    return ul(
        Slot.each('items', item_shape),
        Slot.if_('showFooter', footer_shape),
    )
```

- `Slot.value()`——转义后的文本，或属性值
- `Slot.raw()`——原样标记，也是渲染好的子组件进入模板的唯一途径
- `Slot.child()`——嵌套的标记树，绑定到一个字典
- `Slot.each()`——一个列表，每个元素跑一次内部形状
- `Slot.if_()`——分支，共享当前作用域

`.required(False)` 与 `.default(value)` 让 slot 变为可选；完整参考见
[属性与槽位](/zh/guide/props#slot-速查)。

### 覆盖一次注册

两个单元不能占用同一个名字；第二次 `register()` 会抛异常，除非传 `override=True`，
此时会回收前一个文件占用的名字。确切签名见[组件 API](/zh/api/component)。

## 组件设计模式

### 1. 单一职责

每个组件应该只做一件事：

```python
# 不好的做法：一个组件做太多事情
def Page(props):
    return div(
        # 头部
        div(
            h1('网站标题'),
            nav(
                a('首页').href('/'),
                a('关于').href('/about'),
                a('联系').href('/contact')
            )
        ).class_name('header'),

        # 内容
        div(
            h2(props.get('title')),
            p(props.get('content'))
        ).class_name('content'),

        # 页脚
        div(
            p('版权所有 © 2024')
        ).class_name('footer')
    )

# 好的做法：拆分成多个组件
def Header():
    return div(
        h1('网站标题'),
        nav(
            a('首页').href('/'),
            a('关于').href('/about'),
            a('联系').href('/contact')
        )
    ).class_name('header')

def Content(props):
    return div(
        h2(props.get('title')),
        p(props.get('content'))
    ).class_name('content')

def Footer():
    return div(
        p('版权所有 © 2024')
    ).class_name('footer')

def Page(props):
    return div(
        Header(),
        Content(props),
        Footer()
    )
```

### 2. 组合优于继承

使用组合来构建复杂组件：

```python
def Button(props):
    variant = props.get('variant', 'primary')
    size = props.get('size', 'medium')
    text = props.get('text', '')

    return button(text).class_name(f'btn btn-{variant} btn-{size}')

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')

    return div(
        h2(title),
        p(content),
        Button({
            'text': '了解更多',
            'variant': 'secondary',
            'size': 'small'
        })
    ).class_name('card')
```

### 3. 容器组件

创建可以包含其他内容的组件：

```python
def Container(props):
    children = props.get('children', [])

    return div(
        *children
    ).class_name('container')

# 使用
Container({
    'children': [
        h1('标题'),
        p('内容'),
        button('点击')
    ]
})
```

## 组件通信

### 1. 通过 Props 传递数据

从父组件向子组件传递数据：

```python
def Parent():
    data = {
        'title': '标题',
        'content': '内容'
    }

    return div(
        Child(data)
    )

def Child(props):
    return div(
        h2(props.get('title')),
        p(props.get('content'))
    )
```

### 2. 组件组合

通过组合组件实现复杂的 UI：

```python
def Layout(props):
    return div(
        Header(props.get('header', {})),
        main(props.get('children', [])),
        Footer()
    ).class_name('layout')

def App():
    return Layout({
        'header': {
            'title': '我的应用',
            'nav_items': [
                {'text': '首页', 'url': '/'},
                {'text': '关于', 'url': '/about'}
            ]
        },
        'children': [
            h1('欢迎'),
            p('这是主页内容')
        ]
    })
```

## 条件渲染

根据条件渲染不同的内容：

```python
def UserGreeting(props):
    user = props.get('user')
    is_admin = props.get('is_admin', False)

    if not user:
        return div(
            p('请登录')
        ).class_name('guest-message')

    return div(
        h2(f'欢迎，{user["name"]}！'),
        p('管理员控制面板') if is_admin else p('用户面板')
    ).class_name('user-message')
```

## 列表渲染

渲染列表数据：

```python
def TodoList(props):
    todos = props.get('todos', [])

    if not todos:
        return div(p('暂无待办事项')).class_name('empty-list')

    return div(
        h2('待办事项'),
        ul(
            *[TodoItem(todo) for todo in todos]
        )
    ).class_name('todo-list')

def TodoItem(props):
    return li(
        input().type('checkbox').checked(props.get('completed', False)),
        span(props.get('text', '')).class_name(
            'completed' if props.get('completed', False) else ''
        )
    ).class_name('todo-item')
```

## 组件库示例

下面是一个简单的组件库示例：

### 按钮组件

```python
from pure.html import button
from pure.clx import clx

def Button(props):
    # 提取 props
    text = props.get('text', '')
    variant = props.get('variant', 'primary')
    size = props.get('size', 'medium')
    disabled = props.get('disabled', False)
    full_width = props.get('fullWidth', False)

    # 构建类名
    classes = clx(
        'btn',
        f'btn-{variant}',
        f'btn-{size}',
        {'btn-disabled': disabled, 'btn-full': full_width}
    )

    # 返回按钮元素
    return button(text) \
        .class_name(classes) \
        .disabled(disabled) \
        .type(props.get('type', 'button')) \
        .onclick(props.get('onClick', ''))
```

### 卡片组件

```python
from pure.html import div, h2, p, img

def Card(props):
    # 提取 props
    title = props.get('title', '')
    content = props.get('content', '')
    image_url = props.get('image', '')

    # 构建卡片内容
    card_content = []

    if image_url:
        card_content.append(
            img().src(image_url).alt(title).class_name('card-image')
        )

    card_content.extend([
        h2(title).class_name('card-title'),
        p(content).class_name('card-content')
    ])

    # 添加操作按钮
    actions = props.get('actions', [])
    if actions:
        action_buttons = div(
            *[Button(action) for action in actions]
        ).class_name('card-actions')
        card_content.append(action_buttons)

    # 返回卡片元素
    return div(
        *card_content
    ).class_name('card')
```

### 表单组件

```python
from pure.html import form, div, label, input, textarea, button

def TextField(props):
    id = props.get('id', '')
    label_text = props.get('label', '')

    return div(
        label(label_text).for_(id) if label_text else None,
        input() \
            .type(props.get('type', 'text')) \
            .id(id) \
            .name(props.get('name', id)) \
            .placeholder(props.get('placeholder', '')) \
            .value(props.get('value', '')) \
            .required(props.get('required', False))
    ).class_name('form-field')

def Form(props):
    fields = props.get('fields', [])
    submit_text = props.get('submitText', '提交')

    return form(
        *[TextField(field) for field in fields],
        button(submit_text).type('submit').class_name('btn btn-primary')
    ) \
    .action(props.get('action', '')) \
    .method(props.get('method', 'post')) \
    .class_name('form')
```

## 最佳实践

### 1. 保持组件简单

每个组件应该只做一件事，并且做好。如果一个组件变得复杂，考虑将其拆分成更小的组件。

### 2. 使用有意义的命名

为组件和 props 使用描述性的名称：

```python
# 不好的命名
def C(p):
    return div(p.get('t'))

# 好的命名
def Card(props):
    return div(props.get('title'))
```

### 3. 提供默认值

为 props 提供合理的默认值，使组件更易用：

```python
def Button(props):
    # 提供默认值
    text = props.get('text', '按钮')
    variant = props.get('variant', 'primary')

    return button(text).class_name(f'btn btn-{variant}')
```

### 4. 文档化组件

为组件添加文档字符串，说明其用途和参数：

```python
def Alert(props):
    """
    显示警告消息的组件

    参数:
        type (str): 警告类型，可选值: 'info', 'success', 'warning', 'error'
        message (str): 显示的消息
        dismissible (bool): 是否可关闭
    """
    alert_type = props.get('type', 'info')
    message = props.get('message', '')
    dismissible = props.get('dismissible', False)

    return div(
        message,
        button('×').class_name('close-btn') if dismissible else None
    ).class_name(f'alert alert-{alert_type}')
```

## 组件测试

测试组件以确保其正确工作：

```python
def test_button_component():
    # 测试默认按钮
    default_button = Button({})
    assert 'btn' in default_button.get_attr('class')
    assert 'btn-primary' in default_button.get_attr('class')

    # 测试禁用按钮
    disabled_button = Button({'disabled': True})
    assert disabled_button.get_attr('disabled') == 'disabled'

    # 测试自定义按钮
    custom_button = Button({
        'text': '点击我',
        'variant': 'danger',
        'size': 'large'
    })
    assert custom_button.get_children()[0] == '点击我'
    assert 'btn-danger' in custom_button.get_attr('class')
    assert 'btn-large' in custom_button.get_attr('class')
```

## 下一步

现在你已经了解了如何创建和使用组件，可以继续学习：

- [属性](/zh/guide/props) - 深入了解属性系统
- [TailwindCSS 集成](/zh/guide/tailwindcss) - 学习如何为组件添加样式
- [API 参考](/zh/api/) - 查看完整的 API 文档
