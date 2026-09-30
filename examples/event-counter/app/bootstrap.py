import os


def plain(name, data=None):
    if data is None:
        data = {}

    file = os.path.join(os.path.dirname(__file__), '..', 'views', name + '.plain.py')

    if not os.path.isfile(file):
        raise RuntimeError("plain view '{}' is missing: run `pure compile --plain`.".format(name))

    namespace = {}
    namespace.update(data)

    with open(file, 'r') as f:
        code = f.read()

    # A plain view is a module whose `view()` takes the root slots as keyword
    # parameters, so the data is passed by name.
    exec(compile(code, file, 'exec'), namespace)

    return namespace['view'](**data)
