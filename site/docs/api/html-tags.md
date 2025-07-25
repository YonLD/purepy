# HTML 标签

Purepy 提供了完整的 HTML5 标签支持。所有标签都可以通过 `pure.html` 模块导入。

## 文档结构标签

### 根元素

```python
from pure.html import html

# HTML 文档根元素
html_doc = html(
    # 文档内容
).lang('zh-CN')
```

### 文档头部

```python
from pure.html import head, title, meta, link, style, script

# 文档头部
head_section = head(
    meta().charset('UTF-8'),
    meta().name('viewport').content('width=device-width, initial-scale=1.0'),
    title('页面标题'),
    link().rel('stylesheet').href('styles.css'),
    style('body { margin: 0; }'),
    script().src('script.js')
)
```

### 文档主体

```python
from pure.html import body

# 文档主体
body_section = body(
    # 页面内容
).class_name('main-body')
```

## 内容分区标签

### 语义化容器

```python
from pure.html import header, nav, main, section, article, aside, footer

# 页面头部
page_header = header(
    nav(
        # 导航内容
    )
).class_name('page-header')

# 主要内容
main_content = main(
    section(
        article(
            # 文章内容
        )
    ),
    aside(
        # 侧边栏内容
    )
)

# 页面底部
page_footer = footer(
    # 底部内容
).class_name('page-footer')
```

### 通用容器

```python
from pure.html import div, span

# 块级容器
container = div(
    # 内容
).class_name('container')

# 内联容器
inline_container = span('内联内容').class_name('highlight')
```

## 文本内容标签

### 标题

```python
from pure.html import h1, h2, h3, h4, h5, h6

# 各级标题
h1('一级标题').class_name('main-title')
h2('二级标题').class_name('section-title')
h3('三级标题')
h4('四级标题')
h5('五级标题')
h6('六级标题')
```

### 段落和文本

```python
from pure.html import p, br, hr

# 段落
paragraph = p('这是一个段落。').class_name('content-paragraph')

# 换行
line_break = br()

# 水平分割线
horizontal_rule = hr().class_name('section-divider')
```

### 文本格式化

```python
from pure.html import strong, em, mark, small, del_, ins, sub, sup

# 强调文本
strong_text = strong('重要文本')
emphasized_text = em('强调文本')

# 标记文本
marked_text = mark('高亮文本')

# 小号文本
small_text = small('小号文本')

# 删除和插入
deleted_text = del_('删除的文本')
inserted_text = ins('插入的文本')

# 上标和下标
superscript = sup('上标')
subscript = sub('下标')
```

### 引用

```python
from pure.html import blockquote, q, cite

# 块引用
block_quote = blockquote(
    p('这是一个块引用。'),
    cite('引用来源')
).class_name('quote')

# 内联引用
inline_quote = q('这是一个内联引用')
```

### 代码

```python
from pure.html import code, pre, kbd, samp, var

# 内联代码
inline_code = code('print("Hello World")')

# 代码块
code_block = pre(
    code('def hello():\n    print("Hello World")')
).class_name('code-block')

# 键盘输入
keyboard_input = kbd('Ctrl+C')

# 示例输出
sample_output = samp('Hello World')

# 变量
variable = var('x')
```

## 列表标签

### 无序列表

```python
from pure.html import ul, li

# 无序列表
unordered_list = ul(
    li('项目 1'),
    li('项目 2'),
    li('项目 3')
).class_name('menu-list')
```

### 有序列表

```python
from pure.html import ol

# 有序列表
ordered_list = ol(
    li('第一步'),
    li('第二步'),
    li('第三步')
).type('1').start('1')
```

### 描述列表

```python
from pure.html import dl, dt, dd

# 描述列表
description_list = dl(
    dt('术语 1'),
    dd('术语 1 的描述'),
    dt('术语 2'),
    dd('术语 2 的描述')
)
```

## 链接和媒体标签

### 链接

```python
from pure.html import a

# 基本链接
basic_link = a('链接文本').href('https://example.com')

# 带目标的链接
external_link = a('外部链接').href('https://example.com').target('_blank').rel('noopener')

# 邮件链接
email_link = a('发送邮件').href('mailto:example@example.com')

# 电话链接
phone_link = a('拨打电话').href('tel:+1234567890')
```

### 图片

```python
from pure.html import img, figure, figcaption

# 基本图片
basic_image = img().src('image.jpg').alt('图片描述').width('300').height('200')

# 响应式图片
responsive_image = img().src('image.jpg').alt('图片描述').class_name('responsive-img')

# 带说明的图片
figure_with_caption = figure(
    img().src('image.jpg').alt('图片描述'),
    figcaption('图片说明')
)
```

### 音频和视频

```python
from pure.html import audio, video, source, track

# 音频
audio_element = audio(
    source().src('audio.mp3').type('audio/mpeg'),
    source().src('audio.ogg').type('audio/ogg')
).controls(True).preload('metadata')

# 视频
video_element = video(
    source().src('video.mp4').type('video/mp4'),
    source().src('video.webm').type('video/webm'),
    track().src('subtitles.vtt').kind('subtitles').srclang('zh').label('中文字幕')
).controls(True).width('640').height('360').poster('poster.jpg')
```

## 表格标签

### 基本表格

```python
from pure.html import table, thead, tbody, tfoot, tr, th, td, caption

# 完整表格
complete_table = table(
    caption('表格标题'),
    thead(
        tr(
            th('列 1'),
            th('列 2'),
            th('列 3')
        )
    ),
    tbody(
        tr(
            td('数据 1'),
            td('数据 2'),
            td('数据 3')
        ),
        tr(
            td('数据 4'),
            td('数据 5'),
            td('数据 6')
        )
    ),
    tfoot(
        tr(
            td('总计').colspan('2'),
            td('合计值')
        )
    )
).class_name('data-table')
```

### 表格分组

```python
from pure.html import colgroup, col

# 列分组
table_with_colgroup = table(
    colgroup(
        col().span('2').class_name('group1'),
        col().class_name('group2')
    ),
    # 表格内容...
)
```

## 表单标签

### 表单容器

```python
from pure.html import form, fieldset, legend

# 基本表单
basic_form = form(
    fieldset(
        legend('用户信息'),
        # 表单字段...
    )
).action('/submit').method('post').enctype('multipart/form-data')
```

### 输入字段

```python
from pure.html import input, textarea, select, option, optgroup

# 文本输入
text_input = input().type('text').name('username').placeholder('用户名').required(True)

# 密码输入
password_input = input().type('password').name('password').placeholder('密码').required(True)

# 邮箱输入
email_input = input().type('email').name('email').placeholder('邮箱地址')

# 数字输入
number_input = input().type('number').name('age').min('18').max('100').step('1')

# 日期输入
date_input = input().type('date').name('birthday')

# 文件上传
file_input = input().type('file').name('avatar').accept('image/*')

# 多行文本
textarea_input = textarea('默认内容').name('description').rows('5').cols('50')

# 下拉选择
select_input = select(
    optgroup(
        option('选项 1').value('1'),
        option('选项 2').value('2').selected(True)
    ).label('分组 1'),
    optgroup(
        option('选项 3').value('3'),
        option('选项 4').value('4')
    ).label('分组 2')
).name('category')
```

### 按钮

```python
from pure.html import button

# 提交按钮
submit_button = button('提交').type('submit').class_name('btn btn-primary')

# 重置按钮
reset_button = button('重置').type('reset').class_name('btn btn-secondary')

# 普通按钮
normal_button = button('点击').type('button').onclick('handleClick()').class_name('btn')
```

### 标签

```python
from pure.html import label

# 表单标签
form_label = label('用户名').for_('username')

# 包含输入的标签
label_with_input = label(
    '同意条款',
    input().type('checkbox').name('agree').value('1')
)
```

## 交互元素

### 详情和摘要

```python
from pure.html import details, summary

# 可折叠内容
collapsible_content = details(
    summary('点击展开'),
    p('这是隐藏的内容。'),
    p('可以包含任何元素。')
).open(False)
```

### 对话框

```python
from pure.html import dialog

# 对话框
modal_dialog = dialog(
    h2('对话框标题'),
    p('对话框内容'),
    button('关闭').onclick('this.closest("dialog").close()')
).id('modal')
```

## 嵌入内容

### 内联框架

```python
from pure.html import iframe

# 嵌入页面
embedded_page = iframe().src('https://example.com').width('800').height('600').title('嵌入页面')
```

### 对象和嵌入

```python
from pure.html import object_, embed, param

# 嵌入对象
embedded_object = object_(
    param().name('movie').value('movie.swf'),
    param().name('quality').value('high')
).data('movie.swf').type('application/x-shockwave-flash')

# 直接嵌入
direct_embed = embed().src('movie.swf').type('application/x-shockwave-flash').width('400').height('300')
```

## 脚本和样式

### 脚本

```python
from pure.html import script, noscript

# 外部脚本
external_script = script().src('script.js').defer(True)

# 内联脚本
inline_script = script('console.log("Hello World");')

# 无脚本回退
no_script_fallback = noscript(
    p('请启用 JavaScript 以获得最佳体验。')
)
```

### 样式

```python
from pure.html import style, link

# 内联样式
inline_style = style('''
    body { margin: 0; padding: 0; }
    .container { max-width: 1200px; margin: 0 auto; }
''')

# 外部样式表
external_style = link().rel('stylesheet').href('styles.css')
```

## 元数据

```python
from pure.html import meta, base

# 字符编码
charset_meta = meta().charset('UTF-8')

# 视口设置
viewport_meta = meta().name('viewport').content('width=device-width, initial-scale=1.0')

# SEO 元数据
description_meta = meta().name('description').content('页面描述')
keywords_meta = meta().name('keywords').content('关键词1, 关键词2')

# Open Graph
og_title = meta().property('og:title').content('页面标题')
og_description = meta().property('og:description').content('页面描述')

# 基础 URL
base_url = base().href('https://example.com/')
```

## 下一步

- [SVG 标签](/api/svg-tags) - 了解 SVG 图形元素
- [核心类](/api/core) - 了解核心类的详细功能
- [基本用法](/guide/basic-usage) - 学习如何使用这些标签
