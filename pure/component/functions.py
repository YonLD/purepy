from typing import Callable, Optional

from .Call import Call
from .Registry import Registry


def register(
    call: Callable,
    factory: Optional[Callable] = None,
    override: bool = False,
    prepare: Optional[Callable] = None,
):
    import inspect

    # purephp takes a first-class callable and rejects an anonymous closure.
    # Python's equivalent of an anonymous function is a lambda, which carries
    # no usable name for the registry, so it is rejected the same way.
    if not (inspect.isfunction(call) or inspect.ismethod(call)):
        raise ValueError(
            "'register()' needs a named call function, not an anonymous closure."
        )

    name = getattr(call, "__name__", "")

    if not name or name.startswith("<"):
        raise ValueError(
            "'register()' needs a named call function, not an anonymous closure."
        )

    if factory is None:
        raise ValueError(
            "'register()' needs a factory that returns the component's tag tree or Shape."  # noqa: E501
        )

    file = inspect.getfile(call)
    Registry.register(name, file, factory, override, prepare)


def component(name: str, *children) -> Call:
    return Call(name, list(children))
