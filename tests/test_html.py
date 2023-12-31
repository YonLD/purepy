import unittest
from os import path, remove

from pure.core.HTML import HTML
from pure.raw import raw_html
from pure.html import html, head, meta, title, body, div, header, h1, nav, ul, li, a, main, section, h2, p, form, label, input, textarea, footer, button, span

class HTMLTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__html: HTML = self.__create_instance()

    def __create_instance(self):
        return html(
            head(
                meta().charset('UTF-8'),
                title('Complex HTML Code Example')
            ),
            body(
                div(
                    header(
                        h1('Welcome to My Website'),
                        nav(
                            ul(
                                li(
                                    a('Home').href('#')
                                ),
                                li(
                                    a('About').href('#')
                                ),
                                li(
                                    a('Services').href('#')
                                ),
                                raw_html('<li><a href="#">Contact</a></li>')
                            )
                        ).class_name('nav')
                    ).class_name('header'),
                    main(
                        section(
                            h2('About Us'),
                            p('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultrices urna eget sapien ullamcorper, vel efficitur massa semper.'),
                            a('Learn More').href('#').class_name('button')
                        ).class_name('section'),
                        section(
                            h2('Our Services'),
                            ul(
                                li('Service 1'),
                                li('Service 2'),
                                li('Service 3')
                            )
                        ).class_name('section'),
                        section(
                            h2('Contact Us'),
                            form(
                                label('Name:').class_name('form-label').htmlFor('name'),
                                input().type('text').id('name').name('name').class_name('form-input'),
                                label('Email:').class_name('form-label').htmlFor('email'),
                                input().type('email').id('email').name('email').class_name('form-input'),
                                label('Message:').class_name('form-label').htmlFor('message'),
                                textarea().id('message').name('message').class_name('form-input'),
                                button('Submit').type('submit').class_name('button')
                            )
                        ).class_name('section')
                    ),
                    footer(
                        p('&copy; 2023 My Website. All rights reserved.')
                    ).class_name('footer')
                ).class_name('container'),
            )
        ).lang('en')

    def test_tag_name(self):
        self.assertEqual('html', html().get_tag_name())
        self.assertEqual('head', head().get_tag_name())
        self.assertEqual('body', body().get_tag_name())
        self.assertEqual('div', div().get_tag_name())
        self.assertEqual('title', title().get_tag_name())
        self.assertEqual('p', p().get_tag_name())
        self.assertEqual('a', a().get_tag_name())

    def test_attributes(self):
        tag = input().type('text').id('my-input').value(0).disabled(False).readonly(None).required(True)
        attributes = tag.get_attributes()

        self.assertEqual(4, len(attributes))
        self.assertNotIn('disabled', attributes)
        self.assertNotIn('readonly', attributes)
        self.assertEqual('text', tag.get_attribute('type'))
        self.assertEqual('my-input', tag.get_attribute('id'))
        self.assertEqual('0', tag.get_attribute('value'))
        self.assertEqual('required', tag.get_attribute('required'))

    def test_children(self):
        child1 = 'Hello'
        child2 = span('World').style('color: red;')
        tag = div(child1, child2)
        children = tag.get_children()

        self.assertEqual(2, len(children))
        self.assertEqual(child1, children[0])
        self.assertEqual(child2, children[1])

    def test_to_JSON(self):
        excepted = {
            'tag_name': 'html',
            'children': [
                {
                    'tag_name': 'head',
                    'children': [
                        {
                            'tag_name': 'meta',
                            'children': [],
                            'charset': 'UTF-8'
                        },
                        {
                            'tag_name': 'title',
                            'children': [
                                'Complex HTML Code Example'
                            ]
                        }
                    ]
                },
                {
                    'tag_name': 'body',
                    'children': [
                        {
                            'tag_name': 'div',
                            'children': [
                                {
                                    'tag_name': 'header',
                                    'children': [
                                        {
                                            'tag_name': 'h1',
                                            'children': [
                                                'Welcome to My Website'
                                            ]
                                        },
                                        {
                                            'tag_name': 'nav',
                                            'children': [
                                                {
                                                    'tag_name': 'ul',
                                                    'children': [
                                                        {
                                                            'tag_name': 'li',
                                                            'children': [
                                                                {
                                                                    'tag_name': 'a',
                                                                    'children': [
                                                                        'Home'
                                                                    ],
                                                                    'href': '#'
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            'tag_name': 'li',
                                                            'children': [
                                                                {
                                                                    'tag_name': 'a',
                                                                    'children': [
                                                                        'About'
                                                                    ],
                                                                    'href': '#'
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            'tag_name': 'li',
                                                            'children': [
                                                                {
                                                                    'tag_name': 'a',
                                                                    'children': [
                                                                        'Services'
                                                                    ],
                                                                    'href': '#'
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            'type': 'HTML',
                                                            'content': '<li><a href="#">Contact</a></li>'
                                                        }
                                                    ]
                                                }
                                            ],
                                            'class': 'nav'
                                        }
                                    ],
                                    'class': 'header'
                                },
                                {
                                    'tag_name': 'main',
                                    'children': [
                                        {
                                            'tag_name': 'section',
                                            'children': [
                                                {
                                                    'tag_name': 'h2',
                                                    'children': [
                                                        'About Us'
                                                    ]
                                                },
                                                {
                                                    'tag_name': 'p',
                                                    'children': [
                                                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultrices urna eget sapien ullamcorper, vel efficitur massa semper.'
                                                    ]
                                                },
                                                {
                                                    'tag_name': 'a',
                                                    'children': [
                                                        'Learn More'
                                                    ],
                                                    'href': '#',
                                                    'class': 'button'
                                                }
                                            ],
                                            'class': 'section'
                                        },
                                        {
                                            'tag_name': 'section',
                                            'children': [
                                                {
                                                    'tag_name': 'h2',
                                                    'children': [
                                                        'Our Services'
                                                    ]
                                                },
                                                {
                                                    'tag_name': 'ul',
                                                    'children': [
                                                        {
                                                            'tag_name': 'li',
                                                            'children': [
                                                                'Service 1'
                                                            ]
                                                        },
                                                        {
                                                            'tag_name': 'li',
                                                            'children': [
                                                                'Service 2'
                                                            ]
                                                        },
                                                        {
                                                            'tag_name': 'li',
                                                            'children': [
                                                                'Service 3'
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ],
                                            'class': 'section'
                                        },
                                        {
                                            'tag_name': 'section',
                                            'children': [
                                                {
                                                    'tag_name': 'h2',
                                                    'children': [
                                                        'Contact Us'
                                                    ]
                                                },
                                                {
                                                    'tag_name': 'form',
                                                    'children': [
                                                        {
                                                            'tag_name': 'label',
                                                            'children': [
                                                                'Name:'
                                                            ],
                                                            'class': 'form-label',
                                                            'for': 'name'
                                                        },
                                                        {
                                                            'tag_name': 'input',
                                                            'children': [],
                                                            'type': 'text',
                                                            'id': 'name',
                                                            'name': 'name',
                                                            'class': 'form-input'
                                                        },
                                                        {
                                                            'tag_name': 'label',
                                                            'children': [
                                                                'Email:'
                                                            ],
                                                            'class': 'form-label',
                                                            'for': 'email'
                                                        },
                                                        {
                                                            'tag_name': 'input',
                                                            'children': [],
                                                            'type': 'email',
                                                            'id': 'email',
                                                            'name': 'email',
                                                            'class': 'form-input'
                                                        },
                                                        {
                                                            'tag_name': 'label',
                                                            'children': [
                                                                'Message:'
                                                            ],
                                                            'class': 'form-label',
                                                            'for': 'message'
                                                        },
                                                        {
                                                            'tag_name': 'textarea',
                                                            'children': [],
                                                            'id': 'message',
                                                            'name': 'message',
                                                            'class': 'form-input'
                                                        },
                                                        {
                                                            'tag_name': 'button',
                                                            'children': [
                                                                'Submit'
                                                            ],
                                                            'type': 'submit',
                                                            'class': 'button'
                                                        }
                                                    ]
                                                }
                                            ],
                                            'class': 'section'
                                        }
                                    ],
                                },
                                {
                                    'tag_name': 'footer',
                                    'children': [
                                        {
                                            'tag_name': 'p',
                                            'children': [
                                                '&copy; 2023 My Website. All rights reserved.'
                                            ]
                                        }
                                    ],
                                    'class': 'footer'
                                }
                            ],
                            'class': 'container'
                        }
                    ]
                }
            ],
            'lang': 'en'
        }

        self.assertEqual(excepted, self.__html.to_JSON())

    def test_to_string(self):
        excepted_str = '<html lang="en"><head><meta charset="UTF-8" /><title>Complex HTML Code Example</title></head><body><div class="container"><header class="header"><h1>Welcome to My Website</h1><nav class="nav"><ul><li><a href="#">Home</a></li><li><a href="#">About</a></li><li><a href="#">Services</a></li><li><a href="#">Contact</a></li></ul></nav></header><main><section class="section"><h2>About Us</h2><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultrices urna eget sapien ullamcorper, vel efficitur massa semper.</p><a href="#" class="button">Learn More</a></section><section class="section"><h2>Our Services</h2><ul><li>Service 1</li><li>Service 2</li><li>Service 3</li></ul></section><section class="section"><h2>Contact Us</h2><form><label class="form-label" for="name">Name:</label><input type="text" id="name" name="name" class="form-input" /><label class="form-label" for="email">Email:</label><input type="email" id="email" name="email" class="form-input" /><label class="form-label" for="message">Message:</label><textarea id="message" name="message" class="form-input"></textarea><button type="submit" class="button">Submit</button></form></section></main><footer class="footer"><p>&copy; 2023 My Website. All rights reserved.</p></footer></div></body></html>'
        self.assertEqual(excepted_str, str(self.__html))

    def test_to_save(self):
        output_path = './output.html'
        tag = div('Hello, World!')
        tag.to_save(output_path)

        with open(output_path, 'r') as file:
            content = file.read()

        self.assertTrue(path.exists(output_path))
        self.assertEqual('<!DOCTYPE html><div>Hello, World!</div>', content)
        remove(output_path)

if __name__ == '__main__':
    unittest.main()
