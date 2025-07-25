# 快速开始

本指南将帮助你快速上手 Purepy，创建你的第一个应用。

## 安装

首先安装 Purepy：

```bash
pip install purepy
```

## 创建第一个应用

### 1. 创建项目目录

```bash
mkdir my-purepy-app
cd my-purepy-app
```

### 2. 创建入口文件

创建 `app.py` 文件：

```python
from pure.html import html, head, meta, title, body, div, h1, p, a

def App():
    return html(
        head(
            meta().charset('UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1.0'),
            title('我的第一个 Purepy 应用')
        ),
        body(
            div(
                h1('欢迎使用 Purepy'),
                p('这是你的第一个 Purepy 应用！'),
                a('了解更多').href('https://github.com/YonLD/purepy')
            ).class_name('container')
        )
    )

if __name__ == '__main__':
    app = App()
    print(app)
```

### 3. 运行应用

```bash
python app.py
```

你将看到生成的 HTML 输出。

## 添加样式

让我们为应用添加一些样式。修改 `app.py`：

```python
from pure.html import html, head, meta, title, style, body, div, h1, p, a

def App():
    return html(
        head(
            meta().charset('UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1.0'),
            title('我的第一个 Purepy 应用'),
            style("""
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    line-height: 1.6;
                }
                a {
                    color: #007bff;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            """)
        ),
        body(
            div(
                h1('欢迎使用 Purepy'),
                p('这是你的第一个 Purepy 应用！Purepy 让你可以使用纯 Python 代码来构建 HTML 内容。'),
                p(
                    '想了解更多？访问 ',
                    a('GitHub 仓库').href('https://github.com/YonLD/purepy'),
                    ' 获取更多信息。'
                )
            ).class_name('container')
        )
    )

if __name__ == '__main__':
    app = App()
    print(app)
```

## 创建组件

Purepy 的强大之处在于组件化开发。让我们创建一些可重用的组件：

```python
from pure.html import html, head, meta, title, style, body, div, h1, h2, p, a, ul, li

def Header(props):
    title = props.get('title', 'Purepy App')
    return div(
        h1(title)
    ).class_name('header')

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')
    link = props.get('link', '#')
    
    return div(
        h2(title),
        p(content),
        a('了解更多').href(link)
    ).class_name('card')

def Footer():
    return div(
        p('© 2024 Purepy 应用')
    ).class_name('footer')

def App():
    cards_data = [
        {
            'title': '简单易用',
            'content': 'Purepy 提供简洁的 API，让你快速上手。',
            'link': '/guide/basic-usage'
        },
        {
            'title': '组件化',
            'content': '通过组件化开发，让代码更易维护和复用。',
            'link': '/guide/components'
        },
        {
            'title': '类型安全',
            'content': '完整的类型提示支持，提供更好的开发体验。',
            'link': '/guide/concepts'
        }
    ]
    
    return html(
        head(
            meta().charset('UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1.0'),
            title('我的第一个 Purepy 应用'),
            style("""
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { text-align: center; margin-bottom: 30px; }
                .header h1 { color: #333; }
                .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                .card h2 { margin-top: 0; color: #333; }
                .card p { color: #666; line-height: 1.6; }
                .card a { color: #007bff; text-decoration: none; }
                .footer { text-align: center; margin-top: 40px; color: #666; }
            """)
        ),
        body(
            div(
                Header({'title': '欢迎使用 Purepy'}),
                div(
                    *[Card(card) for card in cards_data]
                ).class_name('cards'),
                Footer()
            ).class_name('container')
        )
    )

if __name__ == '__main__':
    app = App()
    print(app)
```

## 保存为 HTML 文件

你也可以将生成的 HTML 保存为文件：

```python
def save_to_file():
    app = App()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(app))
    print('HTML 文件已保存为 index.html')

if __name__ == '__main__':
    save_to_file()
```

## 下一步

恭喜！你已经创建了第一个 Purepy 应用。接下来你可以：

- [学习基本概念](/guide/concepts) - 深入理解 Purepy 的工作原理
- [探索组件开发](/guide/components) - 学习如何创建复杂的组件
- [查看 API 文档](/api/) - 了解所有可用的标签和方法
- [集成到 Web 框架](/guide/flask) - 在 Flask 或 Django 中使用 Purepy
