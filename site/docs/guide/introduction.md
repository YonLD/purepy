# 简介

欢迎使用 Purepy！这是一个受 ReactJS 启发的 Python 模板引擎，让你能够以函数式的方式创建 HTML、SVG 和 XML 内容。

## 什么是 Purepy？

Purepy 是一个现代化的 Python 模板引擎，它借鉴了 ReactJS 的组件化思想，让你能够：

- **函数式编程**：每个 HTML 标签都是一个函数
- **组件化开发**：将 UI 拆分成可重用的组件
- **类型安全**：完整的类型提示支持
- **链式调用**：流畅的 API 设计
- **工具函数**：内置样式和类名处理工具

## 核心特性

### 1. 直观的语法

```python
from pure.html import div, h1, p

# 创建 HTML 结构就像调用函数一样简单
content = div(
    h1('欢迎使用 Purepy'),
    p('这是一个现代化的 Python 模板引擎')
).class_name('welcome')
```

### 2. 组件化思维

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

### 3. 强大的工具函数

```python
from pure.clx import clx
from pure.sty import sty

# 条件类名
classes = clx('btn', {'active': is_active, 'disabled': is_disabled})

# 样式对象
styles = sty({
    'color': 'red',
    'font-size': '16px',
    'padding': '10px'
})
```

## 设计理念

### 函数式优先

Purepy 采用函数式编程范式，每个 HTML 标签都是一个纯函数，这带来了以下好处：

- **可预测性**：相同的输入总是产生相同的输出
- **可测试性**：函数易于单元测试
- **可组合性**：小函数可以组合成复杂的结构
- **可重用性**：组件可以在不同地方重复使用

### 声明式语法

与传统的模板引擎不同，Purepy 使用声明式语法：

```python
# 声明式：描述你想要什么
div(
    h1('标题'),
    p('内容')
).class_name('container')

# 而不是命令式：描述如何做
# template = "<div class='container'><h1>标题</h1><p>内容</p></div>"
```

### 类型安全

Purepy 提供完整的类型提示支持：

```python
from typing import Dict, Any
from pure.html import div, h1, p

def Card(props: Dict[str, Any]) -> 'HTML':
    title: str = props.get('title', '')
    content: str = props.get('content', '')
    
    return div(
        h1(title),
        p(content)
    ).class_name('card')
```

## 与其他模板引擎的对比

### vs Jinja2

```python
# Jinja2
template = """
<div class="card">
    <h1>{{ title }}</h1>
    <p>{{ content }}</p>
</div>
"""

# Purepy
def Card(props):
    return div(
        h1(props['title']),
        p(props['content'])
    ).class_name('card')
```

**Purepy 的优势：**
- 完整的 Python 语法支持
- 更好的 IDE 支持（自动完成、重构等）
- 类型检查
- 更容易调试

### vs Django Templates

```html
<!-- Django Template -->
<div class="card">
    <h1>{{ title }}</h1>
    <p>{{ content }}</p>
    {% if user.is_authenticated %}
        <button>编辑</button>
    {% endif %}
</div>
```

```python
# Purepy
def Card(props):
    user = props.get('user')
    
    return div(
        h1(props['title']),
        p(props['content']),
        button('编辑') if user and user.is_authenticated else None
    ).class_name('card')
```

**Purepy 的优势：**
- 使用标准 Python 语法
- 更强的逻辑表达能力
- 更好的代码重用

## 适用场景

Purepy 特别适合以下场景：

### 1. 静态站点生成

```python
from pure.html import html, head, title, body, div, h1, p

def generate_blog_post(post):
    return html(
        head(title(post['title'])),
        body(
            div(
                h1(post['title']),
                p(post['content'])
            ).class_name('post')
        )
    )

# 生成多个页面
for post in posts:
    page = generate_blog_post(post)
    page.to_save(f'posts/{post["slug"]}.html')
```

### 2. 邮件模板

```python
def email_template(user, content):
    return html(
        head(title('邮件通知')),
        body(
            div(
                h1(f'你好，{user.name}！'),
                div(content),
                p('感谢使用我们的服务')
            ).class_name('email-container')
        )
    )
```

### 3. 报告生成

```python
def generate_report(data):
    return html(
        head(title('数据报告')),
        body(
            div(
                h1('月度报告'),
                *[
                    div(
                        h2(item['title']),
                        p(f'数值：{item["value"]}')
                    ).class_name('report-item')
                    for item in data
                ]
            ).class_name('report')
        )
    )
```

### 4. 组件库开发

```python
# 创建可重用的 UI 组件库
def Button(props):
    variant = props.get('variant', 'primary')
    size = props.get('size', 'medium')
    
    classes = clx('btn', f'btn-{variant}', f'btn-{size}')
    
    return button(props.get('children', '')).class_name(classes)

def Modal(props):
    return div(
        div(
            h2(props.get('title', '')),
            div(props.get('children', '')),
            Button({'children': '关闭', 'variant': 'secondary'})
        ).class_name('modal-content')
    ).class_name('modal')
```

## 学习路径

建议按以下顺序学习 Purepy：

1. **[安装](/guide/installation)** - 设置开发环境
2. **[快速开始](/guide/getting-started)** - 创建第一个应用
3. **[基本概念](/guide/concepts)** - 理解核心概念
4. **[基本用法](/guide/basic-usage)** - 掌握基础语法
5. **[组件](/guide/components)** - 学习组件化开发
6. **[属性](/guide/props)** - 理解属性系统
7. **[TailwindCSS 集成](/guide/tailwindcss)** - 样式处理

## 社区和支持

- **GitHub**: [https://github.com/YonLD/purepy](https://github.com/YonLD/purepy)
- **文档**: 你正在阅读的这份文档
- **问题反馈**: 通过 GitHub Issues 报告问题

## 下一步

现在你已经了解了 Purepy 的基本概念，可以开始：

- [安装 Purepy](/guide/installation)
- [快速开始教程](/guide/getting-started)
- [查看 API 文档](/api/)

让我们开始构建令人惊叹的应用吧！
