import json
import os

_content = None


def content():
    global _content

    if _content is not None:
        return _content

    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'features.json')

    try:
        with open(file, 'r', encoding='utf-8') as f:
            raw = f.read()
    except OSError:
        raise RuntimeError("could not read the page content from '{}'.".format(file))

    decoded = json.loads(raw)

    if not isinstance(decoded, dict):
        raise RuntimeError("'{}' must hold a JSON object.".format(file))

    _content = decoded

    return _content
