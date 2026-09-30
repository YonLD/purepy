# XML Class

`pure.core.XML.XML` extends the Tag class for creating XML elements.

## Creating XML Elements

XML tag names are arbitrary, so elements are created by reading the tag name off
the class:

```python
from pure.core.XML import XML

customer = XML.customer(
    XML.name('Customer Name'),
    XML.address(
        XML.street('Street Address'),
        XML.city('City'),
        XML.zip('Zip Code')
    )
).id('123')
```

A name that is not a valid Python identifier — a namespaced one, for instance —
goes through the dynamic form:

```python
envelope = getattr(XML, 'soap:Envelope')(
    getattr(XML, 'soap:Header')()
)
```

## Save Methods

### `save(path, header=None)`

Saves the XML element to a file. When `header` is omitted,
`<?xml version="1.0"?>` is written first. The return value is the number of
bytes written.

```python
from pure.core.XML import XML

xml = XML.root(
    XML.item('Content 1'),
    XML.item('Content 2')
)

written = xml.save('output.xml')
if written is not None:
    print('XML file saved successfully')
```

## Document Header

### `documentHeader()`

Returns the default XML declaration, `<?xml version="1.0"?>`. `save()` uses it
unless an explicit header is supplied; `render()` never adds a header. The same
declaration is prepended by `pure.utils.renderXML()`, which is the entry point
to use when you want the document rather than a fragment.

## Examples

### Configuration Files

```python
from pure.core.XML import XML

config = XML.configuration(
    XML.database(
        XML.host('localhost'),
        XML.port('3306'),
        XML.name('myapp'),
        XML.username('user'),
        XML.password('pass')
    ),
    XML.cache(
        XML.enabled('true'),
        XML.ttl('3600')
    ),
    XML.logging(
        XML.level('info'),
        XML.file('/var/log/app.log')
    )
).version('1.0')

config.save('config.xml')
```

### Data Export

```python
from pure.core.XML import XML


def export_users(users):
    user_elements = []

    for user_data in users:
        address_elements = []
        for address in user_data.get('addresses', []):
            address_elements.append(
                XML.address(
                    XML.street(address['street']),
                    XML.city(address['city']),
                    XML.state(address['state']),
                    XML.zip(address['zip'])
                ).type(address['type'])
            )

        children = [
            XML.name(user_data['name']),
            XML.email(user_data['email']),
            XML.role(user_data['role']),
            XML.created(user_data['created_at']),
        ]
        if address_elements:
            children.append(XML.addresses(*address_elements))

        user_elements.append(XML.user(*children).id(user_data['id']))

    return XML.users(*user_elements)


users = [
    {
        'id': '1',
        'name': 'John Doe',
        'email': 'john@example.com',
        'role': 'admin',
        'created_at': '2024-01-01',
        'addresses': [
            {
                'type': 'home',
                'street': '123 Main St',
                'city': 'Anytown',
                'state': 'CA',
                'zip': '12345'
            }
        ]
    }
]

xml = export_users(users)
xml.save('users.xml')
```

### RSS Feed

```python
from pure.core.XML import XML


def create_rss_feed(items):
    return XML.rss(
        XML.channel(
            XML.title('My Blog'),
            XML.link('https://myblog.com'),
            XML.description('Latest posts from my blog'),
            XML.language('en-us'),
            XML.pubDate('Mon, 01 Jan 2024 12:00:00 +0000'),
            *[
                XML.item(
                    XML.title(item['title']),
                    XML.link(item['url']),
                    XML.description(item['description']),
                    XML.pubDate(item['date']),
                    XML.guid(item['url'])
                )
                for item in items
            ]
        )
    ).version('2.0')


posts = [
    {
        'title': 'First Post',
        'url': 'https://myblog.com/first-post',
        'description': 'This is my first blog post',
        'date': 'Mon, 01 Jan 2024 12:00:00 +0000'
    }
]

rss = create_rss_feed(posts)
rss.save('feed.xml')
```

RSS `pubDate` values must be RFC 2822 dates, as in the example. The XML
builder escapes element text and attribute values, but it does not validate a
feed against the RSS schema.

### SOAP Envelope

```python
from pure.core.XML import XML

soap_namespace = 'http://schemas.xmlsoap.org/soap/envelope/'
soap_envelope = getattr(XML, 'soap:Envelope')(
    getattr(XML, 'soap:Header')(
        getattr(XML, 'soap:Authentication')(
            XML.username('user'),
            XML.password('pass')
        )
    ),
    getattr(XML, 'soap:Body')(
        getattr(XML, 'soap:GetUserRequest')(
            XML.userId('123')
        )
    )
)
soap_envelope.set_attrs({'xmlns:soap': soap_namespace})

print(soap_envelope.render())
```

A name that contains a colon cannot be a Python identifier, so the example uses
`getattr(XML, 'soap:Envelope')` for the prefixed element names. `set_attrs()`
is public and keeps the `xmlns:soap` spelling; `xmlns_soap(...)` would normalize
the underscore to `xmlns-soap` and is not a SOAP namespace.

### Large Documents

```python
from pure.core.XML import XML

items = [XML.item('Item {}'.format(i)).id(str(i)) for i in range(1, 10001)]

large_xml = XML.root(*items)
large_xml.save('large.xml')
```
