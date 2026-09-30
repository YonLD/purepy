# 事件

**前置**：[基本用法](/zh/guide/basic-usage)；**本页内容**：无障碍的浏览器事件、事件委托，以及符合 CSP 的监听器写法。

Purepy 负责渲染 HTML，浏览器 JavaScript 负责交互。用 Python 输出语义化的控件和
无障碍的状态区域，再用 JavaScript 的 `addEventListener` 挂上行为。

::: tip 优先使用外部监听器
`onclick(...)`、`oninput(...)` 这类标签方法是有效的：它们写出内联的 `onclick` 或
`oninput` 属性。省略了 `'unsafe-inline'` 的 Content Security Policy 会阻止这些
处理器。所以下面的例子把行为放在元素属性之外，改用 `addEventListener`。
:::

## 基础事件处理

把它存为已安装 Purepy 的项目里的 `events.py`，然后运行 `python3 events.py`：

```python
from pure.html import button, div, input, label, output, p
from pure.utils import renderHTML

print(renderHTML(div(
    label('Message').for_('event-message'),
    input()
        .id('event-message')
        .name('message')
        .aria_describedby('event-help'),
    p('The status is announced after either control changes.').id('event-help'),
    button('Show message').type('button').id('event-trigger'),
    output('Ready.').id('event-status').aria_live('polite')
).class_('events-container')))
```

```html
<script>
const eventTrigger = document.getElementById('event-trigger');
const eventInput = document.getElementById('event-message');
const eventStatus = document.getElementById('event-status');

eventTrigger.addEventListener('click', () => {
    eventStatus.textContent = 'Message button activated.';
});

eventInput.addEventListener('input', event => {
    eventStatus.textContent = `Current message: ${event.target.value || '(empty)'}`;
});
</script>
```

输入框有真实的 `<label>`，动作用的是语义化的 `<button type="button">`，而
`<output aria-live="polite">` 会在不移动键盘焦点的情况下播报更新。

## 鼠标事件

用按钮承载动作，并通过活动区域暴露结果：

```python
from pure.html import button, div, output
from pure.utils import renderHTML

print(renderHTML(div(
    button('Hover and click me').type('button').id('mouse-button'),
    output('Waiting for an event.').id('mouse-status').aria_live('polite')
).class_('mouse-events')))
```

```html
<script>
const mouseButton = document.getElementById('mouse-button');
const mouseStatus = document.getElementById('mouse-status');

mouseButton.addEventListener('click', () => {
    mouseStatus.textContent = 'Clicked';
    mouseButton.style.backgroundColor = '#f0f0f0';
});

mouseButton.addEventListener('mouseover', () => {
    mouseButton.style.backgroundColor = '#e0e0e0';
});

mouseButton.addEventListener('mouseout', () => {
    mouseButton.style.backgroundColor = '';
});

mouseButton.addEventListener('mousedown', () => {
    mouseButton.style.transform = 'scale(0.95)';
});

mouseButton.addEventListener('mouseup', () => {
    mouseButton.style.transform = 'scale(1)';
});
</script>
```

## 键盘事件

保留可见标签、描述活动输出，并监听键盘输入：

```python
from pure.html import div, input, label, output
from pure.utils import renderHTML

print(renderHTML(div(
    label('Keyboard input').for_('keyboard-input'),
    input()
        .id('keyboard-input')
        .type('text')
        .aria_describedby('key-display'),
    output('Focus the input and press a key.').id('key-display').aria_live('polite')
).class_('keyboard-events')))
```

```html
<script>
const keyboardInput = document.getElementById('keyboard-input');
const keyDisplay = document.getElementById('key-display');

function handleKeyDown(event) {
    keyDisplay.textContent = `Key pressed: ${event.key} (Code: ${event.code})`;
}

function handleKeyUp(event) {
    console.log('Key released:', event.key);
}

function handleInput(event) {
    console.log('Input value:', event.target.value);
}

keyboardInput.addEventListener('keydown', handleKeyDown);
keyboardInput.addEventListener('keyup', handleKeyUp);
keyboardInput.addEventListener('input', handleInput);
</script>
```

## 表单事件

每个控件都关联标签，并播报校验或提交状态：

```python
from pure.html import button, div, form, input, label, output
from pure.utils import renderHTML

print(renderHTML(div(
    form(
        div(
            label('Username').for_('username'),
            input().id('username').name('username').required(True)
        ),
        div(
            label('Email').for_('email'),
            input().id('email').name('email').type('email').required(True)
        ),
        button('Submit').type('submit')
    )
        .id('event-form')
        .aria_describedby('form-status'),
    output('The form has not been submitted.').id('form-status').aria_live('polite')
).class_('form-events')))
```

```html
<script>
const eventForm = document.getElementById('event-form');
const formStatus = document.getElementById('form-status');

eventForm.addEventListener('change', event => {
    console.log(`${event.target.name} changed to: ${event.target.value}`);
});

eventForm.addEventListener('submit', event => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.target));
    formStatus.textContent = `Form submitted with: ${JSON.stringify(data)}`;
});
</script>
```

## 事件委托

一个监听器就能处理一组相关联的按钮。这些按钮依然能各自用键盘操作：

```python
from pure.html import button, div, output
from pure.utils import renderHTML

buttons = [
    button('Button {}'.format(i))
        .type('button')
        .data_id(i)
        .class_('delegated-btn')
    for i in range(1, 6)
]

print(renderHTML(div(
    div(*buttons).role('group').aria_label('Delegated buttons'),
    output('Click a button.').id('delegation-output').aria_live('polite')
)
    .id('delegation-container')
    .class_('delegation-container')))
```

```html
<script>
const delegationContainer = document.getElementById('delegation-container');
const delegationOutput = document.getElementById('delegation-output');

delegationContainer.addEventListener('click', event => {
    const selectedButton = event.target.closest('.delegated-btn');

    if (selectedButton && delegationContainer.contains(selectedButton)) {
        delegationOutput.textContent = `Clicked button ${selectedButton.dataset.id}`;
    }
});
</script>
```

当监听器就挂在你真正想读的那个元素上时，用 `event.currentTarget`。
`event.target` 可能是后代元素，做委托时很有用。

## Shape 之间的事件通信

编译后的 shape 可以把可信的展示数据放进属性，同时让 JavaScript 把处理器留在外部：

```python
from pure.compile.Compile import Compile
from pure.core.Slot import Slot
from pure.html import button, div, output, p

child = Compile.shape(
    button(Slot.value('message'))
        .type('button')
        .data_role('child-button')
        .data_message(Slot.value('message'))
)

parent = Compile.shape(
    div(
        p('Parent shape'),
        Slot.raw('child'),
        output('Waiting for the child.').id('parent-output').aria_live('polite')
    )
)

print(parent({'child': child({'message': 'Send from the child'})}))
```

```html
<script>
const childButton = document.querySelector('[data-role="child-button"]');
const parentOutput = document.getElementById('parent-output');

if (childButton) {
    childButton.addEventListener('click', () => {
        parentOutput.textContent = `Received from child: ${childButton.dataset.message}`;
    });
}
</script>
```

这是 shape 的组合，而不是注册过的组件单元。消息作为普通属性数据被转义；没有任何
请求值被插入到 JavaScript 源码里。完整流程见
[编译渲染](/zh/guide/compiled)。

## 自定义浏览器事件

下面的图片使用自包含的 data URI，所以示例不依赖任何占位服务：

```python
from pure.html import button, div, img, output
from pure.utils import renderHTML

print(renderHTML(div(
    img()
        .src('data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==')
        .alt('Embedded placeholder image')
        .width(200)
        .height(100)
        .id('load-image'),
    button('Focus me').type('button').id('focus-button'),
    output('Waiting.').id('custom-status').aria_live('polite')
).class_('custom-events')))
```

```html
<script>
const loadImage = document.getElementById('load-image');
const focusButton = document.getElementById('focus-button');
const customStatus = document.getElementById('custom-status');

function announceImageLoaded() {
    customStatus.textContent = 'Image loaded.';
}

function announceImageError() {
    customStatus.textContent = 'Image failed to load.';
}

loadImage.addEventListener('load', announceImageLoaded);
loadImage.addEventListener('error', announceImageError);
if (loadImage.complete) announceImageLoaded();

focusButton.addEventListener('focus', () => {
    focusButton.style.outline = '2px solid blue';
});

focusButton.addEventListener('blur', () => {
    focusButton.style.outline = '';
});
</script>
```

对于本地资源，请使用稳定的应用路径（例如 `/assets/placeholder.svg`），并让文件与
页面同源。

## 事件处理的最佳实践

### 优先使用 `addEventListener`

先渲染语义化的 HTML，再在同源的 JavaScript 文件里挂上行为。状态文本用
`textContent`，请求数据放在文本或已转义的数据属性里，只在确实需要替换浏览器默认行为
时才调用 `preventDefault()`。

独立的示例把 `<script>` 块内联，这样每个文件都能直接复制运行。生产环境中若启用严格
CSP，应把监听器代码移到外部 `.js` 文件，或用 nonce / hash 授权该脚本。

### CSP 与内联属性

`onclick(...)`、`onsubmit(...)` 这类方法会创建内联的事件处理器属性。不含
`'unsafe-inline'` 的 CSP `script-src` 策略会阻止这些属性。用允许的外部脚本通过
`addEventListener` 挂上的 JavaScript 不属于内联处理器属性，所以应当默认采用它，
不要仅仅为了让 `onclick` 能用就放宽 CSP。

## 下一步

- [HTMX 集成](/zh/guide/htmx) — 把服务端渲染的片段与 HTMX 组合起来
- [组件](/zh/guide/components) — 围绕 shape 组织可复用单元
- [属性与 Slot](/zh/guide/props) — 绑定展示数据而不注入脚本
