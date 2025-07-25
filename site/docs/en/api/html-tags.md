# HTML Tags

Purepy provides complete HTML5 tag support. All tags can be imported from the `pure.html` module.

## Document Structure Tags

### Root Element

```python
from pure.html import html

# HTML document root element
html_doc = html(
    # Document content
).lang('en')
```

### Document Head

```python
from pure.html import head, title, meta, link, style, script

# Document head
head_section = head(
    meta().charset('UTF-8'),
    meta().name('viewport').content('width=device-width, initial-scale=1.0'),
    title('Page Title'),
    link().rel('stylesheet').href('styles.css'),
    style('body { margin: 0; }'),
    script().src('script.js')
)
```

### Document Body

```python
from pure.html import body

# Document body
body_section = body(
    # Page content
).class_name('main-body')
```

## Content Sectioning Tags

### Semantic Containers

```python
from pure.html import header, nav, main, section, article, aside, footer

# Page header
page_header = header(
    nav(
        # Navigation content
    )
).class_name('page-header')

# Main content
main_content = main(
    section(
        article(
            # Article content
        )
    ),
    aside(
        # Sidebar content
    )
)

# Page footer
page_footer = footer(
    # Footer content
).class_name('page-footer')
```

### Generic Containers

```python
from pure.html import div, span

# Block container
container = div(
    # Content
).class_name('container')

# Inline container
inline_container = span('Inline content').class_name('highlight')
```

## Text Content Tags

### Headings

```python
from pure.html import h1, h2, h3, h4, h5, h6

# Various heading levels
h1('Main Title').class_name('main-title')
h2('Section Title').class_name('section-title')
h3('Subsection Title')
h4('Fourth Level Title')
h5('Fifth Level Title')
h6('Sixth Level Title')
```

### Paragraphs and Text

```python
from pure.html import p, br, hr

# Paragraph
paragraph = p('This is a paragraph.').class_name('content-paragraph')

# Line break
line_break = br()

# Horizontal rule
horizontal_rule = hr().class_name('section-divider')
```

### Text Formatting

```python
from pure.html import strong, em, mark, small, Del, ins, sub, sup

# Emphasized text
strong_text = strong('Important text')
emphasized_text = em('Emphasized text')

# Marked text
marked_text = mark('Highlighted text')

# Small text
small_text = small('Small text')

# Deleted and inserted
deleted_text = Del('Deleted text')
inserted_text = ins('Inserted text')

# Superscript and subscript
superscript = sup('Superscript')
subscript = sub('Subscript')
```

### Quotes

```python
from pure.html import blockquote, q, cite

# Block quote
block_quote = blockquote(
    p('This is a block quote.'),
    cite('Quote source')
).class_name('quote')

# Inline quote
inline_quote = q('This is an inline quote')
```

### Code

```python
from pure.html import code, pre, kbd, samp, var

# Inline code
inline_code = code('print("Hello World")')

# Code block
code_block = pre(
    code('def hello():\n    print("Hello World")')
).class_name('code-block')

# Keyboard input
keyboard_input = kbd('Ctrl+C')

# Sample output
sample_output = samp('Hello World')

# Variable
variable = var('x')
```

## List Tags

### Unordered Lists

```python
from pure.html import ul, li

# Unordered list
unordered_list = ul(
    li('Item 1'),
    li('Item 2'),
    li('Item 3')
).class_name('menu-list')
```

### Ordered Lists

```python
from pure.html import ol

# Ordered list
ordered_list = ol(
    li('First step'),
    li('Second step'),
    li('Third step')
).type('1').start('1')
```

### Description Lists

```python
from pure.html import dl, dt, dd

# Description list
description_list = dl(
    dt('Term 1'),
    dd('Description of term 1'),
    dt('Term 2'),
    dd('Description of term 2')
)
```

## Link and Media Tags

### Links

```python
from pure.html import a

# Basic link
basic_link = a('Link text').href('https://example.com')

# Link with target
external_link = a('External link').href('https://example.com').target('_blank').rel('noopener')

# Email link
email_link = a('Send email').href('mailto:example@example.com')

# Phone link
phone_link = a('Call phone').href('tel:+1234567890')
```

### Images

```python
from pure.html import img, figure, figcaption

# Basic image
basic_image = img().src('image.jpg').alt('Image description').width('300').height('200')

# Responsive image
responsive_image = img().src('image.jpg').alt('Image description').class_name('responsive-img')

# Image with caption
figure_with_caption = figure(
    img().src('image.jpg').alt('Image description'),
    figcaption('Image caption')
)
```

### Audio and Video

```python
from pure.html import audio, video, source, track

# Audio
audio_element = audio(
    source().src('audio.mp3').type('audio/mpeg'),
    source().src('audio.ogg').type('audio/ogg')
).controls(True).preload('metadata')

# Video
video_element = video(
    source().src('video.mp4').type('video/mp4'),
    source().src('video.webm').type('video/webm'),
    track().src('subtitles.vtt').kind('subtitles').srclang('en').label('English subtitles')
).controls(True).width('640').height('360').poster('poster.jpg')
```

## Table Tags

### Basic Table

```python
from pure.html import table, thead, tbody, tfoot, tr, th, td, caption

# Complete table
complete_table = table(
    caption('Table title'),
    thead(
        tr(
            th('Column 1'),
            th('Column 2'),
            th('Column 3')
        )
    ),
    tbody(
        tr(
            td('Data 1'),
            td('Data 2'),
            td('Data 3')
        ),
        tr(
            td('Data 4'),
            td('Data 5'),
            td('Data 6')
        )
    ),
    tfoot(
        tr(
            td('Total').colspan('2'),
            td('Sum value')
        )
    )
).class_name('data-table')
```

### Table Grouping

```python
from pure.html import colgroup, col

# Column grouping
table_with_colgroup = table(
    colgroup(
        col().span('2').class_name('group1'),
        col().class_name('group2')
    ),
    # Table content...
)
```

## Form Tags

### Form Container

```python
from pure.html import form, fieldset, legend

# Basic form
basic_form = form(
    fieldset(
        legend('User Information'),
        # Form fields...
    )
).action('/submit').method('post').enctype('multipart/form-data')
```

### Input Fields

```python
from pure.html import input, textarea, select, option, optgroup

# Text input
text_input = input().type('text').name('username').placeholder('Username').required(True)

# Password input
password_input = input().type('password').name('password').placeholder('Password').required(True)

# Email input
email_input = input().type('email').name('email').placeholder('Email address')

# Number input
number_input = input().type('number').name('age').min('18').max('100').step('1')

# Date input
date_input = input().type('date').name('birthday')

# File upload
file_input = input().type('file').name('avatar').accept('image/*')

# Textarea
textarea_input = textarea('Default content').name('description').rows('5').cols('50')

# Select dropdown
select_input = select(
    optgroup(
        option('Option 1').value('1'),
        option('Option 2').value('2').selected(True)
    ).label('Group 1'),
    optgroup(
        option('Option 3').value('3'),
        option('Option 4').value('4')
    ).label('Group 2')
).name('category')
```

### Buttons

```python
from pure.html import button

# Submit button
submit_button = button('Submit').type('submit').class_name('btn btn-primary')

# Reset button
reset_button = button('Reset').type('reset').class_name('btn btn-secondary')

# Normal button
normal_button = button('Click').type('button').onclick('handleClick()').class_name('btn')
```

### Labels

```python
from pure.html import label

# Form label (use htmlFor since 'for' is a Python keyword)
form_label = label('Username').htmlFor('username')

# Label with input
label_with_input = label(
    'Agree to terms',
    input().type('checkbox').name('agree').value('1')
)
```

## Interactive Elements

### Details and Summary

```python
from pure.html import details, summary

# Collapsible content
collapsible_content = details(
    summary('Click to expand'),
    p('This is hidden content.'),
    p('Can contain any elements.')
).open(False)
```

### Dialog

```python
from pure.html import dialog

# Modal dialog
modal_dialog = dialog(
    h2('Dialog Title'),
    p('Dialog content'),
    button('Close').onclick('this.closest("dialog").close()')
).id('modal')
```

## Embedded Content

### Inline Frame

```python
from pure.html import iframe

# Embedded page
embedded_page = iframe().src('https://example.com').width('800').height('600').title('Embedded page')
```

### Object and Embed

```python
from pure.html import object, embed, param

# Embedded object
embedded_object = object(
    param().name('movie').value('movie.swf'),
    param().name('quality').value('high')
).data('movie.swf').type('application/x-shockwave-flash')

# Direct embed
direct_embed = embed().src('movie.swf').type('application/x-shockwave-flash').width('400').height('300')
```

## Script and Style

### Scripts

```python
from pure.html import script, noscript

# External script
external_script = script().src('script.js').defer(True)

# Inline script
inline_script = script('console.log("Hello World");')

# No script fallback
no_script_fallback = noscript(
    p('Please enable JavaScript for the best experience.')
)
```

### Styles

```python
from pure.html import style, link

# Inline style
inline_style = style('''
    body { margin: 0; padding: 0; }
    .container { max-width: 1200px; margin: 0 auto; }
''')

# External stylesheet
external_style = link().rel('stylesheet').href('styles.css')
```

## Metadata

```python
from pure.html import meta, base

# Character encoding
charset_meta = meta().charset('UTF-8')

# Viewport settings
viewport_meta = meta().name('viewport').content('width=device-width, initial-scale=1.0')

# SEO metadata
description_meta = meta().name('description').content('Page description')
keywords_meta = meta().name('keywords').content('keyword1, keyword2')

# Open Graph
og_title = meta().property('og:title').content('Page title')
og_description = meta().property('og:description').content('Page description')

# Base URL
base_url = base().href('https://example.com/')
```

## Next Steps

- [SVG Tags](/en/api/svg-tags) - Learn about SVG graphic elements
- [Core Classes](/en/api/core) - Learn about core class functionality
- [Basic Usage](/en/guide/basic-usage) - Learn how to use these tags
