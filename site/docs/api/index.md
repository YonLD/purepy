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

### 工具函数

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
    .to_print()
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
element.to_print()

# 保存到文件（HTML 元素）
from pure.html import html, head, title, body

page = html(
    head(title('页面标题')),
    body(element)
)
# 注意：Purepy 目前不支持 to_save 方法，需要手动保存
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

## 属性方法

### 通用属性

- `.id(value)` - 设置 ID
- `.class_name(*values)` - 设置 CSS 类
- `.style(value)` - 设置样式
- `.title(value)` - 设置标题
- `.lang(value)` - 设置语言

### 数据属性

- `.data_*(value)` - 设置数据属性（如 `.data_id('123')`）

### 事件属性

- `.onclick(value)` - 点击事件
- `.onchange(value)` - 变化事件
- `.onsubmit(value)` - 提交事件
- `.onload(value)` - 加载事件

### 表单属性

- `.type(value)` - 输入类型
- `.name(value)` - 表单名称
- `.value(value)` - 表单值
- `.placeholder(value)` - 占位符
- `.required()` - 必填
- `.disabled()` - 禁用

### 链接属性

- `.href(value)` - 链接地址
- `.target(value)` - 打开方式

### 媒体属性

- `.src(value)` - 资源地址
- `.alt(value)` - 替代文本
- `.width(value)` - 宽度
- `.height(value)` - 高度

## 工具函数详解

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
).to_print()
```

## 下一步

- [HTML 标签](/api/html-tags) - 完整的 HTML 标签列表
- [SVG 标签](/api/svg-tags) - 完整的 SVG 标签列表
- [核心类](/api/core) - 核心类和方法详解
