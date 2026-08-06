# Django Integration

Purepy integrates seamlessly with the Django framework as an alternative to traditional Django templates, providing a more powerful component-based development experience.

## Why Choose This Combination?

- **Purepy**: Provides component-based Python template rendering
- **Django**: Provides complete web framework and ORM
- **Perfect Complement**: Purepy handles the view layer, Django handles models, routing, and business logic

## Quick Start

### 1. Install Dependencies

```bash
pip install django yonld-purepy
```

### 2. Create Django Project

```bash
django-admin startproject myproject
cd myproject
python manage.py startapp myapp
```

### 3. Basic Integration

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
        h1('Welcome to Purepy + Django'),
        p('This is an application built with Purepy and Django'),
        a('Learn more').href('/about/')
    )
    
    page = Layout({
        'title': 'Home',
        'content': content
    })
    
    return HttpResponse(str(page))

def about(request):
    content = div(
        h1('About Us'),
        p('Purepy is a Python template engine inspired by ReactJS.')
    )
    
    page = Layout({
        'title': 'About Us',
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

## Django Model Integration

### 1. Model Definition

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

### 2. Component-Based Views

```python
# myapp/components.py
from pure.html import html, head, title, body, div, h1, h2, h3, p, a, article, time, ul, li, link

def Layout(props):
    page_title = props.get('title', 'Django + Purepy Blog')
    content = props.get('content', '')
    
    return html(
        head(
            title(page_title),
            # Add Bootstrap CSS
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
        h1('Blog Posts'),
        div(
            *[PostCard(post) for post in posts]
        ) if posts else p('No posts available')
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
            h3('Comments'),
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
            ) if comments else p('No comments yet')
        ).class_name('mt-4')
    )
```

### 3. View Functions

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
        'title': 'Blog Home',
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

## Form Handling

### 1. Django Forms

```python
# myapp/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']
```

### 2. Purepy Form Components

```python
# myapp/components.py
from pure.html import form, div, label, input, textarea, button

def CommentFormComponent(form_data=None, errors=None):
    return form(
        div(
            label('Author').for_('id_author'),
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
            label('Comment Content').for_('id_content'),
            textarea(form_data.get('content', '') if form_data else '')
                .name('content')
                .id('id_content')
                .class_name('form-control')
                .rows('4')
                .required(),
            div(errors.get('content', '') if errors else '').class_name('text-danger')
        ).class_name('mb-3'),
        button('Submit Comment').type('submit').class_name('btn btn-primary')
    ).method('POST')
```

### 3. Form Handling Views

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
            # Display form errors
            content = div(
                PostDetail(post, post.comment_set.all()),
                h3('Add Comment'),
                CommentFormComponent(
                    form_data=request.POST,
                    errors=form.errors
                )
            )
    else:
        content = div(
            PostDetail(post, post.comment_set.all()),
            h3('Add Comment'),
            CommentFormComponent()
        )
    
    page = Layout({
        'title': f'Comment - {post.title}',
        'content': content
    })
    
    return HttpResponse(str(page))
```

## Middleware Integration

### 1. Custom Middleware

```python
# myapp/middleware.py
from django.utils.deprecation import MiddlewareMixin
from pure.html import div, h1, p

class PurepyErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if settings.DEBUG:
            return None  # Let Django handle exceptions in debug mode
        
        # Use Purepy to render error pages in production
        from .components import Layout
        
        content = div(
            h1('Server Error'),
            p('Sorry, the server encountered an error. Please try again later.')
        )
        
        page = Layout({
            'title': 'Server Error',
            'content': content
        })
        
        return HttpResponse(str(page), status=500)
```

## Management Commands

### 1. Generate Static Pages

```python
# myapp/management/commands/generate_static.py
from django.core.management.base import BaseCommand
from django.conf import settings
import os
from myapp.models import Post
from myapp.components import Layout, PostDetail

class Command(BaseCommand):
    help = 'Generate static HTML pages'
    
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
                self.style.SUCCESS(f'Generated page: {filename}')
            )
```

## Best Practices

### 1. Component Organization

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

### 2. Caching Optimization

```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def cached_post_list(request):
    # View implementation
    pass

def get_cached_component(cache_key, component_func, *args, **kwargs):
    cached_html = cache.get(cache_key)
    if cached_html is None:
        component = component_func(*args, **kwargs)
        cached_html = str(component)
        cache.set(cache_key, cached_html, 60 * 30)  # Cache for 30 minutes
    return cached_html
```

### 3. Internationalization Support

```python
from django.utils.translation import gettext as _

def MultilingualComponent(props):
    return div(
        h1(_(props.get('title', 'Default Title'))),
        p(_(props.get('content', 'Default content')))
    )
```

## Next Steps

- [Flask Integration](/en/guide/flask) - Learn how to work with Flask
- [Components](/en/guide/components) - Deep dive into component development
- [API Documentation](/en/api/) - View complete API reference
