# 编译渲染

**前置**：[组件](/zh/guide/components) · **本页内容**：组件模板如何编译、运行时缓存与性能。

编译渲染把一个不含数据的 **Shape**（也就是组件的模板）编译成一段扁平的 Python
渲染器。静态标记在编译期就完成转义并作为字面量输出，因此渲染一个页面的开销，
基本只剩字符串拼接加上动态值的转义。

组件的 factory 返回一棵由 `Slot` 占位符组成的标签树；注册表会把它包成 `Shape`
——和 `Compile.shape()` 对内联树所做的包装完全一样。模板在**每个进程内只构建
一次**，适用于长驻 worker、CLI 进程，或任何在请求之间保留模块状态的宿主。
在标准 WSGI 下每个请求都是全新进程，此时应开启磁盘缓存（见[缓存](#缓存)），
直接加载已编译的渲染器，而不是每个请求重新生成；或者干脆部署预编译产物
（见[产物与部署](/zh/guide/artifacts)）。

## Shape、Slot、Renderer

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div, h1, li, ul

# Shape 就是一棵用 Slot 占位符代替数据的普通标签树。
item = Compile.shape(li(Slot.value('title')))

root = Compile.shape(
    div(
        h1(Slot.value('heading')),
        ul(Slot.each('items', item)),
    ).class_('card')
)

# 渲染时再绑定数据。
print(root({
    'heading': 'Users',
    'items': [{'title': 'Ada'}, {'title': 'Grace'}],
}))
```

输出：

```html
<div class="card"><h1>Users</h1><ul><li>Ada</li><li>Grace</li></ul></div>
```

| 对象 | 含义 |
| --- | --- |
| `Shape` | 不含数据的树：`shape(data)`、`compile()`、`id()`、`print(data)`、`save(path, data)` |
| `Renderer` | 编译后的渲染器：`render(data)`、`save(path, data)`，以及 `source` / `id` / `slots` 属性 |
| `Slot` | 数据的占位符，在渲染时绑定 |

四条渲染路径——`shape(data)`、`renderer.render(data)`、扁平的 `CodeGenerator`
路径，以及生成的 plain 视图——对同一棵树产出**逐字节相同**的结果，因为它们共用
同一套转义实现。测试套件正是这么断言的，因此任何一条路径出现偏差都会变成测试
失败，而不是生产环境里的意外。

模板可用的 slot（`Slot.value()`、`Slot.raw()`、`Slot.child()`、`Slot.each()`、
`Slot.if_()`）、它们的修饰符、值转换规则与缺失数据的处理，统一在
[属性与槽位](/zh/guide/props#slot-速查)里讲一次，本页不重复。

## 作用域与缺失数据

`Slot.child()` 和 `Slot.each()` 会开启一层嵌套数据作用域；在其内部，slot 相对该
作用域解析。缺失的必填键会抛出
`pure.core.MissingSlotException.MissingSlotException`，消息里带上完整路径，并
给出最接近的已提供键，或列出该作用域实际提供了哪些键。可选数据请用
`.default(value)` 或 `.required(False)`——完整规则见
[属性与槽位](/zh/guide/props)。

`Slot.if_()` 的分支共享当前作用域，因此下面这样写很自然：

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import li, span

item = Compile.shape(
    li(
        Slot.value('name'),
        Slot.if_('admin', span('(admin)')),
    )
)
```

::: tip Python 关键字的转义约定
`if` 是 Python 关键字，所以分支助手叫 `Slot.if_()`。同样的约定也适用于属性：
`for_()` 渲染出 `for="…"`、`class_()` 渲染出 `class="…"`，而 `data_id()` 仍
渲染出 `data-id="…"`。尾下划线只用于转义关键字；其他位置的 `_` 一律变成连字符。
:::

## 组件

组件的模板——一个包含调用函数、惰性 factory 和 `prepare()` 钩子的 `*.cmp.py`
单元（完整说明见[组件](/zh/guide/components)）——走的是同一条流水线：factory 每次
编译只运行一次，标签树包成 shape，而编译出的渲染器会被后续请求复用。

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

`*.cmp.py` 文件无法按模块名直接 import——那个点属于文件名，而不是包路径。用
`pure.loader.load_module` 加载，或者交给 CLI 与组件注册表去发现：

```python
from pure.loader import load_module

card = load_module('components/Card.cmp.py', 'Card')

print(card.Card().title('Title').content('Content'))
```

输出：

```html
<div class="card"><h2>Title</h2><p>Content</p></div>
```

在模板内部，嵌套 shape 用 `Slot.child()`，列表用 `Slot.each()`，可选/条件标记用
`Slot.if_()`，而渲染好的子组件只能通过 `Slot.raw()` 进入。

## 列表

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import li, ul

row = Compile.shape(li(Slot.value('label')))

shape = Compile.shape(ul(Slot.each('rows', row)))

print(shape({'rows': [{'label': 'a'}, {'label': 'b'}]}))
```

## 缓存

默认情况下编译后的渲染器只存在于内存中，这适合在请求之间保留状态的长驻 worker。
在普通 WSGI 服务器下，shape 树会在每个请求重建、渲染器重新生成——比直接渲染更
慢——因此应开启磁盘渲染器缓存，加载已生成的代码：

```python
from pure.compile.Compile import Compile

# 在启动时设置一次
Compile.cachePath('/var/cache/purepy')
```

- `Compile.cachePath(dir)` 开启磁盘渲染器缓存；传 `None` 关闭（默认值）。
- 缓存文件以 `Shape.id()` 为内容寻址；shape 一变就写入新文件。
- 写入是原子的（临时文件加 `os.rename`），并发 worker 是安全的。
- `cachePath()` 会以 `0700` 权限创建缺失的目录，并拒绝 group/other 可写的目录。
  它**不会**检查路径是否位于 web 根目录之外，所以请把缓存放在文档根之外的专用
  目录里。
- `Compile.clearCache()` 删除由本库写出的文件。
- `Compile.flush()` 让内存中的渲染器失效（长驻 worker 部署后很有用）。

### 记住你的 shape

为了捕获「每个请求都重建 shape 而没有记住」的情况，打开开发守卫：

```python
from pure.compile.Compile import Compile

Compile.guard(True)
```

它还会对拼错的��准属性名、以及模板从未读取的数据键发出警告。参见
[开发守卫](/zh/guide/troubleshooting#开发守卫)。

每个 shape 只构建一次并复用：

```python
_shape = None


def shape():
    global _shape
    if _shape is None:
        _shape = Compile.shape(div(Slot.value('title')))
    return _shape
```

## Shape 标识

`Shape.id()` 是结构体的 SHA-1 指纹：同一棵树永远得到同一个 id，任何结构变动都会
得到不同的 id。它混入了 `Compile.CACHE_VERSION` 与 Python 次版本号，因此运行时升级
之后绝不会复用为旧版本构建的渲染器。

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div

a = Compile.shape(div(Slot.value('x')))
b = Compile.shape(div(Slot.value('x')))
c = Compile.shape(div(Slot.value('y')))

assert a.id() == b.id()   # 结构相同，id 相同
assert a.id() != c.id()   # slot 名不同，id 不同
```

指纹通过代码生成器所用的同一个 `ShapeWalker` 遍历整棵树，因此 shape 与其编译产物
对「同一个 shape」永远有一致的理解。

## 下一步

- [产物与部署](/zh/guide/artifacts)——把模板预编译成文件
- [属性与槽位](/zh/guide/props)——完整 slot 参考
- [故障排查](/zh/guide/troubleshooting)——调试编译不过的 shape
