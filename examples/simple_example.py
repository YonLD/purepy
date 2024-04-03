#!/usr/bin/env python3
"""
Simple example demonstrating Purepy usage.

This example shows how to create HTML content using Purepy
in a way similar to React functional components.
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import pure
sys.path.insert(0, str(Path(__file__).parent.parent))

from pure.html import html, head, meta, title, body, div, h1, h2, p, a, ul, li, nav, footer
from pure.svg import svg, circle, rect
from pure.clx import clx
from pure.sty import sty

def Header(props):
    """Header component."""
    site_name = props.get('site_name', 'My Site')
    navigation = props.get('navigation', [])
    
    return div(
        h1(site_name).class_name('site-title'),
        nav(
            ul(
                *[li(a(item['text']).href(item['url'])) for item in navigation]
            ).class_name('nav-list')
        ).class_name('navigation')
    ).class_name('header')

def Card(props):
    """Card component."""
    title = props.get('title', '')
    content = props.get('content', '')
    link = props.get('link', '#')
    
    return div(
        h2(title).class_name('card-title'),
        p(content).class_name('card-content'),
        a('Read more').href(link).class_name('card-link')
    ).class_name('card')

def Icon(props):
    """Simple SVG icon component."""
    size = props.get('size', 24)
    color = props.get('color', 'currentColor')
    
    return svg(
        circle().cx(12).cy(12).r(10).fill(color)
    ).width(size).height(size).class_name('icon')

def Footer(props):
    """Footer component."""
    copyright = props.get('copyright', '© 2024')
    
    return footer(
        p(copyright).class_name('copyright')
    ).class_name('footer')

def Page(props):
    """Main page component."""
    title = props.get('title', 'Purepy Example')
    
    # Sample data
    navigation = [
        {'text': 'Home', 'url': '/'},
        {'text': 'About', 'url': '/about'},
        {'text': 'Contact', 'url': '/contact'}
    ]
    
    cards_data = [
        {
            'title': 'Welcome to Purepy',
            'content': 'Purepy is a Python templating engine inspired by React.',
            'link': 'https://github.com/YonLD/purepy'
        },
        {
            'title': 'Pure Python',
            'content': 'Write your templates using pure Python code.',
            'link': '#'
        },
        {
            'title': 'Component-based',
            'content': 'Create reusable components just like in React.',
            'link': '#'
        }
    ]
    
    return html(
        head(
            meta().charset('UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1.0'),
            title(title),
            # Add some basic styles
            style("""
                body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
                .header { background: #333; color: white; padding: 1rem; }
                .site-title { margin: 0; }
                .navigation { margin-top: 1rem; }
                .nav-list { list-style: none; padding: 0; display: flex; gap: 1rem; }
                .nav-list a { color: white; text-decoration: none; }
                .main { padding: 2rem; }
                .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
                .card { border: 1px solid #ddd; padding: 1rem; border-radius: 8px; }
                .card-title { margin-top: 0; }
                .card-link { color: #007bff; text-decoration: none; }
                .footer { background: #f8f9fa; padding: 1rem; text-align: center; margin-top: 2rem; }
            """)
        ),
        body(
            Header({
                'site_name': 'Purepy Demo',
                'navigation': navigation
            }),
            div(
                h1('Welcome to Purepy'),
                p('This is a simple example showing how to use Purepy to create HTML content.'),
                
                div(
                    *[Card(card_data) for card_data in cards_data]
                ).class_name('cards'),
                
                div(
                    h2('SVG Icon Example'),
                    p('Here\'s a simple SVG icon: ', Icon({'size': 32, 'color': '#007bff'}))
                )
            ).class_name('main'),
            
            Footer({
                'copyright': '© 2024 Purepy Example'
            })
        )
    )

def main():
    """Main function to generate and display the HTML."""
    page = Page({'title': 'Purepy Simple Example'})
    
    # Print the HTML
    print(page)
    
    # Optionally save to file
    with open('simple_example.html', 'w', encoding='utf-8') as f:
        f.write(str(page))
    
    print("\nHTML saved to simple_example.html")

if __name__ == '__main__':
    main()
