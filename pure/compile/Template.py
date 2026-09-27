class Template:
    """Marks a function that builds a shape for a `*.shape.py` template.

    In purephp this is a `#[Template]` attribute; in Python the equivalent is a
    decorator, so a template function declares itself:

        @Template
        def shape():
            return Compile.shape(div(Slot.value('title')))

        @Template()
        def shape(): ...          # both spellings work

    `pure check` reads the mark to verify the declared return type, and
    `pure compile --list` reports the marked functions. The mark is stored on
    the function itself, so the decorated name stays a plain function and stays
    introspectable. A function without the mark behaves exactly as before.
    """

    def __new__(cls, func=None):
        # Used bare as @Template: return the function itself, not a wrapper,
        # so the module keeps a real function for reflection.
        if callable(func):
            Template.mark(func)
            return func

        return super().__new__(cls)

    def __call__(self, func):
        # Used as @Template().
        Template.mark(func)
        return func

    @staticmethod
    def mark(func) -> None:
        markers = list(getattr(func, "__pure_attributes__", ()))

        if Template.__name__ not in markers:
            markers.append(Template.__name__)

        func.__pure_attributes__ = tuple(markers)
