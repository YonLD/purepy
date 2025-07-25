# 基本概念

本章将介绍 Purepy 的核心概念，帮助你更好地理解和使用这个模板引擎。

## 元素 (Elements)

在 Purepy 中，每个 HTML 标签都是一个函数，调用这些函数会创建元素对象。

### 创建元素

```python
from pure.html import div, h1, p

# 创建一个 div 元素
container = div()

# 创建带内容的元素
title = h1('页面标题')
content = p('这是段落内容')
```

### 元素的结构

每个元素都有以下组成部分：

- **标签名**: HTML 标签的名称（如 'div', 'h1', 'p'）
- **属性**: 元素的属性（如 class, id, data-* 等）
- **子元素**: 嵌套在元素内部的其他元素或文本

```python
# 元素结构示例
element = div(                    # 标签名: div
    h1('标题'),                   # 子元素: h1
    p('内容')                     # 子元素: p
).class_name('container')         # 属性: class="container"
```

## 属性 (Attributes)

属性用于配置元素的行为和外观。

### 设置属性

```python
from pure.html import div, input

# 使用方法链设置属性
element = div('内容') \
    .class_name('container') \
    .id('main') \
    .data_value('123')

# 表单元素属性
field = input() \
    .type('text') \
    .name('username') \
    .placeholder('请输入用户名') \
    .required(True)
```

### 特殊属性处理

#### class 属性

由于 `class` 是 Python 关键字，使用 `class_name` 方法：

```python
div('内容').class_name('btn btn-primary')
```

#### data 和 aria 属性

使用下划线替代连字符：

```python
div('内容') \
    .data_id('123') \          # data-id="123"
    .data_type('card') \       # data-type="card"
    .aria_label('按钮')        # aria-label="按钮"
```

#### 布尔属性

```python
input() \
    .type('checkbox') \
    .checked(True) \           # checked="checked"
    .disabled(False)           # 不会添加 disabled 属性
```

## 子元素 (Children)

元素可以包含其他元素或文本内容。

### 添加子元素

```python
from pure.html import div, h1, p, ul, li

# 单个子元素
container = div(h1('标题'))

# 多个子元素
container = div(
    h1('标题'),
    p('内容'),
    ul(
        li('项目 1'),
        li('项目 2'),
        li('项目 3')
    )
)
```

### 动态子元素

```python
# 使用列表推导
items = ['苹果', '香蕉', '橙子']
list_element = ul(
    *[li(item) for item in items]
)

# 条件子元素
is_logged_in = True
header = div(
    h1('网站标题'),
    p('欢迎回来！') if is_logged_in else p('请登录')
)
```

## 组件 (Components)

组件是可重用的函数，返回元素结构。

### 基本组件

```python
def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')
    
    return div(
        h1(title).class_name('card-title'),
        p(content).class_name('card-content')
    ).class_name('card')

# 使用组件
my_card = Card({
    'title': '卡片标题',
    'content': '卡片内容'
})
```

### 组件组合

```python
def Header(props):
    return header(
        h1(props.get('title', '')),
        nav(
            *[a(item['text']).href(item['url']) 
              for item in props.get('nav_items', [])]
        )
    ).class_name('header')

def Footer(props):
    return footer(
        p(props.get('copyright', ''))
    ).class_name('footer')

def Layout(props):
    return div(
        Header(props.get('header', {})),
        main(props.get('content', '')),
        Footer(props.get('footer', {}))
    ).class_name('layout')
```

## 属性传递 (Props)

Props 是传递给组件的数据。

### Props 的类型

```python
def Button(props):
    # 字符串属性
    text = props.get('text', '按钮')
    
    # 布尔属性
    is_primary = props.get('primary', False)
    is_disabled = props.get('disabled', False)
    
    # 函数属性（虽然在 HTML 中不常用）
    on_click = props.get('onClick', '')
    
    # 对象属性
    style_props = props.get('style', {})
    
    return button(text) \
        .class_name('btn btn-primary' if is_primary else 'btn') \
        .disabled(is_disabled) \
        .onclick(on_click)
```

### 默认 Props

```python
def Card(props):
    # 设置默认值
    defaults = {
        'title': '默认标题',
        'content': '默认内容',
        'variant': 'default'
    }
    
    # 合并 props 和默认值
    merged_props = {**defaults, **props}
    
    return div(
        h2(merged_props['title']),
        p(merged_props['content'])
    ).class_name(f'card card-{merged_props["variant"]}')
```

## 条件渲染

根据条件显示不同的内容。

### 简单条件

```python
def UserGreeting(props):
    user = props.get('user')
    
    return div(
        h1('欢迎回来！') if user else h1('请登录'),
        p(f'你好，{user.name}！') if user else None
    )
```

### 复杂条件

```python
def StatusMessage(props):
    status = props.get('status', 'loading')
    
    if status == 'loading':
        return div('加载中...').class_name('loading')
    elif status == 'error':
        return div('发生错误').class_name('error')
    elif status == 'success':
        return div('操作成功').class_name('success')
    else:
        return div('未知状态').class_name('unknown')
```

## 列表渲染

渲染动态列表内容。

### 基本列表

```python
def TodoList(props):
    todos = props.get('todos', [])
    
    return ul(
        *[li(todo['text']) for todo in todos]
    ).class_name('todo-list')
```

### 带键的列表

```python
def UserList(props):
    users = props.get('users', [])
    
    return div(
        *[
            div(
                h3(user['name']),
                p(user['email'])
            ).class_name('user-card')
            for user in users
        ]
    ).class_name('user-list')
```

## 样式处理

Purepy 提供了多种处理样式的方式。

### 内联样式

```python
from pure.sty import sty

styles = sty({
    'color': 'red',
    'font-size': '16px',
    'background-color': '#f0f0f0'
})

div('内容').style(styles)
```

### CSS 类

```python
from pure.clx import clx

# 静态类
div('内容').class_name('btn btn-primary')

# 动态类
is_active = True
classes = clx('btn', {'active': is_active, 'disabled': False})
div('内容').class_name(classes)
```

## 事件处理

虽然 Purepy 主要用于生成静态 HTML，但你仍然可以添加事件属性：

```python
def InteractiveButton(props):
    return button(props.get('text', '点击')) \
        .onclick(props.get('onClick', '')) \
        .class_name('interactive-btn')

# 使用
btn = InteractiveButton({
    'text': '点击我',
    'onClick': 'alert("按钮被点击了！")'
})
```

## 生命周期

在 Purepy 中，组件的"生命周期"主要体现在数据处理和渲染过程中：

### 数据准备

```python
def DataCard(props):
    # 1. 数据准备阶段
    raw_data = props.get('data', {})
    
    # 2. 数据处理
    processed_data = {
        'title': raw_data.get('title', '').upper(),
        'content': raw_data.get('content', '')[:100],  # 截取前100字符
        'date': format_date(raw_data.get('date'))
    }
    
    # 3. 渲染阶段
    return div(
        h2(processed_data['title']),
        p(processed_data['content']),
        small(processed_data['date'])
    ).class_name('data-card')
```

## 错误处理

处理可能出现的错误情况：

```python
def SafeCard(props):
    try:
        title = props['title']  # 必需的属性
        content = props.get('content', '')
        
        return div(
            h2(title),
            p(content) if content else p('暂无内容')
        ).class_name('card')
    
    except KeyError:
        return div(
            p('错误：缺少必需的 title 属性')
        ).class_name('error-card')
```

## 性能考虑

### 避免重复计算

```python
def ExpensiveComponent(props):
    # 缓存计算结果
    if not hasattr(ExpensiveComponent, '_cache'):
        ExpensiveComponent._cache = {}
    
    cache_key = str(props)
    if cache_key in ExpensiveComponent._cache:
        return ExpensiveComponent._cache[cache_key]
    
    # 执行昂贵的计算
    result = div(
        # ... 复杂的渲染逻辑
    )
    
    ExpensiveComponent._cache[cache_key] = result
    return result
```

## 下一步

现在你已经了解了 Purepy 的基本概念，可以继续学习：

- [基本用法](/guide/basic-usage) - 详细的语法说明
- [组件](/guide/components) - 深入学习组件开发
- [属性](/guide/props) - 掌握属性系统
