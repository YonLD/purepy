import os
import io
import contextlib

from pure.core.Markup import Markup


def plain(name, data=None):
    if data is None:
        data = {}

    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'views', name + '.plain.py')

    if not os.path.isfile(file):
        raise RuntimeError("plain view '{}' is missing: run `pure compile --plain`.".format(name))

    bindings = {}
    for slot, value in data.items():
        if isinstance(value, Markup):
            bindings[slot] = str(value)
        else:
            bindings[slot] = value

    namespace = dict(bindings)
    namespace['__file__'] = file

    with open(file, 'r', encoding='utf-8') as f:
        code = f.read()

    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(code, file, 'exec'), namespace)

    return output.getvalue()
