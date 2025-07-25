# TailwindCSS 集成

本指南介绍如何在 Purepy 项目中集成和使用 TailwindCSS。

## 什么是 TailwindCSS？

TailwindCSS 是一个功能优先的 CSS 框架，它提供了大量的实用类，让你可以快速构建现代化的用户界面。

## 安装 TailwindCSS

### 1. 通过 CDN 使用（快速开始）

最简单的方式是通过 CDN 引入 TailwindCSS：

```python
from pure.html import html, head, meta, title, link, body, div, h1, p

def create_page():
    return html(
        head(
            meta().charset('UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1.0'),
            title('Purepy + TailwindCSS'),
            # 引入 TailwindCSS CDN
            link().href('https://cdn.tailwindcss.com').rel('stylesheet')
        ),
        body(
            div(
                h1('欢迎使用 Purepy + TailwindCSS').class_name('text-4xl font-bold text-blue-600 mb-4'),
                p('这是一个使用 TailwindCSS 样式的段落。').class_name('text-gray-700 text-lg')
            ).class_name('container mx-auto p-8')
        )
    )

# 生成页面
page = create_page()
page.to_save('index.html')
```

### 2. 本地安装（推荐用于生产环境）

对于生产环境，建议本地安装 TailwindCSS：

```bash
# 安装 Node.js 和 npm（如果还没有）
npm init -y
npm install -D tailwindcss
npx tailwindcss init
```

配置 `tailwind.config.js`：

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./output/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

创建 CSS 文件 `src/input.css`：

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

构建 CSS：

```bash
npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch
```

## 在 Purepy 中使用 TailwindCSS

### 1. 基本样式

```python
from pure.html import div, h1, p, button

def styled_card(props):
    title = props.get('title', '')
    content = props.get('content', '')

    return div(
        div(
            h1(title).class_name('text-2xl font-bold text-gray-900 mb-4'),
            p(content).class_name('text-gray-600 mb-6'),
            button('了解更多').class_name(
                'bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
            )
        ).class_name('p-6')
    ).class_name('max-w-sm mx-auto bg-white rounded-xl shadow-md overflow-hidden')

# 使用组件
card = styled_card({
    'title': '卡片标题',
    'content': '这是卡片的内容描述。'
})
card.to_print()
```

### 2. 响应式设计

```python
from pure.html import div, h1, p, img

def responsive_hero():
    return div(
        div(
            h1('响应式标题').class_name(
                'text-4xl md:text-6xl font-bold text-white mb-4'
            ),
            p('这是一个响应式的英雄区域').class_name(
                'text-xl md:text-2xl text-gray-200 mb-8'
            ),
            button('开始使用').class_name(
                'bg-white text-blue-600 font-bold py-3 px-6 rounded-lg hover:bg-gray-100 transition duration-300'
            )
        ).class_name('text-center')
    ).class_name(
        'bg-gradient-to-r from-blue-500 to-purple-600 min-h-screen flex items-center justify-center px-4'
    )

hero = responsive_hero()
hero.to_print()
```

### 3. 网格布局

```python
from pure.html import div, h2, p

def grid_layout():
    items = [
        {'title': '特性 1', 'desc': '描述 1'},
        {'title': '特性 2', 'desc': '描述 2'},
        {'title': '特性 3', 'desc': '描述 3'},
        {'title': '特性 4', 'desc': '描述 4'},
    ]

    return div(
        h2('功能特性').class_name('text-3xl font-bold text-center mb-12'),
        div(
            *[
                div(
                    h2(item['title']).class_name('text-xl font-semibold mb-2'),
                    p(item['desc']).class_name('text-gray-600')
                ).class_name('bg-white p-6 rounded-lg shadow-md')
                for item in items
            ]
        ).class_name('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6')
    ).class_name('container mx-auto px-4 py-12')

grid = grid_layout()
grid.to_print()
```

### 4. 表单样式

```python
from pure.html import form, div, label, input, textarea, button

def styled_form():
    return form(
        div(
            label('姓名').for_('name').class_name('block text-sm font-medium text-gray-700 mb-2'),
            input().type('text').id('name').name('name').class_name(
                'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            )
        ).class_name('mb-4'),

        div(
            label('邮箱').for_('email').class_name('block text-sm font-medium text-gray-700 mb-2'),
            input().type('email').id('email').name('email').class_name(
                'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            )
        ).class_name('mb-4'),

        div(
            label('消息').for_('message').class_name('block text-sm font-medium text-gray-700 mb-2'),
            textarea().id('message').name('message').rows('4').class_name(
                'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            )
        ).class_name('mb-6'),

        button('提交').type('submit').class_name(
            'w-full bg-blue-500 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-600 transition duration-300'
        )
    ).class_name('max-w-md mx-auto bg-white p-8 rounded-lg shadow-md')

form_element = styled_form()
form_element.to_print()
```

## 工具函数集成

### 使用 clx 函数管理条件类名

```python
from pure.html import div, button
from pure.clx import clx

def conditional_button(props):
    is_primary = props.get('primary', False)
    is_large = props.get('large', False)
    is_disabled = props.get('disabled', False)
    text = props.get('text', '按钮')

    classes = clx(
        'font-bold py-2 px-4 rounded transition duration-300',
        {
            'bg-blue-500 hover:bg-blue-700 text-white': is_primary,
            'bg-gray-300 hover:bg-gray-400 text-gray-800': not is_primary,
            'py-3 px-6 text-lg': is_large,
            'opacity-50 cursor-not-allowed': is_disabled
        }
    )

    return button(text).class_name(classes).disabled(is_disabled)

# 使用示例
primary_btn = conditional_button({'text': '主要按钮', 'primary': True, 'large': True})
secondary_btn = conditional_button({'text': '次要按钮', 'disabled': True})

div(primary_btn, secondary_btn).class_name('space-x-4').to_print()
```

## 完整示例

以下是一个完整的页面示例，展示了 Purepy 与 TailwindCSS 的集成：

```python
from pure.html import html, head, meta, title, link, body, div, header, nav, a, main, h1, p, button, footer

def create_landing_page():
    return html(
        head(
            meta().charset('UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1.0'),
            title('Purepy + TailwindCSS 示例'),
            link().href('https://cdn.tailwindcss.com').rel('stylesheet')
        ),
        body(
            # 导航栏
            header(
                nav(
                    div(
                        div('Purepy').class_name('text-xl font-bold text-white'),
                        div(
                            a('首页').href('#').class_name('text-white hover:text-gray-300 mx-2'),
                            a('文档').href('#').class_name('text-white hover:text-gray-300 mx-2'),
                            a('关于').href('#').class_name('text-white hover:text-gray-300 mx-2')
                        )
                    ).class_name('flex justify-between items-center')
                ).class_name('container mx-auto px-4 py-4')
            ).class_name('bg-blue-600'),

            # 主要内容
            main(
                div(
                    h1('欢迎使用 Purepy').class_name('text-5xl font-bold text-gray-900 mb-6'),
                    p('一个受 ReactJS 启发的 Python 模板引擎').class_name('text-xl text-gray-600 mb-8'),
                    button('开始使用').class_name(
                        'bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg text-lg'
                    )
                ).class_name('text-center')
            ).class_name('container mx-auto px-4 py-20'),

            # 页脚
            footer(
                p('© 2024 Purepy. All rights reserved.').class_name('text-center text-gray-600')
            ).class_name('bg-gray-100 py-8')
        )
    )

# 生成并保存页面
page = create_landing_page()
page.to_save('landing.html')
print("页面已生成：landing.html")
```

## 最佳实践

1. **使用语义化的组件名称**：创建有意义的组件函数名
2. **提取重复的样式**：将常用的样式组合封装成函数
3. **利用 clx 函数**：管理条件类名，保持代码整洁
4. **响应式优先**：始终考虑移动端体验
5. **性能优化**：在生产环境中使用 PurgeCSS 移除未使用的样式

## 下一步

- [基本用法](/guide/basic-usage) - 学习 Purepy 的基础语法
- [API 参考](/api/) - 查看完整的 API 文档
