# Raw API

**本页内容**：`Raw` 标记与 `Raw` 模块函数。

## 这个类

```text
Raw(value: str)
```

`Raw` 包装一个字符串，把它标记为**已经是可信的标记**。在 purepy 会转义的所有位置
——文本 slot、`Slot.value()`——`Raw` 值都会被原样输出。

| 成员 | 是什么 |
| --- | --- |
| `Raw.of(value)` | 惯用构造方式 |
| `.value` | 被包装的字符串，可读取 |
| `str(raw)` | 被包装的字符串 |

```python
from pure.core.Raw import Raw

raw = Raw.of('<b>bold</b>')

assert raw.value == '<b>bold</b>'
assert str(raw) == '<b>bold</b>'
```

## 什么时候用它

`Slot.raw()` 是接收标记的那一种 slot。`Raw` 则是你递给它的**值**，或者交给一个受
信任的 prop。

```python
from pure.compile.Compile import Compile
from pure.core.Raw import Raw
from pure.core.Slot import Slot

from pure.html import div, p

# 会转义：标签以文本形式出来。
escaped = Compile.shape(p(Slot.value('body')))
print(escaped({'body': '<b>x</b>'}))

# raw：标签以标记形式出来。
verbatim = Compile.shape(p(Slot.raw('body')))
print(verbatim({'body': Raw.of('<b>x</b>')}))
```

输出：

```html
<p>&lt;b&gt;x&lt;/b&gt;</p>
<p><b>x</b></p>
```

::: warning `Raw` 是一个承诺，不是消毒器
`Raw` 会关掉转义。只把你自己产出的内容交给它——绝不要用请求输入。对于不可信的
HTML，请先消毒再包装。
:::

## 可迭代对象

`Slot.raw()` 会拼接**任何**可迭代对象，不只是列表，因此生成器也能用：

```python
from pure.compile.Compile import Compile
from pure.core.Raw import Raw
from pure.core.Slot import Slot

from pure.html import div


def pieces():
    yield Raw.of('<b>a</b>')
    yield Raw.of('<i>b</i>')


print(Compile.shape(div(Slot.raw('items')))({'items': pieces()}))
# <div><b>a</b><i>b</i></div>
```

Python 里 `str` 是可迭代的，因此它被当作一个整体值，而不是逐字符拼接——这是有意
为之，也与 `each` slot 对字符串的处理正好相反。

## 渲染好的子组件

填充 raw slot 最常见的做法，是把另一个组件渲染进去：

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div, span

badge = Compile.shape(span('New').class_('badge'))

print(Compile.shape(div(Slot.raw('body')))({'body': badge({})}))
```

shape 是不含数据的，因此渲染好的子组件无法直接烘焙进树里——`Slot.raw()` 就是那道
接缝。*plain 视图*里则完全不能有组件，因为 plain 视图要在没有 purepy 的环境下运行。

## 相关页面

- [属性与槽位](/zh/guide/props)——`Slot.raw()` 与其他 slot 种类的对比
- [核心类](/zh/api/core)——`Tag`、`Slot`、`Markup`
