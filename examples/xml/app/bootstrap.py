import os


def plain(name, data=None):
    if data is None:
        data = {}

    file = os.path.join(os.path.dirname(__file__), '..', 'views', name + '.plain.py')

    if not os.path.isfile(file):
        raise RuntimeError("plain view '{}' is missing: run `pure compile --plain`.".format(name))

    with open(file) as f:
        code = f.read()

    local_vars = dict(data)
    exec(code, local_vars)
    return local_vars['render']()
