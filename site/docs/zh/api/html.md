# HTML 类

**本页内容**：`HTML` 类——如何创建元素、静态构造器、保存方法与自闭合标签。

`pure.core.HTML.HTML` 继承 Tag 类，专门用于 HTML 标签。

## 创建 HTML 元素

标准标签来自 `pure.html` 模块的函数。其它标签名可以直接从类上读取——读取的属性
名就是标签名：`HTML.myWidget('x')` 会生成 `<myWidget>x</myWidget>`。如果标签名
不是合法的 Python 标识符（比如带连字符的自定义元素），用动态形式
`getattr(HTML, 'user-card')('x')`。

### 1. 函数（标准标签）

```python
from pure.html import div, p, span

d = div('Content')
paragraph = p('Paragraph')
highlighted = span('Text').class_('highlight')
```

函数名与标签名一一对应。标签名若是 Python 关键字就无法作为函数名，所以 `<class>`
没有对应的模块级函数；和 purephp 一样，用类上的动态形式即可。

与 purephp 不同，`<var>`、`<use>`、`<switch>` 不需要别名——它们都不是 Python 关键字，
所以 `pure.html.var()`、`pure.svg.use()`、`pure.svg.switch()` 直接使用原名。

### 2. 从类上读取标签名

```python
from pure.core.HTML import HTML

# 任意标签名都可以：读取的属性名就是标签名
element = HTML.customTag('Content').class_('custom')
# <customTag class="custom">Content</customTag>

component = HTML.myWebComponent(HTML.header('Header'))

# 带连字符的自定义元素走动态形式
web_component = getattr(HTML, 'user-card')('Content')
# <user-card>Content</user-card>
```

**适用场景：**
- 自定义 HTML 标签
- Web 组件
- 非标准 HTML 元素

::: tip
`div` 与 `HTML.div` 生成的是同一个元素。标签名需要由变量决定时，类上的形式更顺
——模块级函数同样得按名字查找。
:::

## 保存方法

### `save(path, header=None)`

把元素写入文件。省略 `header` 时会先写 `<!DOCTYPE html>`。

```python
from pure.html import html, head, title, body, div

page = html(
    head(title('Page Title')),
    body(div('Page Content'))
)

written = page.save('output.html')
if written is not None:
    print('File saved successfully, wrote {} bytes'.format(written))
```

返回值是写入的字节数，文件固定为 UTF-8，与 locale 无关，所以返回的字节数就是文件
里实际的字节数——这与 purephp 的 `save()` 一致。

## 自闭合标签

HTML 类会自动识别以下自闭合标签：
- `area`、`base`、`br`、`col`、`embed`、`hr`、`img`、`input`、`link`、`meta`、`source`、`track`、`wbr`

```python
from pure.html import img, br, hr

# 这些标签会自动设为自闭合
img().src('image.jpg').alt('Image')
br()
hr()
```

## 示例

### 基础 HTML 结构

```python
from pure.html import html, head, meta, title, body, div, h1, p
from pure.utils import renderHTML

page = html(
    head(
        meta().charset('UTF-8'),
        meta().name('viewport').content('width=device-width, initial-scale=1.0'),
        title('My Page')
    ),
    body(
        div(
            h1('Welcome'),
            p('This is my website.')
        ).class_('container')
    )
).lang('en')

print(renderHTML(page))
```

### 表单

```python
from pure.html import form, div, label, input, textarea, button
from pure.utils import renderHTML

contact_form = form(
    div(
        label('Name:').for_('name'),
        input().type('text').id('name').name('name').required(True)
    ).class_('form-group'),
    div(
        label('Email:').for_('email'),
        input().type('email').id('email').name('email').required(True)
    ).class_('form-group'),
    div(
        label('Message:').for_('message'),
        textarea('').id('message').name('message').rows('5').required(True)
    ).class_('form-group'),
    button('Send Message').type('submit')
).method('POST').action('/contact')

print(renderHTML(contact_form))
```

::: tip 关键字的两种写法
`for_` 是 Python 关键字的尾下划线转义写法，输出 `for="name"`，这才是元素需要的。
`htmlFor` 是同一个方法的别名。注意都不是 `html_for`：那只是个普通属性名，会输出
`html-for="name"`——purephp 也是如此。
:::

### 自定义元素

```python
from pure.core.HTML import HTML

card = HTML.cardComponent(
    HTML.cardHeader('Card Title'),
    HTML.cardBody('Card content goes here'),
    HTML.cardFooter('Card footer')
).data_component('card').class_('custom-card')

print(card.render())
```

### 长列表

```python
from pure.html import li, ul
from pure.utils import renderHTML

# 整个列表作为单个子节点传入，一次构建完成
items = [li('Item {}'.format(i)) for i in range(1, 1001)]

print(renderHTML(ul(items)))
```
