# Flask 集成

Purepy 可以很好地与 Flask 框架集成，提供组件化的模板渲染能力。

## 为什么选择这个组合？

- **Purepy**: 提供组件化的 Python 模板渲染
- **Flask**: 提供轻量级的 Web 框架
- **完美互补**: Purepy 处理视图层，Flask 处理路由和业务逻辑

## 快速开始

### 1. 安装依赖

```bash
pip install flask yonld-purepy
```

### 2. 基本集成

```python
from flask import Flask
from pure.html import html, head, title, body, div, h1, p, a

app = Flask(__name__)

def Layout(props):
    page_title = props.get('title', 'Purepy + Flask')
    content = props.get('content', '')
    
    return html(
        head(
            title(page_title)
        ),
        body(
            div(
                content
            ).class_name('container')
        )
    )

@app.route('/')
def index():
    content = div(
        h1('欢迎使用 Purepy + Flask'),
        p('这是一个使用 Purepy 和 Flask 构建的应用'),
        a('了解更多').href('/about')
    )
    
    page = Layout({
        'title': '首页',
        'content': content
    })
    
    return str(page)

@app.route('/about')
def about():
    content = div(
        h1('关于我们'),
        p('Purepy 是一个受 ReactJS 启发的 Python 模板引擎。')
    )
    
    page = Layout({
        'title': '关于我们',
        'content': content
    })
    
    return str(page)

if __name__ == '__main__':
    app.run(debug=True)
```

### 3. 组件化开发

```python
from flask import Flask, request, jsonify
from pure.html import html, head, title, body, div, h1, h2, p, form, input, button, ul, li

app = Flask(__name__)

# 布局组件
def Layout(props):
    page_title = props.get('title', 'Purepy App')
    content = props.get('content', '')
    
    return html(
        head(
            title(page_title),
            # 添加样式
            style("""
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                .container { max-width: 800px; margin: 0 auto; }
                .card { background: #f5f5f5; padding: 20px; margin: 10px 0; border-radius: 8px; }
                .form-group { margin: 10px 0; }
                .form-group input { width: 100%; padding: 8px; }
                .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            """)
        ),
        body(
            div(
                content
            ).class_name('container')
        )
    )

# 卡片组件
def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')
    
    return div(
        h2(title),
        p(content)
    ).class_name('card')

# 表单组件
def ContactForm():
    return form(
        div(
            input().type('text').name('name').placeholder('姓名').required()
        ).class_name('form-group'),
        div(
            input().type('email').name('email').placeholder('邮箱').required()
        ).class_name('form-group'),
        div(
            input().type('text').name('message').placeholder('消息').required()
        ).class_name('form-group'),
        button('提交').type('submit').class_name('btn')
    ).method('POST').action('/contact')

# 路由
@app.route('/')
def index():
    content = div(
        h1('欢迎使用 Purepy + Flask'),
        Card({
            'title': '组件化开发',
            'content': '使用 Purepy 创建可重用的组件，让代码更易维护。'
        }),
        Card({
            'title': 'Flask 集成',
            'content': 'Purepy 与 Flask 完美集成，提供强大的模板渲染能力。'
        })
    )
    
    return str(Layout({
        'title': '首页',
        'content': content
    }))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # 处理表单提交
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # 这里可以保存到数据库或发送邮件
        
        content = div(
            h1('联系我们'),
            p(f'谢谢 {name}，我们已收到您的消息！')
        )
    else:
        content = div(
            h1('联系我们'),
            ContactForm()
        )
    
    return str(Layout({
        'title': '联系我们',
        'content': content
    }))

if __name__ == '__main__':
    app.run(debug=True)
```

## 高级用法

### 1. 模板继承

```python
# templates.py
from pure.html import html, head, title, meta, body, div, nav, ul, li, a, footer, p

def BaseTemplate(props):
    page_title = props.get('title', 'Purepy App')
    content = props.get('content', '')
    nav_items = props.get('nav_items', [])
    
    return html(
        head(
            meta().charset('UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1.0'),
            title(page_title)
        ),
        body(
            nav(
                ul(
                    *[li(a(item['text']).href(item['url'])) for item in nav_items]
                )
            ).class_name('navbar'),
            div(
                content
            ).class_name('main-content'),
            footer(
                p('© 2024 Purepy App')
            ).class_name('footer')
        )
    )

# app.py
from templates import BaseTemplate

@app.route('/')
def index():
    nav_items = [
        {'text': '首页', 'url': '/'},
        {'text': '关于', 'url': '/about'},
        {'text': '联系', 'url': '/contact'}
    ]
    
    content = div(
        h1('首页内容')
    )
    
    return str(BaseTemplate({
        'title': '首页',
        'content': content,
        'nav_items': nav_items
    }))
```

### 2. 数据绑定

```python
from flask import Flask, render_template_string
from pure.html import div, h1, ul, li, p

app = Flask(__name__)

def UserList(users):
    return div(
        h1('用户列表'),
        ul(
            *[li(
                p(f'姓名: {user["name"]}'),
                p(f'邮箱: {user["email"]}')
            ) for user in users]
        )
    )

@app.route('/users')
def users():
    # 模拟从数据库获取用户数据
    users_data = [
        {'name': '张三', 'email': 'zhangsan@example.com'},
        {'name': '李四', 'email': 'lisi@example.com'},
        {'name': '王五', 'email': 'wangwu@example.com'}
    ]
    
    content = UserList(users_data)
    
    return str(Layout({
        'title': '用户列表',
        'content': content
    }))
```

### 3. API 响应

```python
from flask import jsonify

@app.route('/api/component')
def api_component():
    # 返回组件的 HTML 字符串，用于 AJAX 更新
    component = Card({
        'title': '动态内容',
        'content': '这是通过 API 加载的内容'
    })
    
    return jsonify({
        'html': str(component),
        'status': 'success'
    })
```

## 最佳实践

### 1. 组件组织

```python
# components/
#   __init__.py
#   layout.py
#   forms.py
#   cards.py

# components/layout.py
from pure.html import html, head, title, body, div

def Layout(props):
    # 布局组件实现
    pass

# components/forms.py
from pure.html import form, input, button

def ContactForm(props):
    # 表单组件实现
    pass

# app.py
from components.layout import Layout
from components.forms import ContactForm
```

### 2. 错误处理

```python
@app.errorhandler(404)
def not_found(error):
    content = div(
        h1('页面未找到'),
        p('抱歉，您访问的页面不存在。'),
        a('返回首页').href('/')
    )
    
    return str(Layout({
        'title': '404 - 页面未找到',
        'content': content
    })), 404
```

### 3. 性能优化

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_component(data_hash):
    # 缓存静态组件
    return str(SomeComponent(data))
```

## 下一步

- [Django 集成](/guide/django) - 了解如何与 Django 配合使用
- [组件](/guide/components) - 深入学习组件开发
- [API 文档](/api/) - 查看完整的 API 参考
