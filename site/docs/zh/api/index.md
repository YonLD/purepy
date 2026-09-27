# API 参考

Purepy 提供了完整的 HTML、SVG 和 XML 标签支持，以及实用的工具函数。

## 核心模块

### HTML 标签

```python
from pure.html import div, h1, p, a, img, button, input, form
```

所有 HTML5 标签都可以通过 `pure.html` 模块导入。

### SVG 标签

```python
from pure.svg import svg, circle, rect, path, g
```

完整的 SVG 标签支持，用于创建矢量图形。

### XML 标签

```python
from pure.core.XML import XML
```

动态 XML 标签创建，支持任意标签名。

### 工具函数 {#core-modules-utility-functions}

```python
from pure.clx import clx
from pure.sty import sty
from pure.raw import Raw

# 使用工具函数
classes = clx('btn', {'active': is_active, 'primary': is_primary})
styles = sty({'color': 'red', 'font-size': '16px'})
raw_content = Raw('<strong>粗体文本</strong>')

# 在元素中使用
div('内容') \
    .class_name(classes) \
    .style(styles) \
    .print()
```

## 基本用法

### 创建元素

```python
from pure.html import div, h1, p

# 创建基本元素
element = div(
    h1('标题'),
    p('段落内容')
)
```

### 设置属性

```python
from pure.html import div
from pure.sty import sty

element = div('内容') \
    .class_name('container') \
    .id('main') \
    .style(sty({'color': 'red'})) \
    .data_id('123')
```

### 输出 HTML

```python
# 转换为字符串
html_string = str(element)

# 直接打印
element.print()

# 保存到文件（HTML 元素）
from pure.html import html, head, title, body

page = html(
    head(title('页面标题')),
    body(element)
)
# 也可以用 save() 直接写入文件（文档根标签会自动带上 header）
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(str(page))
```

## 常用标签

### 文档结构

- `html()` - HTML 文档根元素
- `head()` - 文档头部
- `body()` - 文档主体
- `meta()` - 元数据
- `title()` - 文档标题
- `link()` - 外部资源链接
- `style()` - 内联样式

### 文本内容

- `h1()`, `h2()`, `h3()`, `h4()`, `h5()`, `h6()` - 标题
- `p()` - 段落
- `span()` - 内联文本
- `div()` - 块级容器
- `a()` - 链接
- `strong()`, `em()` - 强调文本

### 布局

- `div()` - 通用容器
- `section()` - 文档区块
- `article()` - 文章内容
- `header()` - 页头区块
- `footer()` - 页脚区块
- `nav()` - 导航
- `aside()` - 侧栏内容
- `main()` - 主体内容

### 列表

- `ul()` - 无序列表
- `ol()` - 有序列表
- `li()` - 列表项
- `dl()` - 定义列表
- `dt()` - 定义术语
- `dd()` - 定义描述

### 表格

- `table()` - 表格
- `thead()` - 表头
- `tbody()` - 表体
- `tr()` - 表格行
- `th()` - 表头单元格
- `td()` - 表格单元格

### 表单

- `form()` - 表单
- `input()` - 输入框
- `textarea()` - 文本域
- `select()` - 下拉选择
- `option()` - 选项
- `button()` - 按钮
- `label()` - 标签

### 媒体

- `img()` - 图片
- `video()` - 视频
- `audio()` - 音频
- `source()` - 媒体源

## 核心类

### Tag 类

所有 HTML 元素的基类：

```python
from pure.core.Tag import Tag

# 所有 HTML 元素都继承自 Tag
# 常用方法：
element.class_name('css-class')  # 设置 CSS 类名
element.id('element-id')         # 设置 ID
element.style(styles)            # 设置内联样式
element.data_key('value')        # 设置 data 属性
element.print()                  # 打印 HTML
element.to_JSON()                # 转为 JSON
str(element)                     # 转为 HTML 字符串
```

完整的属性设置器与取值器参考见 [Tag 类](/zh/api/tag)。

### HTML 类

在 Tag 之上补充 HTML 特有的行为：

```python
from pure.core.HTML import HTML

# HTML 元素支持：
html_element.save('file.html')  # 保存时带上 DOCTYPE
```

### SVG 类

用于 SVG 元素：

```python
from pure.core.SVG import SVG

# SVG 特有行为
svg_element.save('image.svg')  # 保存为 SVG 文件
```

## 工具函数

### clx() - 类名合并

```python
from pure.clx import clx

# 基本用法
classes = clx('btn', 'btn-primary')  # "btn btn-primary"

# 条件类名
is_active = True
classes = clx('btn', is_active and 'active')  # "btn active"

# 过滤空值
classes = clx('btn', None, 'primary', '')  # "btn primary"
```

### sty() - 样式处理

```python
from pure.sty import sty

# 字典样式
styles = sty({
    'color': 'red',
    'font-size': '16px',
    'background-color': '#f0f0f0'
})  # "color: red; font-size: 16px; background-color: #f0f0f0;"

# 字符串样式
styles = sty('color: red; font-size: 16px;')  # 原样返回
```

### raw_html() - 原始 HTML

```python
from pure.raw import raw_html

# 插入原始 HTML
raw = raw_html('<strong>粗体文本</strong>')

div(
    p('普通文本'),
    raw,
    p('更多文本')
).print()
```

## 方法链式

所有元素都支持方法链式调用，从而写出流畅的 API：

```python
from pure.clx import clx
from pure.sty import sty

from pure.html import div, h1, p

page = (
    div(
        h1('欢迎').class_name('title'),
        p('描述').class_name('subtitle'),
    )
    .class_name(clx('container', {'active': True}))
    .style(sty({'padding': '20px'}))
    .id('main-content')
    .data_component('hero')
)

page.print()
```

## 自闭合标签

部分 HTML 标签会自动自闭合：

- `area`、`base`、`br`、`col`、`embed`
- `hr`、`img`、`input`、`link`、`meta`
- `source`、`track`、`wbr`

```python
from pure.html import br, img, input

# 这些标签自动自闭合
img().src('image.jpg').alt('Description')
# <img src="image.jpg" alt="Description" />

br()
# <br />

input().type('text').name('username')
# <input type="text" name="username" />
```

## 下一步

- [HTML 标签](/zh/api/html-tags) - 完整的 HTML 标签列表
- [SVG 标签](/zh/api/svg-tags) - 完整的 SVG 标签列表
- [核心类](/zh/api/core) - 核心类和方法详解
