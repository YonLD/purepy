# Purepy

Purepy is a Virtual DOM based templating-engine for Python inspired by ReactJS.

## Why use Purepy

To enjoy pure Python programming.

In traditional approaches, mixing HTML code, Python code, and other template syntax in the view layer can be frustrating for developers.

However, with Purepy:
+ Everything is 100% native Python code.
+ Encapsulate components to eliminate repetitive HTML code.
+ The syntax closely resembles HTML.

## Install

`composer require yonld/purephp`

## Basic usage

Here is a simple example that will show how to use `Purepy`:

```python

from purepy.html import div, a

div(
    'Hello ',
    a('Python').href('https://www.php.net')
).class_name('container').style('background: #fff;').data_key('primary').toPrint()
```

The above code will output:

```html
<div class_name="container" style="background: #fff;" data-key="primary">Hello <a href="https://www.php.net">Python</a></div>
```

## Documentation

To check out docs, visit []().

## Examples

For more usage examples see [here](https://github.com/YonLD/purepy/tree/master/examples).

## License

MIT © YonLD
