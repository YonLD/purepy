# 编译 API

**本页内容**：`Compile`、`Shape`、`Renderer`、slot 种类、结构指纹、磁盘缓存、开发
守卫，以及错误。

## 类

| 类 | 是什么 |
| --- | --- |
| `Compile` | 静态入口：构建 shape、编译标签树、控制缓存与守卫 |
| `Shape` | 不含数据的树：`shape(data)`、`compile()`、`id()`、`tree()`、`print(data)`、`save(path, data)` |
| `Renderer` | 编译后的渲染器：`render(data)`、`save(path, data)`，以及 `id` / `slots` |
| `ShapeIndex` | `Shape.id()` 背后的结构指纹 |

## `Compile`

| 成员 | 签名 | 作用 |
| --- | --- | --- |
| `Compile.shape` | `(tree: Tag) -> Shape` | 把标签树包成不含数据的 shape |
| `Compile.renderer` | `(tree: Tag) -> Renderer` | 直接把标签树编译成渲染器 |
| `Compile.toShape` | `(result) -> Optional[Shape]` | 接受 `Tag` 或 `Shape` 并返回 `Shape`，否则 `None` |
| `Compile.cachePath` | `(dir) -> None` | 开启或关闭磁盘缓存 |
| `Compile.clearCache` | `() -> int` | 删除本库写出的文件，返回删除数量 |
| `Compile.flush` | `() -> None` | 丢弃内存中的渲染器 |
| `Compile.guard` | `(enabled: bool = True) -> None` | 开关开发期检查 |
| `Compile.CACHE_VERSION` | `int` | 生成代码形态变化时递增 |
| `Compile.MEMO_BYTES` | `int` | 内存中源码记忆化的预算 |

`flush()` 是长驻 worker 在部署之后要调的；`guard()` 是测试或开发服务器要打开的。

## Shape 与数据

`Shape` 是带占位符的树。数据在你调用它的时候才到来。

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot

from pure.html import div, h1, ul, li

item = Compile.shape(li(Slot.value('title')))

root = Compile.shape(
    div(
        h1(Slot.value('heading')),
        ul(Slot.each('items', item)),
    ).class_('card')
)

print(root({'heading': 'Users', 'items': [{'title': 'Ada'}]}))
```

`Compile.toShape()` 是让两者可以互换的适配器，也是 factory 返回值要经过的一步：

```python
Compile.toShape(tag_tree)        # -> Shape
Compile.toShape(shape)           # -> 同一个 Shape
Compile.toShape(render_result)   # -> None（组件调用不是树）
```

最后这一种情况正是渲染好的子组件无法被烘焙进 shape 的原因：`toShape()` 对它返回
`None`，而错误消息会明确指出这一点。

## Slot 种类

| 种类 | 助手 | 绑定的值 |
| --- | --- | --- |
| `Value` | `Slot.value(name)` | 标量，会转义；在属性位置同样有效 |
| `Raw` | `Slot.raw(name)` | 标记，或任意可迭代对象原样拼接；绝不转义 |
| `Child` | `Slot.child(name, shape)` | 一个字典，相对内部 shape 解析 |
| `Each` | `Slot.each(name, shape)` | 一个列表；每个元素跑一次内部 shape |
| `If` | `Slot.if_(name, then[, else])` | 一个布尔值；分支共享当前作用域 |

每个 slot 都支持修饰符：

| 修饰符 | 效果 |
| --- | --- |
| `.required(False)` | 可选；键缺失时省略 |
| `.default(value)` | 可选，带一个回退值 |
| `Slot.if_` 分支 | `then` 与 `else` 都是 shape |

`Each` slot 会刻意拒绝 `str`：Python 里字符串是可迭代的，放行它会把一个笔误变成
逐字符渲染。`Raw` 是例外——拼接标记本来就是它的职责，因此它接受任何可迭代对象。

## 结构指纹

`Shape.id()` 是结构体的 SHA-1 指纹。

```python
a = Compile.shape(div(Slot.value('x')))
b = Compile.shape(div(Slot.value('x')))
c = Compile.shape(div(Slot.value('y')))

assert a.id() == b.id()
assert a.id() != c.id()
```

指纹覆盖标签名、自闭合标记、每一个属性、每个 slot 的种类、路径、必填标记与默认值，
以及每一个分支标签。它混入了 `Compile.CACHE_VERSION` 与 Python 次版本号，因此运行时
升级之后绝不会复用为旧版本构建的渲染器。

`ShapeIndex` 通过代码生成器所用的同一个 `ShapeWalker` 计算指纹，因此对「同一个
shape」这件事，两者的理解永远一致。

## `Renderer` API

```python
renderer = root.compile()

renderer.render(data)     # -> str
renderer.id               # 结构指纹
renderer.slots            # 根 slot 清单，供守卫使用
renderer.source           # 生成的源码（预编译产物为空）
```

`Renderer.save(path, data)` 把渲染结果写入文件。

## 磁盘缓存

```python
from pure.compile.Compile import Compile

Compile.cachePath('/var/cache/purepy')   # 开启
Compile.cachePath(None)                  # 关闭（默认）
```

- 文件以 `Shape.id()` 为内容寻址，因此 shape 一变就会写入新文件，而不是覆盖正在
  使用的那一个。
- 写入是原子的：临时文件加 `os.rename`，并发 worker 不可能读到写了一半的渲染器。
- `cachePath()` 以 `0700` 权限创建缺失的目录，并拒绝 group 或 other 可写的目录。
  它**不会**检查路径是否位于 web 根之外——请把缓存放在专用目录里，而不是 `/tmp`。
- `Compile.clearCache()` 返回它删除的文件数量。
- `Compile.flush()` 只丢弃内存中的渲染器，不碰磁盘。

## 请求期守卫

```python
Compile.guard(True)
```

守卫默认关闭，且绝不改变输出——它只发警告，每个主题一次。它会报告模板从未读取的
数据键、拼错的标准属性名，以及某个调用点已经重建 shape 二十次。请在开发环境与 CI
中打开。参见[故障排查](/zh/guide/troubleshooting#开发守卫)。

## 错误

| 异常 | 何时抛出 |
| --- | --- |
| `pure.core.MissingSlotException.MissingSlotException` | 必填 slot 没有可绑定的值 |
| `pure.compile.CompileException.CompileException` | 编译时发现的结构性问题 |
| `pure.component.Registry` 的错误 | 重名、文件缺失，或 factory 没有返回树 |

`MissingSlotException` 会带上完整 slot 路径，并给出你实际提供过的最接近的键，或
列出该作用域提供了哪些键：

```
slot 'title' is required but was not provided; did you mean 'titel'?
```

嵌套作用域里没有「最接近的键」可言，于是改为列出该作用域提供了什么：

```
slot 'items.label' is required but was not provided; provided keys: 'text'.
```

## 带 Slot 的树不能走其他输出路径

`save()`、`print()` 和 plain 视图都通过 `Shape` 绑定数据。一棵仍含 `Slot` 占位符的
裸标签树本身无法渲染——`Tag.render()` 不接受数据，而 `Slot` 不是标记。请先经过
`Compile.shape()`。

## 下一步

- [编译渲染](/zh/guide/compiled)——这套模型的实际用法
- [产物与部署](/zh/guide/artifacts)——编译流水线
- [属性与槽位](/zh/guide/props)——完整 slot 参考
