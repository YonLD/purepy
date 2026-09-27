# 属性

属性（Props）是组件的输入，用于配置组件的行为和外观。本指南将详细介绍如何在 Purepy 中使用属性。

## 什么是属性？

属性是传递给组件的数据，通常是一个字典。组件通过属性接收外部数据，并根据这些数据渲染相应的内容。

## 基本属性使用

### 传递属性

```python
from pure.html import div, h1, p

def Greeting(props):
    name = props.get('name', '访客')
    message = props.get('message', '欢迎！')
    
    return div(
        h1(f'你好，{name}！'),
        p(message)
    ).class_name('greeting')

# 使用组件并传递属性
greeting = Greeting({
    'name': '张三',
    'message': '欢迎来到我们的网站！'
})
```

### 属性类型

属性可以是任何 Python 数据类型：

```python
def UserCard(props):
    # 字符串属性
    name = props.get('name', '')
    
    # 数字属性
    age = props.get('age', 0)
    
    # 布尔属性
    is_premium = props.get('isPremium', False)
    
    # 列表属性
    hobbies = props.get('hobbies', [])
    
    # 字典属性
    address = props.get('address', {})
    
    return div(
        h2(name),
        p(f'年龄：{age}'),
        p('高级用户' if is_premium else '普通用户'),
        div(
            h3('爱好：'),
            ul(*[li(hobby) for hobby in hobbies])
        ) if hobbies else None,
        div(
            h3('地址：'),
            p(f"{address.get('city', '')} {address.get('street', '')}")
        ) if address else None
    ).class_name('user-card')
```

## 默认属性

为属性提供默认值，使组件更加健壮：

```python
def Button(props):
    # 使用 get() 方法提供默认值
    text = props.get('text', '按钮')
    variant = props.get('variant', 'primary')
    size = props.get('size', 'medium')
    disabled = props.get('disabled', False)
    
    return button(text) \
        .class_name(f'btn btn-{variant} btn-{size}') \
        .disabled(disabled)

# 也可以使用字典合并的方式
def Card(props):
    defaults = {
        'title': '默认标题',
        'content': '默认内容',
        'variant': 'default',
        'shadow': True
    }
    
    # 合并默认值和传入的属性
    merged_props = {**defaults, **props}
    
    return div(
        h2(merged_props['title']),
        p(merged_props['content'])
    ).class_name(f"card card-{merged_props['variant']}" + 
                 (' card-shadow' if merged_props['shadow'] else ''))
```

## 属性验证

虽然 Python 是动态类型语言，但我们可以添加属性验证来提高代码质量：

```python
def validateProps(props, required=None, types=None):
    """简单的属性验证函数"""
    required = required or []
    types = types or {}
    
    # 检查必需属性
    for prop in required:
        if prop not in props:
            raise ValueError(f"缺少必需属性: {prop}")
    
    # 检查属性类型
    for prop, expected_type in types.items():
        if prop in props and not isinstance(props[prop], expected_type):
            raise TypeError(f"属性 {prop} 应该是 {expected_type.__name__} 类型")

def SafeButton(props):
    # 验证属性
    validateProps(props, 
                  required=['text'],
                  types={'text': str, 'disabled': bool})
    
    return button(props['text']) \
        .class_name('btn') \
        .disabled(props.get('disabled', False))
```

## 属性传递模式

### 1. 属性透传

将属性传递给子组件：

```python
def Card(props):
    # 提取卡片特有的属性
    title = props.get('title', '')
    content = props.get('content', '')
    
    # 将按钮相关属性传递给 Button 组件
    button_props = {
        'text': props.get('buttonText', '了解更多'),
        'variant': props.get('buttonVariant', 'primary'),
        'disabled': props.get('buttonDisabled', False)
    }
    
    return div(
        h2(title),
        p(content),
        Button(button_props)
    ).class_name('card')
```

### 2. 属性解构

从属性中提取特定的值：

```python
def UserProfile(props):
    user = props.get('user', {})
    
    # 解构用户对象
    name = user.get('name', '')
    email = user.get('email', '')
    avatar = user.get('avatar', '')
    bio = user.get('bio', '')
    
    return div(
        div(
            img().src(avatar).alt(name) if avatar else None,
            h2(name),
            p(email)
        ).class_name('user-header'),
        div(
            p(bio)
        ).class_name('user-bio') if bio else None
    ).class_name('user-profile')
```

### 3. 属性分组

将相关属性分组传递：

```python
def Form(props):
    # 表单配置
    form_config = props.get('config', {})
    
    # 字段定义
    fields = props.get('fields', [])
    
    # 提交配置
    submit_config = props.get('submit', {})
    
    return form(
        *[FormField(field) for field in fields],
        button(submit_config.get('text', '提交')) \
            .type('submit') \
            .class_name(submit_config.get('className', 'btn btn-primary'))
    ) \
    .action(form_config.get('action', '')) \
    .method(form_config.get('method', 'post')) \
    .class_name(form_config.get('className', 'form'))
```

## 条件属性

根据条件设置不同的属性：

```python
def Alert(props):
    alert_type = props.get('type', 'info')
    message = props.get('message', '')
    dismissible = props.get('dismissible', False)
    
    # 根据类型设置不同的图标
    icons = {
        'info': 'ℹ️',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    }
    
    icon = icons.get(alert_type, icons['info'])
    
    return div(
        span(icon).class_name('alert-icon'),
        span(message).class_name('alert-message'),
        button('×').class_name('alert-close') if dismissible else None
    ).class_name(f'alert alert-{alert_type}')
```

## 函数属性

虽然在生成静态 HTML 时不常用，但可以传递函数作为属性：

```python
def DataTable(props):
    data = props.get('data', [])
    columns = props.get('columns', [])
    row_renderer = props.get('rowRenderer', None)
    
    def default_row_renderer(row, index):
        return tr(
            *[td(str(row.get(col['key'], ''))) for col in columns]
        )
    
    renderer = row_renderer or default_row_renderer
    
    return table(
        thead(
            tr(*[th(col['title']) for col in columns])
        ),
        tbody(
            *[renderer(row, i) for i, row in enumerate(data)]
        )
    ).class_name('data-table')

# 使用自定义渲染器
def custom_row_renderer(row, index):
    return tr(
        td(row.get('name', '')),
        td(row.get('email', '')),
        td(
            button('编辑').class_name('btn btn-sm'),
            button('删除').class_name('btn btn-sm btn-danger')
        )
    ).class_name('table-row')

table = DataTable({
    'data': users,
    'columns': [
        {'key': 'name', 'title': '姓名'},
        {'key': 'email', 'title': '邮箱'},
        {'key': 'actions', 'title': '操作'}
    ],
    'rowRenderer': custom_row_renderer
})
```

## 属性最佳实践

### 1. 使用描述性的属性名

```python
# 不好的命名
def Card(props):
    t = props.get('t')  # 不清楚 t 是什么
    c = props.get('c')  # 不清楚 c 是什么
    
# 好的命名
def Card(props):
    title = props.get('title')
    content = props.get('content')
```

### 2. 保持属性结构简单

```python
# 避免过度嵌套
# 不好的做法
props = {
    'user': {
        'profile': {
            'personal': {
                'name': {
                    'first': 'John',
                    'last': 'Doe'
                }
            }
        }
    }
}

# 好的做法
props = {
    'firstName': 'John',
    'lastName': 'Doe',
    'email': 'john@example.com'
}
```

### 3. 使用类型提示

```python
from typing import Dict, Any, List, Optional

def UserList(props: Dict[str, Any]) -> 'HTML':
    users: List[Dict[str, Any]] = props.get('users', [])
    title: str = props.get('title', '用户列表')
    show_email: bool = props.get('showEmail', True)
    
    return div(
        h2(title),
        ul(
            *[UserItem({
                'user': user,
                'showEmail': show_email
            }) for user in users]
        )
    ).class_name('user-list')
```

### 4. 文档化属性

```python
def Button(props):
    """
    按钮组件
    
    属性:
        text (str): 按钮文本，默认为 '按钮'
        variant (str): 按钮样式，可选值: 'primary', 'secondary', 'danger'
        size (str): 按钮大小，可选值: 'small', 'medium', 'large'
        disabled (bool): 是否禁用，默认为 False
        fullWidth (bool): 是否全宽，默认为 False
        onClick (str): 点击事件处理器
    """
    # 组件实现...
```

## 属性模式示例

### 配置对象模式

```python
def Chart(props):
    config = props.get('config', {})
    data = props.get('data', [])
    
    # 从配置中提取设置
    chart_type = config.get('type', 'bar')
    width = config.get('width', 400)
    height = config.get('height', 300)
    colors = config.get('colors', ['#blue', '#red', '#green'])
    
    return div(
        # 图表实现...
    ).class_name(f'chart chart-{chart_type}') \
     .style(f'width: {width}px; height: {height}px;')
```

### 渲染属性模式

```python
def List(props):
    items = props.get('items', [])
    render_item = props.get('renderItem', None)
    
    def default_render(item, index):
        return li(str(item))
    
    renderer = render_item or default_render
    
    return ul(
        *[renderer(item, i) for i, item in enumerate(items)]
    ).class_name('list')
```

## Slot 速查

**Slot** 是模板里留给数据的占位符，渲染时才绑定。属性说明的是*组件接受什么*，
slot 说明的是*数据落在哪里*。

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div, p

# 值 slot：会转义，和其他文本位置一样。
print(Compile.shape(p(Slot.value('body')))({'body': '<x>'}))
# <p>&lt;x&gt;</p>

# raw slot：原样输出。
from pure.core.Raw import Raw

print(Compile.shape(p(Slot.raw('body')))({'body': Raw.of('<x>')}))
# <p><x></p>
```

### 五种 slot

| 助手 | 绑定 | 说明 |
| --- | --- | --- |
| `Slot.value(name)` | 一个标量 | 会转义；在属性位置同样有效 |
| `Slot.raw(name)` | 标记，或任意可迭代对象 | 绝不转义 |
| `Slot.child(name, shape)` | 一个字典 | 相对 `shape` 解析 |
| `Slot.each(name, shape)` | 一个列表 | 每个元素跑一次 `shape` |
| `Slot.if_(name, then)` | 一个布尔值 | 第二个参数 `otherwise` 可选 |

`if` 是 Python 关键字，所以助手叫 `Slot.if_()`。

### 作用域

`Slot.child()` 与 `Slot.each()` 会开启一层嵌套数据作用域。在其内部，slot 名相对
嵌套对象解析，而不是顶层数据——而 slot 路径会记录这一点，因此报错能指出确切位置。

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div, span

item = Compile.shape(span(Slot.value('label')))
list_shape = Compile.shape(div(Slot.each('items', item)))

# 列表 slot 接收由 item shape 自身 slot 组成的列表。
print(Compile.shape(div(Slot.each('rows', item)))({'rows': [{'label': 'a'}]}))
# <div><span>a</span></div>

# child slot 接收一个对象。
print(Compile.shape(div(Slot.child('meta', list_shape)))({'meta': {'items': [{'label': 'm'}]}}))
# <div><div><span>m</span></div></div>
```

::: warning 字符串不是列表
`Slot.each()` 会刻意拒绝 `str`。Python 的字符串是可迭代的，放行它会把一个笔误
变成逐字符渲染。请包成列表；如果本意就是拼接字符，那用 `Slot.raw()`。
:::

### 分支

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div, span

shape = Compile.shape(div(Slot.if_('on', span('yes'), span('no'))))

print(shape({'on': True}))    # <div><span>yes</span></div>
print(shape({'on': False}))   # <div><span>no</span></div>

# 没有 else 分支时，假值不渲染任何东西。
print(Compile.shape(div(Slot.if_('on', span('yes'))))({}))
# <div></div>
```

两个分支共享当前作用域，因此两边的 slot 读法一致。

### 可选数据

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div

# 键缺失时省略。
print(Compile.shape(div(Slot.value('note').required(False)))({}))
# <div></div>

# 回落到一个值。
print(Compile.shape(div(Slot.value('note').default('(none)')))({}))
# <div>(none)</div>
```

### 缺失数据

必填 slot 没有可绑定的值时会抛出 `MissingSlotException`。在顶层，消息会给出你
实际提供过的最接近的键；在嵌套作用域里没有「最接近的键」可言，于是改为列出该
作用域提供了什么。

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import h1

Compile.shape(h1(Slot.value('title')))({'titel': 'Users'})
# MissingSlotException: slot 'title' is required but was not provided;
#   did you mean 'titel'?
```

### 属性位置的 slot

属性位置的 `Slot` 只能是 `Slot.value()`：其他种类会静默丢掉 shape，因此会被以与
编译渲染器相同的方式拒绝。

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import a

print(Compile.shape(a('x').href(Slot.value('url')))({'url': '/target'}))
# <a href="/target">x</a>
```

### slot 不能出现在哪里

`Slot` 不是标记，因此仍含 slot 的裸标签树本身无法渲染——`Tag.render()` 不接受
数据。请先用 `Compile.shape()` 包起来。而渲染好的子组件完全无法烘焙进树里；它
通过 `Slot.raw()` 进入。

## 下一步

现在你已经掌握了属性的使用方法，可以继续学习：

- [TailwindCSS 集成](/zh/guide/tailwindcss) - 学习如何为组件添加样式
- [API 参考](/zh/api/) - 查看完整的 API 文档
- [基本用法](/zh/guide/basic-usage) - 回顾基础语法
