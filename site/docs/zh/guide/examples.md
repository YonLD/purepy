# 示例

仓库在 `examples/` 下维护可运行的示例。它们使用同样的组件、编译与 plain 视图
路径，所以你可以把一个小型生产 shape 与一个零依赖视图做对比。

## 从一小段代码开始

```python
from pure.html import a, div

div(
    'Hello ',
    a('Python').href('https://www.python.org')
).class_('container').print()
```

组件带来一份有类型的 prop 契约和一份无数据的 shape。`register()` 接收调用函数
本身——组件名就来自它：

```python
from pure.component import component, register
from pure.component.Call import Call
from pure.core.Slot import Slot
from pure.html import div, h2, p


def Card() -> Call:
    return component('Card')


register(
    Card,
    factory=lambda: div(
        h2(Slot.value('title')),
        p(Slot.value('content'))
    ).class_('card'),
    prepare=lambda title, content: {'title': title, 'content': content},
)

print(Card().title('Card Title').content('Card Content').render())
```

::: tip 为什么是函数而不是调用结果
注册表以来源函数的名字作为组件的键，所以写 `register(Card, ...)` 而不是
`register(Card(), ...)`。lambda 也会因为没有名字可注册而被拒绝。详见
[组件](/zh/guide/components)。
:::

## 子节点、列表与按钮

这个单元在一份 shape 里展示了三条常见数据路径：通过保留的 raw slot 传入子节点、
通过 `Slot.each()` 重复记录、以及通过值 slot 设置按钮属性。

```python
from pure.component import component, register
from pure.component.Call import Call
from pure.core.Slot import Slot
from pure.html import button, div, h2, li, ul


def PricingCard(*children) -> Call:
    return component('PricingCard', *children)


register(
    PricingCard,
    factory=lambda: div(
        Slot.raw('children'),
        h2(Slot.value('type')).class_('card-title'),
        ul(Slot.each('features', li(Slot.value('value')))),
        button(Slot.value('text')).class_(Slot.value('class'))
    ).class_('card'),
    prepare=lambda **props: {
        'type': props['type'],
        'features': props['features'],
        'text': props['text'],
        'class': props['class'],
    },
)

print(div(
    PricingCard(h2('Pro'))
        .type('Free')
        .features([{'value': '10 users'}, {'value': '2 GB'}])
        .text('Sign up for free')
        .class_('btn btn-lg btn-block btn-outline-primary')
).render())
```

::: warning `type` 与 `class` 是 Python 内置名
`prepare` 是用关键字参数接收 props 的，所以它无法把参数命名为 `type` 或 `class`
——那是语法错误，而不是遮蔽问题。上面的 `**props` 写法就是绑定这类 prop 的方式。
调用点上的 prop 名称不受影响。
:::

子节点传给调用，列表可以用 `Slot.each()` 绑定，组件调用实现了
`pure.core.Markup.Markup`，所以它们能嵌进标签树。完整词汇请从
[快速开始](/zh/guide/getting-started) 读到[组件](/zh/guide/components)。

## 准备仓库

示例不随 wheel 发布，所以请克隆仓库并在它的根目录执行下面的命令：

```bash
git clone https://github.com/YonLD/purepy.git
cd purepy
python3 -m pip install -e .
python3 bin/pure compile --plain examples/bootstrap
python3 bin/pure compile --plain examples/event-counter
python3 bin/pure compile --plain examples/xml
```

用 `--list` 查看发现的单元。输出里的标签是 `(component)`、`(shape)` 和
`(template)`；页面不是单独的文件类型：

```bash
python3 bin/pure compile --list examples
```

## Bootstrap MVC 示例

`examples/bootstrap` 是一个小型 MVC 应用。控制器保持轻薄，DAO 读取数据，服务把
记录转成绑定，组件单元拥有自己的标记。`features` 与 `pricing` 两个页面同时有
严格产物和 plain 视图。封面页是静态标记，有意不提供这两个变体。

| 路由 | 渲染内容 |
| --- | --- |
| `/cover` | 静态的 `views/cover.py`；无需编译。 |
| `/pure/features` | 页面函数加上 `*.pure.py` 组件产物。 |
| `/plain/features` | 组件绑定渲染后的 `features.plain.py`。 |
| `/pure/pricing` | 页面函数加上 `*.pure.py` 组件产物。 |
| `/plain/pricing` | 组件绑定渲染后的 `pricing.plain.py`。 |

从仓库根目录运行它的前端控制器：

```bash
python3 examples/bootstrap/public/index.py --serve
```

访问 `http://localhost:8000/cover`，然后对比 `/pure/features` 与
`/plain/features`，以及 `/pure/pricing` 与 `/plain/pricing`。未知路径返回一个
列出全部五条路由的 404 页面。同一个入口也能把单页打印到 stdout——这是不启动
服务器就能对比两个变体最快的方式：

```bash
python3 examples/bootstrap/public/index.py /pure/features > /tmp/strict.html
python3 examples/bootstrap/public/index.py /plain/features > /tmp/plain.html
diff /tmp/strict.html /tmp/plain.html
```

plain 加载器按名字把数据传给生成的 `view()`。`Call` 绑定会在该视图加载之前被
转成标记，所以 plain 文件本身在渲染时不需要 Purepy。

## 计数器示例

`examples/event-counter` 展示一个带随机初值（`random.randint(0, 100)`）和浏览器端
`+` / `-` 控件的小页面。它有同样的严格与 plain 两个变体：

| 路由 | 渲染内容 |
| --- | --- |
| `/` 或 `/index.py` | 重定向到 `/plain`。 |
| `/pure` | 页面函数和 `counter.pure.py`。 |
| `/plain` | `counter.plain.py`，视图里没有任何库调用。 |

运行方式：

```bash
python3 examples/event-counter/public/index.py --serve
```

打开 `http://localhost:8000/pure` 或 `/plain`，然后使用计数器按钮。JavaScript
和 CSS 是 `public/` 下的静态文件；前端控制器把它们交回内置服务器，由后者直接
提供。

## XML 示例

`examples/xml` 展示 XML 根、嵌套的 item shape、可选字段，以及一个 `Template`
构建器。它走的是 `XML.state` 与 `XML.address` 两个分支；响应是 XML 而非 HTML：

| 路由或命令 | 作用 |
| --- | --- |
| `/` 或 `/index.py` | 重定向到 `/plain`。 |
| `/pure` | 页面函数和 `xml.pure.py`。 |
| `/plain` | `xml.plain.py`，作为完整文档渲染。 |
| `python3 examples/xml/write.py` | 写出 `examples/xml/example.xml` 并打印字节数。 |

Web 版本：

```bash
python3 examples/xml/public/index.py --serve
```

或者从仓库根目录写出文件：

```bash
python3 examples/xml/write.py
```

XML 声明由 `renderXML()` 提供；模板本身只描述树。这个 XML shape 用
`Slot.each()` 处理列表，用 `Slot.if_()` 处理可选的 city。

## 对比严格与 plain 输出

对于普通数据，生成的 plain 视图与严格产物逐字节相同，根是 HTML 或 XML 文档时
也包含文档头。当部署只提供 `public/` 与 `views/`、不安装 Purepy 时，plain 路径
很有用。它是一个基于 include 的视图，而不是第二套模板语言。

排查路由缺失、产物过期或片段被转义的问题，请看
[故障排查](/zh/guide/troubleshooting)。与版本相关的重新生成步骤，请看
[升级指南](/zh/guide/upgrading)。
