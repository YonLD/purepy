# 什么是 Purepy?

Purepy 是一个 Python 模板引擎，受 ReactJS 函数式组件的启发。它使用 Python 对象来表示 HTML 元素，提供了一种声明式的方式来构建用户界面，使代码更加简洁、可维护和可重用。

## 特性

### 1. 声明式渲染

使用 Purepy，你可以用声明式的方式描述你的 UI：

```python
from pure.html import div, h1, p

div(
    h1('欢迎使用 Purepy'),
    p('这是一个 Python 模板引擎')
).class_name('container').print()
```

### 2. 组件化开发

将 UI 拆分为独立、可重用的 Python 函数：

```python
from pure.html import div, h2, p

def Card(props):
    title = props.get('title', '')
    content = props.get('content', '')

    return div(
        h2(title),
        p(content)
    ).class_name('card')

# 使用组件
div(
    Card({
        'title': '标题 1',
        'content': '内容 1'
    }),
    Card({
        'title': '标题 2',
        'content': '内容 2'
    })
).class_name('card-grid').print()
```

### 3. XML 支持

Purepy 提供了强大的 XML 处理能力，让您可以轻松地生成和处理 XML 文档：

```python
from pure.core.XML import XML

# 创建 XML 元素
xml = XML.customers(
    XML.customer(
        XML.name('Charter Group'),
        XML.address(
            XML.street('100 Main'),
            XML.city('Framingham'),
            XML.state('MA'),
            XML.zip('01701')
        )
    ).id('55000')
)

# 保存到文件
xml.toSave('./example.xml')
```

### 4. SVG 支持

内置完整的 SVG 标签支持：

```python
from pure.svg import svg, circle, rect

svg(
    rect()
        .x(10)
        .y(10)
        .width(80)
        .height(80)
        .fill('none')
        .stroke('blue')
        .stroke_width(2),
    circle()
        .cx(50)
        .cy(50)
        .r(30)
        .fill('red')
).width(100).height(100).print()
```

## 为什么选择 Purepy?

### 1. 简单易用

Purepy 的 API 设计简单直观，学习曲线平缓。只需要了解 Python 即可快速上手。

### 2. 性能优秀

通过高效的对象转换算法，Purepy 能够提供出色的渲染性能。

### 3. 组件化

组件化开发让代码更容易维护和复用，提高开发效率。

### 4. 类型安全

Purepy 完全支持 Python 的类型提示系统，提供更好的开发体验。

### 5. 轻量级

核心库体积小巧，没有多余的依赖，可以轻松集成到现有项目中。

## 快速开始

### 安装

```bash
pip install yonld-purepy
```

### 基本使用

```python
from pure.html import div, h1, p

# 创建页面
div(
    h1('欢迎'),
    p('开始使用 Purepy 吧！')
).class_name('container').print()
```

## 下一步

- [快速开始](/zh/guide/getting-started) - 学习如何创建你的第一个 Purepy 应用
- [安装](/zh/guide/installation) - 了解如何安装和配置 Purepy
- [基本概念](/zh/guide/concepts) - 深入理解 Purepy 的核心概念
