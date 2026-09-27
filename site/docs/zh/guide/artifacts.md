# 产物与部署

**前置**：[编译渲染](/zh/guide/compiled)、[组件](/zh/guide/components) · **本页内容**：`pure compile` 产物、`pure check` 契约检查、plain 视图与部署缓存。

磁盘缓存在每个请求里仍会重建 shape 树。要在部署时完全不做 shape 构建，就用
`pure` 命令提前把它们编译好。

## 预编译产物

```bash
pure compile src
```

每个 `*.cmp.py` 单元都会编译出一个同名的 `*.pure.py` 产物。产物里声明了 shape
指纹并提供一个 `Renderer`，因此它既不需要 shape 树，也不需要编译缓存：

```python
from pure.compile.Internal.ArtifactCompiler import ArtifactCompiler

page = ArtifactCompiler.loadRenderer('page.pure.py')

data = {'title': 'Users', 'items': [{'label': 'Ada'}]}

print(page.render(data))
page.save('out.html', data)
```

::: tip 进阶：独立的 `*.shape.py` 模板
除了单元文件，`pure compile` 也会发现暴露了 `shape` 属性的 `*.shape.py` 文件——
即没有调用函数的模板。组件是推荐形式；只有在没有组件适合承载该模板时，才退而
使用 shape 文件。
:::

- `pure compile <path>...` 接受文件与目录（递归搜索），同时发现 `*.cmp.py` 单元
  与 `*.shape.py` 模板，并跳过内容已是最新��文件：shape 仍会被加载和编译（这样它
  间接引入的任何改动都能被察觉），但已是最新的文件会报告为 `unchanged:` 而不
  重写。典型的一行 `--list` 输出是
  `Card -> components/Card.cmp.py (component)`；独立模板报告为
  `views/page.shape.py (shape)`，标了 `@Template()` 的构建器报告为
  `pageShape -> views/page.cmp.py (template)`。
- `--list` 只打印这些标签，不做编译。`--check` 不写任何文件，当产物过期或缺失时
  以状态码 1 退出，正好可以放进 CI。`--plain` 会额外写出下文那份零依赖视图，
  `--check --plain` 同时覆盖两种产物。
- 产物渲染的结果与运行时编译器完全一致——测试套件逐字节断言了这一点——并且产物
  携带根 slot 清单（`Renderer.slots`），因此开发守卫无需重建 shape 树就能报告
  模板从未读取的绑定。
- 对产物来说 `Renderer.source` 为空：文件本身就是源码。

生成的产物是示意性的，不是应用层 API。其中的 `SlotRuntime` 导入由
`pure compile` 写出；应用代码仍然应当调用 `renderer.render()`：

```python
# 上面的模板生成出来的样子——供阅读，不要直接调用
from pure.compile.Internal.SlotRuntime import SlotRuntime


def render(v):
    out = []
    out.append('<div')
    out.append(' class="card"')
    out.append('>')
    out.append('<h1>')
    out.append(SlotRuntime.text(v, 'title'))
    out.append('</h1>')
    out.append('<ul>')
    for v1 in SlotRuntime.items(v, 'items'):
        out.append('<li>')
        out.append(SlotRuntime.text(v1, 'label'))
        out.append('</li>')
    out.append('</ul>')
    out.append('</div>')
    return ''.join(out)
```

动态值通过 `SlotRuntime` 读取自己的 slot，从而把编译期的语义集中在一处：必填
slot 缺失时抛出 `pure.core.MissingSlotException.MissingSlotException`，可选 slot
回落到其编译好的默认值，并且转义与类型转换规则与扁平渲染器完全一致。

## Plain 视图

`--plain` 会写出第二份产物，一个 `*.plain.py` 视图：一个自带 `view()` 函数、
完全不依赖 purepy 的文件。

```bash
pure compile --plain src
```

```python title="page.plain.py"
from html import escape as _escape
from typing import Any, Dict, Iterable, List, Optional


def _text(value):
    """Escape a value for a text position, like the compiled renderer."""
    return '' if value is None else _escape(str(value), quote=False)


def view(title: Optional[str] = None, items: Optional[Iterable[Any]] = None) -> str:
    out = []
    out.append('<div')
    out.append(' class="card"')
    out.append('>')
    out.append('<h1>')
    out.append(_text(title))
    out.append('</h1>')
    out.append('<ul>')
    for i1 in (items or ()):
        out.append('<li>')
        out.append(_text(i1.get('label')))
        out.append('</li>')
    out.append('</ul>')
    out.append('</div>')
    return ''.join(out)
```

plain 视图适合放进那些支持 Python 但没装 purepy 的宿主，替代服务端渲染的模板。
它渲染出的字节与编译渲染器一致，测试套件对项目覆盖到的每个 shape 都断言了这一点。

::: warning plain 视图不是组件
plain 视图把根 slot 作为**函数参数**绑定。如果某个 slot 名无法充当参数
（`user-name`），它会回落到 `data` 偏移，即从 `data.get('user-name')` 读取。
渲染好的子组件也无法出现在 plain 视图中：组件是 purepy 的运行时行为，而该视图
必须在没有 purepy 的环境下运行。 :::

## 契约检查

`pure check` 在不渲染任何东西的前提下校验单元的契约。它加载每个单元、遍历其
shape，并报告「模板读取的内容」与「调用点绑定的内容」之间的冲突：

```bash
pure check src
```

```
checked 23 unit(s): 0 error(s), 0 warning(s).
```

检查项包括：

| 检查内容 | 报告形式 |
| --- | --- |
| 必填 slot 从未被赋值 | `slot 'title' is required but was not provided` |
| 声明的 prop 与 shape 的 slot 不符 | `prop $x declares ... but slot 'x' reads ...` |
| 列表 slot 收到非列表值 | `slot 'rows' is a list slot but parameter $rows is typed str` |
| 单元文件没有注册、或注册了多个单元 | `no component unit is registered here` / `2 component units are registered here` |
| 两个文件争抢同一个产物 | `is claimed by both ... and ...` |

出问题时它以状态码 1 退出，因此可以直接作为 CI 步骤：

```yaml
- run: pure check src --strict
```

## 部署

预编译部署需要三件事：

1. **产物落盘。** 构建时执行 `pure compile src`，把 `*.pure.py` 随发布一起带上。
2. **一个可写的缓存目录，或者干脆不要缓存。** 如果没有设置
   `Compile.cachePath()`，请求时就不会写任何东西，产物是唯一参与运行的已编译代码。
3. **版本一致。** 产物记录了构建时的 `Compile.CACHE_VERSION`，在版本不一致时拒绝
   加载，并提示 `stale purepy artifact ... run 'pure compile' to rebuild`，
   而不是在更深处报一个莫名其妙错。只要生成代码的形态发生变化，就应提升缓存版本。

```python
from pure.compile.Compile import Compile

# 产物已预编译，不需要请求期缓存。
Compile.cachePath(None)
```

一个典型的部署长这样：

```bash
pure check src                 # 有契约错误就让构建失败
pure compile src --check       # 产物是否最新
```

## 新鲜度

当 `*.pure.py` 产物存在且**不比单元文件旧**时，注册表会直接使用它，单元 factory
完全不会运行。因此你改完单元必须重新编译——否则过期的产物会继续被使用，这正是
部署故事够快、但本地也容易搞错的原因。

```bash
pure compile src --check       # 报告 `stale:` 并以 1 退出
```

## 下一步

- [编译渲染](/zh/guide/compiled)——渲染器是怎么产生的
- [故障排查](/zh/guide/troubleshooting)——检查或编译失败时
- [API 参考](/zh/api/)——`pure` 的全部参数
