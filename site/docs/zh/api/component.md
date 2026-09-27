# 组件 API

**本页内容**：`component()` 与 `Call`、注册单元、契约注解、`@Template`，以及注册表边界。

Purepy 有两种构建组件的方式。一个**普通函数**返回标签，对于单文件里的模板已经
够用。**注册的单元**则额外带来名字、声明的数据契约、预编译能力和静态检查。本页讲
第二种；第一种见[组件](/zh/guide/components)。

## 公开接口一览

| 名称 | 是什么 |
| --- | --- |
| `component(name, *children) -> Call` | 构造一次对已注册组件的调用 |
| `register(call, factory=None, override=False, prepare=None)` | 在 `*.cmp.py` 文件里注册一个单元 |
| `Prop(slot=, required=, item=, deprecated=)` | 标注 `prepare()` 的参数 |
| `Trusted` | 标注一个值本身就是可信标记 |
| `Binds(*keys)` | 标注 `prepare()` 的一个参数绑定了多个 slot |
| `@Template()` | 标记构建器，使 `pure compile --list` 能报告它 |
| `Registry` | 单元文件与本库之间的边界 |

## `component()` 与 `Call`

```text
component(name: str, *children) -> Call
```

`component()` 不做渲染。它返回一个 `Call`：一个可链式调用的构造器，累积具名参数，
在你要求时才渲染。

```python
from pure.component import component

card = component('Card').title('Title').content('Content')

print(card.render())
print(card)
```

`render()` 与 `str()` 产出同样的 HTML；`print(card)` 走的是后者。

| `Call` 成员 | 作用 |
| --- | --- |
| `.set(key, value)` | 按名字绑定一个 prop |
| `.props()` | 累积起来的 prop 字典 |
| `.class_(...)` / `.class_name(...)` | `class` prop 的简写 |
| `.style(...)` | `style` prop 的简写 |
| `.guard()` | 跑一遍开发期检查（`render()` 会自动调用） |
| `.render()` | 立即渲染并返回 HTML |

任何不是 `Call` 成员的名字都会变成 prop，所以模板可以声明它想要的任意参数：

```python
from pure.component import component

component('Card').title('T').anything_else(1)
```

### 子组件

`*children` 是渲染好的子组件，它们通过 `Slot.raw()` 进入模板：

```python
from pure.component import component

component('Card').title('T').content(component('Badge').label('New'))
```

::: warning 子组件需要一个 `raw` slot
shape 是不含数据的：渲染好的子组件属于运行时行为。要放置它，模板必须通过
`Slot.raw()` 读取。plain 视图里则完全不能出现组件，因为 plain 视图必须在没有
purepy 的环境下运行。 :::

## 注册一个单元

```text
register(call, factory=None, override=False, prepare=None) -> None
```

一个单元是一个 `*.cmp.py` 文件，包含三部分：**调用函数**、**factory** 和
**`prepare()`**。

```python [components/Card.cmp.py]
from pure.core.Slot import Slot

from pure.component import component, register

from pure.html import div, h2, p


def Card(*children):
    return component('Card', *children)


def factory():
    return div(
        h2(Slot.value('title')),
        p(Slot.value('content')),
    ).class_('card')


def prepare(title, content):
    return {'title': title, 'content': content}


register(Card, factory, prepare=prepare)
```

- **`call`** —— 调用点使用的函数，它的 `__name__` 就是注册名。
- **`factory`** —— 返回带 `Slot` 占位符的标签树。每个进程运行一次；把昂贵的
  计算写在它里面并做记忆化。
- **`prepare`** —— 接收调用点的参数，返回 slot 读取的数据字典。当 factory 只
  读取单个匿名数据字典时，可以省略。
- **`override`** —— 默认 `False`，重名会抛异常；`True` 会回收前一个文件占用的
  名字并接管。

一个单元文件**只注册一个**组件。`pure compile` 会拒绝没有注册的���件
（`no component unit is registered here`）和注册了多个的文件
（`2 component units are registered here`）。

::: warning `*.cmp.py` 文件不能按名字 import
那个点属于文件名，所以 `import components.Card` 行不通。请用
`pure.loader.load_module(path, name)`，或者交给 CLI 与注册表去发现。
:::

## 契约注解

`prepare()` 参数上的注解就是组件的契约，`pure check` 会读取它们。这是 purephp
里 `#[Prop]`、`#[Trusted]`、`#[Binds]` 属性的 Python 写法。

### `Prop`

```text
Prop(slot=None, required=None, item=None, deprecated=None)
```

| 字段 | 含义 |
| --- | --- |
| `slot` | 该参数以另一个名字提供这个根 slot |
| `required` | 覆盖 shape 自身的必填标记 |
| `item` | 该参数提供一个列表项，或一列列表项，item shape 如是 |
| `deprecated` | 保留该参数，但在开发守卫下发出警告 |

```python
from pure.component.Prop import Prop

def prepare(
    heading,                              # 必填的值 slot
    subtitle: Prop(required=False),       # 可选，shape 里已经这么写了
    rows: Prop(item='label'),             # 一个 item，或一列 item
    teaser: Prop(deprecated='别再用它了'),
):
    return {'heading': heading, 'subtitle': subtitle, 'rows': rows}
```

声明的 `Prop` 与 shape 不符时是一个静态错误：

```
error: prop $features declares one item slot 'vaule' but the item shape of
       slot 'features' reads 'value' (did you mean 'value'?)
```

### `Trusted`

```python
from pure.component.Trusted import Trusted

def prepare(body: Trusted):
    return {'body': body}
```

`Trusted` 标记一个值本身就是可信标记：它不会再被转义。只对你自己产出的内容使用，
绝不要用于请求输入。

### `Binds`

```python
from pure.component.Binds import Binds

def prepare(media: Binds('src', 'alt')):
    return {'src': media['src'], 'alt': media['alt']}
```

`Binds(*keys)` 声明一个参数提供多个 slot。

## `@Template`

```python
from pure.compile.Template import Template

@Template()
def page_shape():
    return Compile.shape(div(Slot.value('title')))
```

`@Template()` 标记一个做了记忆化的 shape 构建器。这个标记不改变任何渲染行为；它
让 `pure compile --list` 把该构建器报告为 `name -> file (template)`，使大型单元
依然可导航。

## Registry 边界

`Registry` 是单元文件与本库之间的接缝。应用代码通常不直接碰它——CLI 会把它接好
——但它是公开的，静态分析各趟就是驱动它的。

| 成员 | 作用 |
| --- | --- |
| `Registry.register(name, file, factory, override, prepare)` | 底层注册，由 `register()` 调用 |
| `Registry.component(name_or_path) -> Callable` | 单元绑定好的渲染器，可按名字或文件路径 |
| `Registry.names() -> set` | 所有已注册的名字 |
| `Registry.unitsFor(file) -> dict` | 某个文件声明的单元，即 `pure compile` 使用的解析器 |
| `Registry.slots(name_or_path) -> list` | 单元的根 slot 清单 |
| `Registry.prepare(name_or_path) -> Callable` | 单元的 `prepare()` 钩子 |
| `Registry.reset()` | 丢弃所有注册——供测试使用 |

`Registry.component('Card')` 与 `Registry.component('components/Card.cmp.py')`
解析到同一个 binder，因此调用点两种写法都可以。

## 相关页面

- [组件](/zh/guide/components)——组件模型的实际用法
- [属性与槽位](/zh/guide/props)——完整 slot 参考
- [产物与部署](/zh/guide/artifacts)——单元如何变成文件
