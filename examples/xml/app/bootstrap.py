import os


def plain(name, data=None):
    """Render a compiled plain view and return its document.

    A plain view is a module whose `view()` takes the root slots as keyword
    parameters, so the data is passed by name rather than extracted into the
    module globals.
    """
    if data is None:
        data = {}

    file = os.path.join(os.path.dirname(__file__), '..', 'views', name + '.plain.py')

    if not os.path.isfile(file):
        raise RuntimeError("plain view '{}' is missing: run `pure compile --plain`.".format(name))

    with open(file) as f:
        code = f.read()

    namespace = {}
    exec(compile(code, file, 'exec'), namespace)

    return namespace['view'](**data)
