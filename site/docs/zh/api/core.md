# 核心类

Purepy 的核心类提供了创建和操作 HTML、SVG 和 XML 元素的基础功能。

## Tag 类

`Tag` 是所有元素的基类，提供了基本的元素操作功能。

### 基本用法 {#tag-class-basic-usage}

```python
from pure.core.Tag import Tag

# 创建基本标签
tag = Tag('div', ('内容'))
```

### 主要方法

#### 属性设置

```python
# 设置 CSS 类
tag.class_name('container')

# 设置 ID
tag.id('main-content')

# 设置数据属性
tag.data_id('123')
tag.data_type('card')

# 设置 ARIA 属性
tag.aria_label('按钮')
tag.aria_hidden('true')

# 设置样式
tag.style({'color': 'red', 'font-size': '16px'})
```

#### 内容操作

```python
# 添加子元素
tag.append(child_element)

# 设置文本内容
tag.text('新的文本内容')

# 获取子元素
children = tag.get_children()
```

#### 输出方法

```python
# 转换为 HTML 字符串
html_string = str(tag)

# 打印 HTML
tag.print()

# 转换为 JSON
json_data = tag.to_JSON()
```

## HTML 类

`HTML` 类继承自 `Tag`，专门用于 HTML 元素，提供了额外的 HTML 特定功能。

### 基本用法 {#html-class-basic-usage}

```python
from pure.core.HTML import HTML

# 创建 HTML 元素
html_element = HTML('div', '内容')
```

### HTML 特有方法

#### 文档保存

```python
from pure.html import html, head, title, body, div

# 创建完整的 HTML 文档
page = html(
    head(title('页面标题')),
    body(div('页面内容'))
)

# 保存为 HTML 文件（包含 DOCTYPE）
# 也可以用 save() 直接写入文件（文档根标签会自动带上 header）
with open('output.html', 'w', encoding='utf-8') as f:
    f.write('<!DOCTYPE html>\n' + str(page))
```

#### 表单元素支持

```python
from pure.html import form, input, button

# 表单元素的特殊属性
form_element = form(
    input().type('text').name('username').required(True),
    button('提交').type('submit')
).action('/submit').method('post')
```

#### 媒体元素支持

```python
from pure.html import img, video, audio

# 图片元素
img_element = img().src('image.jpg').alt('描述').width('300').height('200')

# 视频元素
video_element = video().src('video.mp4').controls(True).autoplay(False)

# 音频元素
audio_element = audio().src('audio.mp3').controls(True)
```

## SVG 类

`SVG` 类用于创建 SVG 图形元素。

### 基本用法

```python
from pure.core.SVG import SVG

# 创建 SVG 元素
svg_element = SVG('circle')
```

### SVG 特有方法

#### 几何属性

```python
from pure.svg import svg, circle, rect, line

# 圆形
circle_element = circle().cx('50').cy('50').r('40').fill('red')

# 矩形
rect_element = rect().x('10').y('10').width('100').height('50').fill('blue')

# 直线
line_element = line().x1('0').y1('0').x2('100').y2('100').stroke('black')
```

#### SVG 容器

```python
from pure.svg import svg, g

# SVG 根元素
svg_root = svg(
    circle().cx('50').cy('50').r('40').fill('red'),
    rect().x('10').y('10').width('100').height('50').fill('blue')
).width('200').height('200').viewBox('0 0 200 200')

# 分组元素
group = g(
    circle().cx('25').cy('25').r('20'),
    circle().cx('75').cy('25').r('20')
).transform('translate(10, 10)')
```

#### 保存 SVG

```python
# 保存为 SVG 文件
# 也可以用 save() 直接写入文件（文档根标签会自动带上 header）
with open('image.svg', 'w', encoding='utf-8') as f:
    f.write(str(svg_root))
```

## XML 类

`XML` 类用于创建任意的 XML 元素。

### 基本用法 {#xml-类-基本用法}

```python
from pure.core.XML import XML

# 创建自定义 XML 元素
xml_element = XML('custom-tag', '内容')
```

### XML 特有功能

#### 命名空间支持

```python
# 带命名空间的元素
xml_element = XML('ns:element', '内容').xmlns_ns('http://example.com/namespace')
```

#### 自定义属性

```python
# 任意属性名
xml_element = XML('item').set_attrs({
    'custom-attr': 'value',
    'another_attr': 'another_value'
})
```

## 工具函数

### clx 函数

用于处理条件 CSS 类名：

```python
from pure.clx import clx

# 基本用法
classes = clx('btn', 'btn-primary')  # "btn btn-primary"

# 条件类名
is_active = True
is_disabled = False
classes = clx('btn', {
    'active': is_active,      # 包含 'active'
    'disabled': is_disabled   # 不包含 'disabled'
})  # "btn active"

# 混合用法
classes = clx(
    'btn',                    # 总是包含
    'btn-primary',           # 总是包含
    {
        'active': is_active,
        'disabled': is_disabled
    }
)
```

### sty 函数

用于处理样式对象：

```python
from pure.sty import sty

# 将字典转换为 CSS 字符串
styles = sty({
    'color': 'red',
    'font-size': '16px',
    'background-color': '#f0f0f0',
    'margin': '10px 20px'
})
# 返回: "color: red; font-size: 16px; background-color: #f0f0f0; margin: 10px 20px;"

# 在元素中使用
from pure.html import div
div('内容').style(styles)
```

### Raw 类

用于插入原始 HTML 内容：

```python
from pure.raw import Raw

# 插入原始 HTML
raw_content = Raw('<strong>粗体文本</strong>')

# 在元素中使用
from pure.html import div
div('前缀 ', raw_content, ' 后缀').print()
# 输出: <div>前缀 <strong>粗体文本</strong> 后缀</div>
```

## 方法链

所有核心类都支持方法链，允许流畅的 API 调用：

```python
from pure.html import div
from pure.clx import clx
from pure.sty import sty

# 链式调用示例
element = div('内容') \
    .class_name(clx('card', {'active': True})) \
    .style(sty({'padding': '20px', 'margin': '10px'})) \
    .id('main-card') \
    .data_component('card') \
    .aria_label('主要卡片')

element.print()
```

## 自闭合标签

某些 HTML 标签会自动自闭合：

```python
from pure.html import img, br, hr, input, meta, link

# 这些标签自动自闭合
img().src('image.jpg').alt('图片')     # <img src="image.jpg" alt="图片" />
br()                                   # <br />
hr()                                   # <hr />
input().type('text').name('username') # <input type="text" name="username" />
meta().charset('UTF-8')               # <meta charset="UTF-8" />
link().rel('stylesheet').href('style.css') # <link rel="stylesheet" href="style.css" />
```

## 错误处理

核心类提供了基本的错误处理：

```python
try:
    # 创建元素
    element = div('内容').class_name('container')

    # 设置属性
    element.id('main').data_value('123')

    # 输出
    element.print()

except Exception as e:
    print(f"创建元素时发生错误: {e}")
```

## 性能考虑

### 元素重用

```python
# 避免重复创建相同的元素
base_button = button().class_name('btn')

# 克隆并修改
primary_button = base_button.clone().class_name('btn btn-primary').text('主要按钮')
secondary_button = base_button.clone().class_name('btn btn-secondary').text('次要按钮')
```

### 批量操作

```python
# 批量设置属性
element = div('内容')
attributes = {
    'class': 'container',
    'id': 'main',
    'data-component': 'layout'
}

for key, value in attributes.items():
    if key == 'class':
        element.class_name(value)
    elif key == 'id':
        element.id(value)
    else:
        element.set_attrs({key: value})
```

## 下一步

- [HTML 标签](/zh/api/html-tags) - 了解所有可用的 HTML 标签
- [SVG 标签](/zh/api/svg-tags) - 了解 SVG 图形元素
- [基本用法](/zh/guide/basic-usage) - 学习基础语法
