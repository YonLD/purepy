# Tag API

**本页内容**：元素基类——属性设置器、取值器、输出方法，以及动态属性是如何工作的。

`Tag` 是所有元素类的基类：`HTML`、`SVG` 与 `XML`。各个标签函数
（`div()`、`span()`、`path()`……）都返回一个 `Tag` 子类实例。

```python
from pure.html import div, span

tag = div(span('x')).class_('card')
```

## 属性设置器

属性通过方法调用来设置，未知的方法名会变成一个属性：

```python
from pure.html import a, div

div().id('main').data_id('7').title('a tip')
a('x').href('/target').rel('help')
```

`data_id` 会变成 `data-id`，`aria_label` 变成 `aria-label`——下划线变连字符。有
两个例外：

- **结尾**的下划线用于转义 Python 关键字：`for_()` 渲染出 `for="…"`、
  `class_()` 渲染出 `class="…"`、`is_()` 渲染出 `is="…"`。尾下划线只做关键字
  检查，因此 `data_id()` 照常工作。
- purephp 用的那些精确名称可以直接作为方法使用：`class_name()` 与
  `className()` 都渲染出 `class`。

### 值

| 值 | 渲染为 |
| --- | --- |
| `str`、`int`、`float` | 转义后的值 |
| `True` | 只有属性名，例如 `checked` |
| `False` 或 `None` | 省略该属性 |
| `Slot` | 该 slot 的值，在属性位置会转义 |
| `Raw` | 原样输出 |

```python
from pure.html import input, label

input().type('checkbox').checked(True).disabled(False)
# <input type="checkbox" checked="checked" />

label().class_('a', 'b', 'c')     # 用空格连接
```

数组形式的属性请用 `Slot`，或者用 `style()` / `class_()`；把列表直接传给普通属性
会被拒绝，而不是被静默拼接。

### 批量设置

```python
div().set_attrs({'data-id': '7', 'id': 'main', 'hidden': True})
```

`set_attrs(props: dict) -> Tag` 一次设置多个并返回自身，因此可以链式调用。当键是
计算出来的，用它最合适。

## 取值器

| 方法 | 返回 |
| --- | --- |
| `get_tag_name()` | 标签名，例如 `'div'` |
| `get_attrs()` | 属性字典，含 `Slot` 值 |
| `get_attr(key)` | 单个值，或 `None` |
| `get_children()` | 子节点列表：`str`、`Raw`、`Tag` 或 `Slot` |
| `get_self_close()` | 是否为自闭合标签 |
| `export()` | 整棵树导出为字典——编译器遍历的就是它 |
| `to_JSON()` | 整棵树导出为 JSON 字符串 |
| `tree()` | 底层的 `Tag` 节点 |

## 输出

```text
render() -> str
save(path: str, header: Optional[str] = None) -> None
print() -> None
```

- `render()` 返回 HTML。它不接受数据：仍含 `Slot` 占位符的标签树本身无法渲染，
  请先经过 `Compile.shape()`。
- `save(path, header=None)` 写入文件，默认前缀是该类的默认 header：HTML 是
  `<!DOCTYPE html>`，SVG 与 XML 是 `<?xml version="1.0"?>`。这个前缀是**无条件**
  的——保存一个裸 `div()` 依然会写入 doctype，purephp 也是如此。要写入纯片段请传
  `header=''`，要自定义则传 `header='...'`。
- `print()` 把渲染结果写到标准输出。

```python
from pure.html import div, html, body

page = html(body(div('content')))
page.save('index.html')
# <!DOCTYPE html><html><body><div>content</div></body></html>

div('a fragment').save('fragment.html', '')
# a fragment
```

::: tip 输出永远不会被重新缩进
Purepy 输出的就是它渲染的字节。你写在多行的标记，出来时在同一行。
:::

## 开发期守卫

| 方法 | 作用 |
| --- | --- |
| `guardAttributeName(key)` | 设置属性前调用的钩子；基类上是空实现 |
| `guardStandardAttribute(key)` | 在守卫开启时，对每个拼错的标准属性名警告一次 |

`HTML` 与 `SVG` 覆写第一个以调用第二个；`XML` 保持空实现，因为 XML 树自带自己的
属性命名。参见[故障排查](/zh/guide/troubleshooting#开发守卫)。

## 文档根

| 方法 | 作用 |
| --- | --- |
| `isDocumentRoot()` | 该标签是否开启一份文档 |
| `documentHeader()` | 文档根所需的 header |
| `defaultHeader()` | 子类自己的默认 header |

## 子类说明

| 类 | Header | 说明 |
| --- | --- | --- |
| `HTML` | `<!DOCTYPE html>` | 空元素拒绝子节点；自闭合渲染为 `<br />` |
| `SVG` | `<?xml version="1.0"?>` | 属性保留驼峰式（`viewBox`） |
| `XML` | `<?xml version="1.0"?>` | 任意元素名；没有标准属性表 |

## 相关页面

- [HTML 标签](/zh/api/html-tags)——完整元素列表
- [核心类](/zh/api/core)——`Slot`、`Raw`、`Escaper`
- [基本用法](/zh/guide/basic-usage)——属性的实际写法
