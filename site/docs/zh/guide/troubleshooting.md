# 故障排查

**本页内容**：你最可能遇到的报错、它们的成因，以及末尾的一份简短诊断清单。

## 安装与导入错误

### `ModuleNotFoundError: No module named 'pure'`

包没有装进你正在使用的解释器：

```bash
pip install -e .
```

`pure.__version__` 通过已安装的发行版元数据解析，所以装上包之后，
`pure --version` 才会报告 `pyproject.toml` 里的版本号。

### `ModuleNotFoundError: No module named 'components.Card'`

`*.cmp.py` 文件**不能**按模块名 import——那个点属于文件名，而不是包路径。请显式
加载：

```python
from pure.loader import load_module

card = load_module('components/Card.cmp.py', 'Card')
```

或者交给 `pure compile` 与组件注册表去发现，这正是 CLI 和 `pure check` 的做法。

### `SyntaxError: invalid syntax`，函数名形如 `view(user-name_: ...)`

你看到的是生成的 plain 视图源码，其中某个 slot 名不是合法的 Python 标识符。生成
器其实已经处理了这种情况：这样的 slot 会回落到 `data` 偏移，以
`data.get('user-name')` 读取。如果你是在手写的视图里看到它，请改名该 slot，或者
改用 data 偏移传入。

## Slot 与绑定错误

### `MissingSlotException: slot '...' is required but was not provided`

某个必填 slot 没有可绑定的值。消息会带上完整路径，并给出你实际提供过的、最接近
的键，或列出该作用域提供了哪些键：

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import h1

shape = Compile.shape(h1(Slot.value('title')))
shape({'titel': 'Users'})
# MissingSlotException: slot 'title' is required but was not provided;
#   did you mean 'titel'?
```

数据确实可选时，就在 shape 里说明：

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import h1

print(Compile.shape(h1(Slot.value('subtitle').required(False)))({}))
# <h1></h1>  缺失时省略

print(Compile.shape(h1(Slot.value('subtitle').default('(none)')))({}))
# <h1>(none)</h1>  缺失时回落到默认值
```

### child 或 each slot 的值被拒绝

`Slot.child()` 与 `Slot.each()` 各自开启一层嵌套数据作用域，传入的值必须具备
模板所读取的结构：

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div

inner = Compile.shape(div(Slot.value('label')))

Compile.shape(div(Slot.child('meta', inner)))({'meta': {'label': 'm'}})
# 绑定 meta={'label': 'm'} —— 一个字典，键就是子 shape 自己的 slot
```

`each` slot 的值必须是这类对象的列表。字符串会被刻意拒绝：Python 里 `str` 是可
迭代的，放行它会把一个笔误变成逐字符渲染的静默错误。

### 消息里的 `did you mean '...'?`

有两种不同的检查会产生这条提示，触发时机也不同：

- **静态**——`pure check` 在任何渲染发生之前，依据 shape 与声明的 `Prop` 报出。
- **运行时**——开发守卫报出拼错的标准属性名，或模板从未读取的数据键。参见
  [开发守卫](#开发守卫)。

### 渲染好的子组件不见了

`Markup` 值无法被烘焙进 shape。shape 是不含数据的：渲染好的子组件属于运行时行为，
因此要通过 `Slot.raw()` 进入；plain 视图里则完全不能出现组件。

## 转义与标记

### 标记被当成转义后的文本显示

这是有意为之。`Slot.value()` 会转义，`Slot.raw()` 不会。如果可信的标记是通过
`Slot.value()` 传进来的，你会看到它的标签变成文本——请改用 raw 传入。

```python
from pure.compile.Compile import Compile
from pure.core.Raw import Raw
from pure.core.Slot import Slot

from pure.html import p

print(Compile.shape(p(Slot.raw('body')))({'body': Raw.of('<b>x</b>')}))
# <p><b>x</b></p>  原样输出

print(Compile.shape(p(Slot.value('body')))({'body': '<b>x</b>'}))
# <p>&lt;b&gt;x&lt;/b&gt;</p>  转义
```

## 产物、缓存与性能

### 输出是旧的，或者产物提示你去运行 `pure compile`

当产物不比单元文件旧时，注册表会使用 `*.pure.py` 产物。两条不同的消息意味着两种
不同的问题：

- **`stale purepy artifact ... run 'pure compile' to rebuild`**——产物是用另一个
  `Compile.CACHE_VERSION` 构建的。请重新构建，不要手改它。
- **你的改动没生效**——你改了单元，但产物仍然比它新。重新编译。

```bash
pure compile src --check     # 报告 `stale:` 并以 1 退出
```

### shape 在每个请求都被重建

打开开发守卫；某个调用点累计调用二十次时会警告一次，这正是「shape 没有被记住」
的典型特征：

```python
from pure.compile.Compile import Compile

Compile.guard(True)
```

然后每个 shape 只构建一次：

```python
_shape = None


def shape():
    global _shape
    if _shape is None:
        _shape = Compile.shape(tree)
    return _shape
```

## 开发守卫

`Compile.guard(True)`——或者环境变量 `PURE_COMPILE_GUARD=1`——会打开三项开发期
检查。每个发现按主题只报告一次，因此循环里不会刷屏。

| 警告 | 含义 |
| --- | --- |
| `unknown data key 'x' (did you mean 'y'?)` | 调用点绑定了模板从未读取的键 |
| `Element 'div' has no standard attribute 'hreff'; did you mean 'href'?` | 拼错的标准属性名；自定义与 `data-*` 名不会触发 |
| `Compile.shape() was called 20 times from <file>:<line>` | 某个调用点在反复重建 shape 而不是记住它 |

守卫默认关闭，且绝不影响输出——它只发警告。请在开发环境与 CI 中打开，不要在生产
环境打开。

::: warning `Compile.guard(False)` 不等于状态干净
`DevMode.reset()` 会把开关还原为「按环境变量解析」，从而抵消掉在它之前的
`guard(True)`。如果测试先设了守卫再 reset，它会悄无声息地停止守卫。 :::

## CLI 与检查错误

### `pure compile` 报 `is claimed by both ... and ...`

两个文件解析到了同一个产物名——最常见的是同一目录下同时存在 `Box.shape.py` 和
`Box.cmp.py`，因为两者都要写 `box.pure.py`。该次运行失败，两个文件都不会被编译；
改掉其中一个基础名即可。

### `pure check` 报 `no component unit is registered here`

文件是 `*.cmp.py` 单元，但 `register()` 从未执行——通常是漏了导入，或者定义了
factory 却没有注册。

### `pure compile` 说需要组件注册表

`*.cmp.py` 单元只能由 CLI 编译，因为注册表是 CLI 接进去的。直接构造的
`ArtifactCommand()` 解析不了单元，所以库会提示你走 `bin/pure`。

## 一份简短的诊断清单

1. **先跑契约检查。** `pure check src` 能在任何渲染之前静态发现绝大多数绑定问题。
2. **打开守卫。** `Compile.guard(True)` 后重跑；警告会指明文件与行号。
3. **比较各条路径。** 对同一个 shape，`shape(data)` 与
   `shape.compile().render(data)` 必须输出一致。如果不一致，那是 purepy 的 bug，
   请连同该 shape 一起报告。
4. **检查产物新鲜度。** `pure compile src --check`。
5. **二分数据。** 用仍会失败的最小输入去渲染；异常消息里会给出完整 slot 路径。

## 下一步

- [编译渲染](/zh/guide/compiled)——shape 如何变成渲染器
- [产物与部署](/zh/guide/artifacts)——编译流水线
- [属性与槽位](/zh/guide/props)——完整 slot 参考
