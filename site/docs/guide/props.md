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

## 下一步

现在你已经掌握了属性的使用方法，可以继续学习：

- [TailwindCSS 集成](/guide/tailwindcss) - 学习如何为组件添加样式
- [API 参考](/api/) - 查看完整的 API 文档
- [基本用法](/guide/basic-usage) - 回顾基础语法
