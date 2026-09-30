# Purepy 与 HTMX

**Prerequisites**: [Components](/guide/components); **On this page**: server-rendered fragments, routing, and safe state changes with HTMX.

Purepy 在服务端渲染 HTML，HTMX 把返回的 HTML 换进页面。请把边界保持很小：普通路由
返回完整文档，而 HTMX 路由只返回 target 指向的那段片段。

::: tip 片段与编译后的 shape
`hx-*` 属性就是无数据树上的普通属性。把它们放进编译后的 shape，然后用请求数据
渲染同一个 shape。下面的例子使用注册过的组件，这样片段契约保持可见。
:::

## Quick Start

### 1. 安装并固定 HTMX 版本

先安装 Purepy：

```bash
python3 -m pip install purepy
```

本指南固定 HTMX **2.0.11**。使用 CDN 时请用确切的文件和它公布的 SRI 哈希：

```html
<script
  src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.11/dist/htmx.min.js"
  integrity="sha384-2OatzQy1H+Zd/IIrjr1TcuDGqLXeHhbooAyJY1KdQMKnr4LZ22k31GBLdYKHmVjg"
  crossorigin="anonymous"
></script>
```

如果自托管该文件，请在 `package.json` 与 lockfile 里记录同一个版本，然后把确切的
文件复制到 web 根目录：

```bash
npm install --save-exact htmx.org@2.0.11
mkdir -p public/assets
cp node_modules/htmx.org/dist/htmx.min.js public/assets/htmx.min.js
```

用同源 URL 提供它：

```html
<script src="/assets/htmx.min.js" defer></script>
```

SRI 只适用于 CDN 的确切字节。如果自托管，请使用固定的 npm lockfile 和你平常的
资源校验方式，不要把 CDN 哈希复制到另一个构建上。下面的前端控制器用的就是本地 URL。

### 2. 定义计数器片段

计数器页面包含一个按钮和一个数值。数值是一个独立单元，所以 POST 端点可以只返回
它，而不必把外层页面一起返回。

```python [components/CounterValue.cmp.py]
from pure.component import component, register
from pure.component.Call import Call
from pure.core.Slot import Slot
from pure.html import p


def CounterValue() -> Call:
    return component('CounterValue')


register(
    CounterValue,
    factory=lambda: p('Current count: ', Slot.value('count')).id('counter'),
    prepare=lambda count: {'count': count},
)
```

```python [components/Counter.cmp.py]
import os

from pure.component import component, register
from pure.component.Call import Call
from pure.core.Slot import Slot
from pure.loader import load_module
from pure.html import button, div

# CounterValue is a unit of its own. Loading it here also registers it, which is
# what prepare() below needs; the call function is taken from the module.
CounterValue = load_module(
    os.path.join(os.path.dirname(__file__), 'CounterValue.cmp.py'), 'CounterValue'
).CounterValue


def Counter() -> Call:
    return component('Counter')


register(
    Counter,
    factory=lambda: div(
        Slot.raw('counter'),
        button('Increment')
            .type('button')
            .hx_post('/increment')
            .hx_target('#counter')
            .hx_swap('outerHTML')
            .hx_headers(Slot.value('csrfHeaders'))
    ).class_('counter'),
    prepare=lambda count, csrfHeaders: {
        'counter': CounterValue().count(count),
        'csrfHeaders': csrfHeaders,
    },
)
```

`hx_swap="outerHTML"` 会用端点返回的新 `<p>` 替换原来的 `<p id="counter">`。
端点从不输出周围的页面。

::: tip 一个单元文件只注册一个组件
`register()` 依据你传入的函数名注册，并要求该单元文件尚未注册过其它组件。所以
`Counter.cmp.py` 里 `from CounterValue import CounterValue` 引入的是另一个文件的
单元，这正是它需要的形状。
:::

### 3. 加真正的分页

下面的列表从第 1 页开始。每次响应只追加 `<li>` 项，并用 out-of-band swap 把
“加载更多”控件换成下一页的控件。这是真正的分页：下一个 URL 由当前页推导，最后一页
较短时会移除按钮。

```python [components/TodoList.cmp.py]
from pure.component import component, register
from pure.component.Call import Call
from pure.core.Slot import Slot
from pure.html import button, div, li, ul


def TodoList() -> Call:
    return component('TodoList')


register(
    TodoList,
    factory=lambda: div(
        ul(Slot.each('items', li(Slot.value('label')))).id('todo-items'),
        button(Slot.value('label'))
            .type('button')
            .hx_get(Slot.value('nextUrl'))
            .hx_target('#todo-items')
            .hx_swap('beforeend')
            .id('load-more')
    ).id('todo'),
    prepare=lambda items, nextUrl, label: {
        'items': items,
        'nextUrl': nextUrl,
        'label': label,
    },
)
```

### 4. 定义搜索片段

输入框有真实的 `name`、可见标签和稳定的 target。端点从查询串读取 `q`，并且只
返回结果列表。

```python [components/SearchResult.cmp.py]
from pure.component import component, register
from pure.component.Call import Call
from pure.core.Slot import Slot
from pure.html import div


def SearchResult() -> Call:
    return component('SearchResult')


register(SearchResult,
    factory=lambda: div(Slot.value('title')).class_('search-result'),
    prepare=lambda title: {'title': title})
```

```python [components/ResultList.cmp.py]
import os

from pure.component import component, register
from pure.component.Call import Call
from pure.core.Slot import Slot
from pure.loader import load_module
from pure.html import div

# Loading the unit also registers it, which is what prepare() below needs.
SearchResult = load_module(
    os.path.join(os.path.dirname(__file__), 'SearchResult.cmp.py'), 'SearchResult'
).SearchResult


def ResultList() -> Call:
    return component('ResultList')


register(ResultList,
    factory=lambda: div(Slot.raw('results')),
    prepare=lambda results: {
        'results': [SearchResult().title(r['title']) for r in results]
    })
```

```python [components/SearchBox.cmp.py]
from pure.component import component, register
from pure.component.Call import Call
from pure.core.Slot import Slot
from pure.html import div, input, label


def SearchBox() -> Call:
    return component('SearchBox')


register(SearchBox,
    factory=lambda: div(
        label('Search').for_('q').class_('search-label'),
        input()
            .type('search')
            .name('q')
            .id('q')
            .placeholder('Search...')
            .autocomplete('off')
            .hx_get('/search')
            .hx_trigger('keyup changed delay:500ms')
            .hx_target('#results'),
        div(Slot.raw('list')).id('results').class_('search-results')
    ).class_('search-box'),
    prepare=lambda list: {'list': list})
```

`SearchBox` 通过 `Slot.raw()` 接收 `ResultList` 组件——因为它已经是渲染好的库
标记，而不是用户文本。

### 5. 把路由放在页面之前

下面假设 `components/` 与 `public/` 是项目根目录下的目录。创建一个前端控制器。
每个处理 HTMX 请求的分支都出现在正常页面渲染之前，写完片段就退出。
`Vary: HX-Request` 防止共享缓存把文档响应和片段响应混在一起，
`Cache-Control: private` 让带令牌的页面不进入共享缓存。路径用 `urlsplit()` 取得，
所以查询串不参与匹配。如果应用挂在前缀之下，请先显式剥掉该前缀。

```python [public/index.py]
import hmac
import json
import os
import secrets
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit

from pure.html import body, h1, head, html, meta, script, title
from pure.loader import load_module
from pure.utils import renderHTML

_UNITS = os.path.join(os.path.dirname(__file__), '..', 'components')


def unit(name: str):
    """Load one unit file and return the call function it defines.

    A unit file is named `Counter.cmp.py`, which is not a module name, so it is
    loaded by path the way purephp `require`s it. Loading registers the unit as a
    side effect and returns the module, whose same-named function is the call.
    """
    module = load_module(os.path.join(_UNITS, name + '.cmp.py'), name)

    return getattr(module, name)


# CounterValue and SearchResult load first: Counter and ResultList name them in
# their own prepare(), and a unit that has not been loaded yet is not registered.
CounterValue = unit('CounterValue')
Counter = unit('Counter')
SearchResult = unit('SearchResult')
ResultList = unit('ResultList')
SearchBox = unit('SearchBox')
TodoList = unit('TodoList')

# Where the state lives for this demo. A real application puts it in a session
# or a database; see the security notes at the end of this page.
_STATE = {'count': 0}
_TOKENS = {}


def csrf_token() -> str:
    token = _TOKENS.get('current')
    if token is None:
        token = secrets.token_hex(32)
        _TOKENS['current'] = token
    return token


def csrf_headers() -> str:
    return json.dumps({'X-CSRF-Token': csrf_token()})


def has_valid_csrf(token) -> bool:
    expected = _TOKENS.get('current')
    return (
        isinstance(expected, str)
        and expected != ''
        and isinstance(token, str)
        and hmac.compare_digest(expected, token)
    )


def positive_int(value, default=1) -> int:
    """A page number is only a number when the whole string is digits."""
    if isinstance(value, str) and value.isdigit():
        number = int(value)
        return number if number > 0 else default
    return default


def demo_search(query: str):
    if query == '':
        return []

    items = [
        {'title': 'Alpha component'},
        {'title': 'Beta component'},
        {'title': 'Gamma endpoint'},
    ]

    return [i for i in items if query.lower() in i['title'].lower()]


def document_head(page_title):
    return head(
        meta().charset('utf-8'),
        meta().name('viewport').content('width=device-width, initial-scale=1'),
        title(page_title),
        script().src('/assets/htmx.min.js').defer(True)
    )


def is_htmx(headers) -> bool:
    return (headers.get('HX-Request') or '').lower() == 'true'


def write(handler, status, body, content_type='text/html; charset=utf-8', extra=None):
    payload = body.encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', content_type)
    handler.send_header('Content-Length', str(len(payload)))
    for key, value in (extra or {}).items():
        handler.send_header(key, value)
    handler.end_headers()
    handler.wfile.write(payload)


if __name__ == '__main__':
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = urlsplit(self.path).path
            query = parse_qs(urlsplit(self.path).query)

            if path == '/search':
                results = demo_search((query.get('q') or [''])[0])
                write(self, 200, ResultList().results(results).render(),
                      extra={'Vary': 'HX-Request'})
                return

            page = html(
                document_head('HTMX + Purepy'),
                body(
                    h1('HTMX + Purepy'),
                    Counter().count(_STATE['count']).csrfHeaders(csrf_headers()),
                    SearchBox().list(ResultList().results([])),
                )
            )
            write(self, 200, renderHTML(page), extra={'Vary': 'HX-Request'})

        def do_POST(self):
            if urlsplit(self.path).path != '/increment':
                write(self, 404, 'not found', 'text/plain; charset=utf-8')
                return

            length = int(self.headers.get('Content-Length') or 0)
            form = parse_qs(self.rfile.read(length).decode() if length else '')

            # A state change needs both the HTMX marker and the token: a cookie
            # alone is not a CSRF defense.
            if not is_htmx(self.headers) or not has_valid_csrf(
                self.headers.get('X-CSRF-Token')
            ):
                write(self, 403, 'forbidden', 'text/plain; charset=utf-8',
                      extra={'Vary': 'HX-Request'})
                return

            _STATE['count'] = positive_int(
                (form.get('count') or [_STATE['count']])[0], _STATE['count']
            )
            write(self, 200, CounterValue().count(_STATE['count']).render(),
                  extra={'Vary': 'HX-Request'})

    HTTPServer(('', 8000), Handler).serve_forever()
```

运行 `python3 public/index.py`，然后打开 `http://localhost:8000/`。`public/` 下的
既有文件（诸如 `assets/htmx.min.js`）由内置服务器直接提供；生产环境的 Web 服务器
则直接提供它们。

## 安全与状态边界

- `POST /increment` 是状态变更，所以它同时要求 `HX-Request: true` 和会话绑定的
  `X-CSRF-Token`。`hmac.compare_digest()` 用来比较令牌；仅靠 cookie 不是 CSRF
  防护。上面的控制器里两者缺一都会返回 403。
- 演示状态放在进程内的字典里，因此它在多进程或多实例部署下不共享。真实应用请
  使用服务端会话或数据库，并对拥有它的会话设置 `HttpOnly`、`SameSite=Lax`，
  以及在 HTTPS 下的 `Secure`。本地的普通 HTTP 上 `Secure` 必须为 false，否则
  浏览器不会回传会话 cookie；如果由代理终止 TLS，请在选择该标志前先配置可信代理
  检测。
- 演示状态是刻意不敏感的，浏览器可以编辑它，所以绝不要用它的值做授权或权威状态。
- `Slot.value()` 会转义文本与属性值，但 `Slot.raw()` 是一个信任边界。只传入由你的
  应用产出的标记，在放进 `href` 或 `src` 前校验 URL，并让动态标签名、事件处理器和
  CSS 远离不可信输入。
- 不要把 CSRF 令牌和会话 cookie 放进客户端可见的存储。例子把令牌放在渲染进页面的
  请求头里，而 `HttpOnly` 让会话 cookie 无法被 JavaScript 访问。

## 下一步

- [HTMX 文档](https://htmx.org/docs/)
- [组件](/guide/components)
- [事件与请求边界](/guide/events)
- [安全基础](/guide/basic-usage)
