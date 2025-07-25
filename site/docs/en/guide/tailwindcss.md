# TailwindCSS Integration

This guide shows how to integrate and use TailwindCSS with Purepy projects.

## What is TailwindCSS?

TailwindCSS is a utility-first CSS framework that provides a comprehensive set of utility classes to rapidly build modern user interfaces.

## Installing TailwindCSS

### 1. Using CDN (Quick Start)

The simplest way is to include TailwindCSS via CDN:

```python
from pure.html import html, head, meta, title, link, body, div, h1, p

def create_page():
    return html(
        head(
            meta().charset('UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1.0'),
            title('Purepy + TailwindCSS'),
            # Include TailwindCSS CDN
            link().href('https://cdn.tailwindcss.com').rel('stylesheet')
        ),
        body(
            div(
                h1('Welcome to Purepy + TailwindCSS').class_name('text-4xl font-bold text-blue-600 mb-4'),
                p('This is a paragraph styled with TailwindCSS.').class_name('text-gray-700 text-lg')
            ).class_name('container mx-auto p-8')
        )
    )

# Generate page
page = create_page()
page.to_save('index.html')
```

### 2. Local Installation (Recommended for Production)

For production environments, local installation is recommended:

```bash
# Install Node.js and npm (if not already installed)
npm init -y
npm install -D tailwindcss
npx tailwindcss init
```

Configure `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./output/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Create CSS file `src/input.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Build CSS:

```bash
npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch
```

## Using TailwindCSS with Purepy

### 1. Basic Styling

```python
from pure.html import div, h1, p, button

def styled_card(props):
    title = props.get('title', '')
    content = props.get('content', '')

    return div(
        div(
            h1(title).class_name('text-2xl font-bold text-gray-900 mb-4'),
            p(content).class_name('text-gray-600 mb-6'),
            button('Learn More').class_name(
                'bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
            )
        ).class_name('p-6')
    ).class_name('max-w-sm mx-auto bg-white rounded-xl shadow-md overflow-hidden')

# Use component
card = styled_card({
    'title': 'Card Title',
    'content': 'This is the card content description.'
})
card.to_print()
```

### 2. Responsive Design

```python
from pure.html import div, h1, p, button

def responsive_hero():
    return div(
        div(
            h1('Responsive Title').class_name(
                'text-4xl md:text-6xl font-bold text-white mb-4'
            ),
            p('This is a responsive hero section').class_name(
                'text-xl md:text-2xl text-gray-200 mb-8'
            ),
            button('Get Started').class_name(
                'bg-white text-blue-600 font-bold py-3 px-6 rounded-lg hover:bg-gray-100 transition duration-300'
            )
        ).class_name('text-center')
    ).class_name(
        'bg-gradient-to-r from-blue-500 to-purple-600 min-h-screen flex items-center justify-center px-4'
    )

hero = responsive_hero()
hero.to_print()
```

### 3. Grid Layout

```python
from pure.html import div, h2, p

def grid_layout():
    items = [
        {'title': 'Feature 1', 'desc': 'Description 1'},
        {'title': 'Feature 2', 'desc': 'Description 2'},
        {'title': 'Feature 3', 'desc': 'Description 3'},
        {'title': 'Feature 4', 'desc': 'Description 4'},
    ]

    return div(
        h2('Features').class_name('text-3xl font-bold text-center mb-12'),
        div(
            *[
                div(
                    h2(item['title']).class_name('text-xl font-semibold mb-2'),
                    p(item['desc']).class_name('text-gray-600')
                ).class_name('bg-white p-6 rounded-lg shadow-md')
                for item in items
            ]
        ).class_name('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6')
    ).class_name('container mx-auto px-4 py-12')

grid = grid_layout()
grid.to_print()
```

### 4. Form Styling

```python
from pure.html import form, div, label, input, textarea, button

def styled_form():
    return form(
        div(
            label('Name').for_('name').class_name('block text-sm font-medium text-gray-700 mb-2'),
            input().type('text').id('name').name('name').class_name(
                'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            )
        ).class_name('mb-4'),

        div(
            label('Email').for_('email').class_name('block text-sm font-medium text-gray-700 mb-2'),
            input().type('email').id('email').name('email').class_name(
                'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            )
        ).class_name('mb-4'),

        div(
            label('Message').for_('message').class_name('block text-sm font-medium text-gray-700 mb-2'),
            textarea().id('message').name('message').rows('4').class_name(
                'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            )
        ).class_name('mb-6'),

        button('Submit').type('submit').class_name(
            'w-full bg-blue-500 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-600 transition duration-300'
        )
    ).class_name('max-w-md mx-auto bg-white p-8 rounded-lg shadow-md')

form_element = styled_form()
form_element.to_print()
```

## Utility Function Integration

### Using clx function for conditional class names

```python
from pure.html import div, button
from pure.clx import clx

def conditional_button(props):
    is_primary = props.get('primary', False)
    is_large = props.get('large', False)
    is_disabled = props.get('disabled', False)
    text = props.get('text', 'Button')

    classes = clx(
        'font-bold py-2 px-4 rounded transition duration-300',
        {
            'bg-blue-500 hover:bg-blue-700 text-white': is_primary,
            'bg-gray-300 hover:bg-gray-400 text-gray-800': not is_primary,
            'py-3 px-6 text-lg': is_large,
            'opacity-50 cursor-not-allowed': is_disabled
        }
    )

    return button(text).class_name(classes).disabled(is_disabled)

# Usage examples
primary_btn = conditional_button({'text': 'Primary Button', 'primary': True, 'large': True})
secondary_btn = conditional_button({'text': 'Secondary Button', 'disabled': True})

div(primary_btn, secondary_btn).class_name('space-x-4').to_print()
```

## Complete Example

Here's a complete page example showcasing Purepy and TailwindCSS integration:

```python
from pure.html import html, head, meta, title, link, body, div, header, nav, a, main, h1, p, button, footer

def create_landing_page():
    return html(
        head(
            meta().charset('UTF-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1.0'),
            title('Purepy + TailwindCSS Example'),
            link().href('https://cdn.tailwindcss.com').rel('stylesheet')
        ),
        body(
            # Navigation
            header(
                nav(
                    div(
                        div('Purepy').class_name('text-xl font-bold text-white'),
                        div(
                            a('Home').href('#').class_name('text-white hover:text-gray-300 mx-2'),
                            a('Docs').href('#').class_name('text-white hover:text-gray-300 mx-2'),
                            a('About').href('#').class_name('text-white hover:text-gray-300 mx-2')
                        )
                    ).class_name('flex justify-between items-center')
                ).class_name('container mx-auto px-4 py-4')
            ).class_name('bg-blue-600'),

            # Main content
            main(
                div(
                    h1('Welcome to Purepy').class_name('text-5xl font-bold text-gray-900 mb-6'),
                    p('A Python template engine inspired by ReactJS').class_name('text-xl text-gray-600 mb-8'),
                    button('Get Started').class_name(
                        'bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg text-lg'
                    )
                ).class_name('text-center')
            ).class_name('container mx-auto px-4 py-20'),

            # Footer
            footer(
                p('© 2024 Purepy. All rights reserved.').class_name('text-center text-gray-600')
            ).class_name('bg-gray-100 py-8')
        )
    )

# Generate and save page
page = create_landing_page()
page.to_save('landing.html')
print("Page generated: landing.html")
```

## Best Practices

1. **Use semantic component names**: Create meaningful component function names
2. **Extract repeated styles**: Encapsulate common style combinations into functions
3. **Leverage clx function**: Manage conditional class names to keep code clean
4. **Mobile-first approach**: Always consider mobile experience first
5. **Performance optimization**: Use PurgeCSS in production to remove unused styles

## Next Steps

- [Basic Usage](/en/guide/basic-usage) - Learn Purepy's basic syntax
- [API Reference](/en/api/) - View complete API documentation
