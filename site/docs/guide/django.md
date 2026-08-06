# Django 集成

Purepy 可以与 Django 框架无缝集成，作为传统 Django 模板的替代方案，提供更强大的组件化开发体验。

## 为什么选择这个组合？

- **Purepy**: 提供组件化的 Python 模板渲染
- **Django**: 提供完整的 Web 框架和 ORM
- **完美互补**: Purepy 处理视图层，Django 处理模型、路由和业务逻辑

## 快速开始

### 1. 安装依赖

```bash
pip install django yonld-purepy
```

### 2. 创建 Django 项目

```bash
django-admin startproject myproject
cd myproject
python manage.py startapp myapp
```

### 3. 基本集成

```python
# myapp/views.py
from django.http import HttpResponse
from pure.html import html, head, title, body, div, h1, p, a

def Layout(props):
    page_title = props.get('title', 'Purepy + Django')
    content = props.get('content', '')
    
    return html(
        head(
            title(page_title)
        ),
        body(
            div(
                content
            ).class_name('container')
        )
    )

def index(request):
    content = div(
        h1('欢迎使用 Purepy + Django'),
        p('这是一个使用 Purepy 和 Django 构建的应用'),
        a('了解更多').href('/about/')
    )
    
    page = Layout({
        'title': '首页',
        'content': content
    })
    
    return HttpResponse(str(page))

def about(request):
    content = div(
        h1('关于我们'),
        p('Purepy 是一个受 ReactJS 启发的 Python 模板引擎。')
    )
    
    page = Layout({
        'title': '关于我们',
        'content': content
    })
    
    return HttpResponse(str(page))
```

```python
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]
```

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```

## 与 Django 模型集成

### 1. 模型定义

```python
# myapp/models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### 2. 组件化视图

```python
# myapp/components.py
from pure.html import html, head, title, body, div, h1, h2, h3, p, a, article, time, ul, li

def Layout(props):
    page_title = props.get('title', 'Django + Purepy Blog')
    content = props.get('content', '')
    
    return html(
        head(
            title(page_title),
            # 添加 Bootstrap CSS
            link().rel('stylesheet').href('https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css')
        ),
        body(
            div(
                content
            ).class_name('container mt-4')
        )
    )

def PostCard(post):
    return article(
        h2(
            a(post.title).href(f'/post/{post.id}/')
        ),
        p(post.content[:200] + '...' if len(post.content) > 200 else post.content),
        p(
            time(post.created_at.strftime('%Y-%m-%d %H:%M')).class_name('text-muted')
        )
    ).class_name('card mb-3 p-3')

def PostList(posts):
    return div(
        h1('博客文章'),
        div(
            *[PostCard(post) for post in posts]
        ) if posts else p('暂无文章')
    )

def PostDetail(post, comments):
    return div(
        article(
            h1(post.title),
            p(post.content),
            p(
                time(post.created_at.strftime('%Y-%m-%d %H:%M')).class_name('text-muted')
            )
        ),
        div(
            h3('评论'),
            ul(
                *[li(
                    div(
                        h4(comment.author),
                        p(comment.content),
                        p(
                            time(comment.created_at.strftime('%Y-%m-%d %H:%M')).class_name('text-muted')
                        )
                    )
                ) for comment in comments]
            ) if comments else p('暂无评论')
        ).class_name('mt-4')
    )
```

### 3. 视图函数

```python
# myapp/views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .components import Layout, PostList, PostDetail

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    
    content = PostList(posts)
    
    page = Layout({
        'title': '博客首页',
        'content': content
    })
    
    return HttpResponse(str(page))

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')
    
    content = PostDetail(post, comments)
    
    page = Layout({
        'title': post.title,
        'content': content
    })
    
    return HttpResponse(str(page))
```

## 表单处理

### 1. Django 表单

```python
# myapp/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']
```

### 2. Purepy 表单组件

```python
# myapp/components.py
from pure.html import form, div, label, input, textarea, button

def CommentFormComponent(form_data=None, errors=None):
    return form(
        div(
            label('作者').for_('id_author'),
            input()
                .type('text')
                .name('author')
                .id('id_author')
                .class_name('form-control')
                .value(form_data.get('author', '') if form_data else '')
                .required(),
            div(errors.get('author', '') if errors else '').class_name('text-danger')
        ).class_name('mb-3'),
        div(
            label('评论内容').for_('id_content'),
            textarea(form_data.get('content', '') if form_data else '')
                .name('content')
                .id('id_content')
                .class_name('form-control')
                .rows('4')
                .required(),
            div(errors.get('content', '') if errors else '').class_name('text-danger')
        ).class_name('mb-3'),
        button('提交评论').type('submit').class_name('btn btn-primary')
    ).method('POST')
```

### 3. 表单处理视图

```python
# myapp/views.py
from django.shortcuts import redirect
from .forms import CommentForm

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
        else:
            # 显示表单错误
            content = div(
                PostDetail(post, post.comment_set.all()),
                h3('添加评论'),
                CommentFormComponent(
                    form_data=request.POST,
                    errors=form.errors
                )
            )
    else:
        content = div(
            PostDetail(post, post.comment_set.all()),
            h3('添加评论'),
            CommentFormComponent()
        )
    
    page = Layout({
        'title': f'评论 - {post.title}',
        'content': content
    })
    
    return HttpResponse(str(page))
```

## 中间件集成

### 1. 自定义中间件

```python
# myapp/middleware.py
from django.utils.deprecation import MiddlewareMixin
from pure.html import div, p

class PurepyErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if settings.DEBUG:
            return None  # 让 Django 处理调试模式下的异常
        
        # 生产环境下使用 Purepy 渲染错误页面
        from .components import Layout
        
        content = div(
            h1('服务器错误'),
            p('抱歉，服务器遇到了一个错误。请稍后再试。')
        )
        
        page = Layout({
            'title': '服务器错误',
            'content': content
        })
        
        return HttpResponse(str(page), status=500)
```

## 管理命令

### 1. 生成静态页面

```python
# myapp/management/commands/generate_static.py
from django.core.management.base import BaseCommand
from django.conf import settings
import os
from myapp.models import Post
from myapp.components import Layout, PostDetail

class Command(BaseCommand):
    help = '生成静态 HTML 页面'
    
    def handle(self, *args, **options):
        static_dir = os.path.join(settings.BASE_DIR, 'static_pages')
        os.makedirs(static_dir, exist_ok=True)
        
        posts = Post.objects.all()
        
        for post in posts:
            content = PostDetail(post, post.comment_set.all())
            page = Layout({
                'title': post.title,
                'content': content
            })
            
            filename = f'post_{post.id}.html'
            filepath = os.path.join(static_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(page))
            
            self.stdout.write(
                self.style.SUCCESS(f'生成页面: {filename}')
            )
```

## 最佳实践

### 1. 组件组织

```python
# myapp/
#   components/
#     __init__.py
#     layout.py
#     blog.py
#     forms.py
#   views/
#     __init__.py
#     blog.py
#     api.py
```

### 2. 缓存优化

```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 缓存 15 分钟
def cached_post_list(request):
    # 视图实现
    pass

def get_cached_component(cache_key, component_func, *args, **kwargs):
    cached_html = cache.get(cache_key)
    if cached_html is None:
        component = component_func(*args, **kwargs)
        cached_html = str(component)
        cache.set(cache_key, cached_html, 60 * 30)  # 缓存 30 分钟
    return cached_html
```

### 3. 国际化支持

```python
from django.utils.translation import gettext as _

def MultilingualComponent(props):
    return div(
        h1(_(props.get('title', 'Default Title'))),
        p(_(props.get('content', 'Default content')))
    )
```

## 下一步

- [Flask 集成](/guide/flask) - 了解如何与 Flask 配合使用
- [组件](/guide/components) - 深入学习组件开发
- [API 文档](/api/) - 查看完整的 API 参考
