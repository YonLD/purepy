# XML 类

**本页内容**：`XML` 类——任意标签名的创建、保存方法、文档头，以及配置导出、
RSS、SOAP 等常见场景。

`pure.core.XML.XML` 继承 Tag 类，用于创建 XML 元素。

## 创建 XML 元素

XML 标签名是任意的，所以元素通过从类上读取标签名来创建：

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

不是合法 Python 标识符的名字（比如带命名空间前缀的）走动态形式：

```python
envelope = getattr(XML, 'soap:Envelope')(
    getattr(XML, 'soap:Header')()
)
```

## 保存方法

### `save(path, header=None)`

把 XML 元素写入文件。省略 `header` 时会先写 `<?xml version="1.0"?>`。返回值是
写入的字节数。

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

## 文档头

### `documentHeader()`

返回默认的 XML 声明 `<?xml version="1.0"?>`。`save()` 会使用它，除非显式传入了
header；`render()` 从不添加文档头。`pure.utils.renderXML()` 同样会补上这个声明——
需要完整文档而不是片段时用它。

## 示例

### 配置文件

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

### 数据导出

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

### RSS 订阅源

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

`pubDate` 必须是 RFC 2822 日期，如示例所示。XML 构建器会转义元素文本和属性值，
但不会按 RSS schema 校验整个订阅源。

### SOAP 信封

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

带冒号的名字不是合法 Python 标识符，所以示例用 `getattr(XML, 'soap:Envelope')`
来访问带前缀的元素名。`set_attrs()` 是公开方法，会保留 `xmlns:soap` 的写法；
`xmlns_soap(...)` 会把下划线转成连字符变成 `xmlns-soap`，那不是 SOAP 命名空间。

### 大文档

```python
from pure.core.XML import XML

items = [XML.item('Item {}'.format(i)).id(str(i)) for i in range(1, 10001)]

large_xml = XML.root(*items)
large_xml.save('large.xml')
```
