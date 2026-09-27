from typing import Any, Dict, List, Optional

from ..core.Markup import Markup
from ..core.Tag import Tag
from ..core.Slot import Slot
from ..core.Escaper import Escaper


class Call(Markup):
    def __init__(self, name: str, children: Optional[List[Any]] = None):
        self.__name = name
        self.__props: Dict[str, Any] = {}
        self.__children = self.__flatten(children or [])

    def __call__(self, prop: str, *args):
        if prop == "children":
            raise Exception(
                "component '{}': pass children to the call itself, e.g. {}(children).".format(  # noqa: E501
                    self.__name, self.__name
                )
            )
        if len(args) != 1:
            raise Exception(
                "component '{}': prop '{}' takes exactly one value.".format(
                    self.__name, prop
                )
            )
        return self.set(prop, args[0])

    def __getattr__(self, prop: str):
        def setter(value):
            return self.set(prop, value)

        return setter

    def class_name(self, *args) -> "Call":
        from pure.clx import clx

        if len(args) == 1 and isinstance(args[0], str):
            return self.set("class", args[0])
        return self.set("class", clx(*args))

    def class_(self, *args) -> "Call":
        return self.class_name(*args)

    def style(self, value) -> "Call":
        from pure.sty import sty

        if not isinstance(value, str):
            value = sty(value) or ""
        return self.set("style", value)

    def props(self, props: Dict[str, Any]) -> "Call":
        for key, value in props.items():
            self.set(key, value)
        return self

    def render(self) -> str:
        from .Registry import Registry

        self.guard()
        return Registry.component(self.__name)(self.__data())

    def __str__(self) -> str:
        return self.render()

    def guard(self) -> None:
        """Warn in development about deprecated and untrusted prop bindings.

        purephp reads the #[Prop] and #[Trusted] attributes on the prepare()
        parameters; in Python those are the parameter's annotation or its
        default, so a declaration is read the same way. Silent without the
        guard, and each finding is reported once.
        """
        from ..core.DevMode import DevMode

        if not (DevMode.enabled if DevMode.enabled is not None else DevMode.resolve()):
            return

        trusted, deprecated = self.__declarations()

        for prop, value in self.__props.items():
            if prop in deprecated and DevMode.mark(
                "deprecated:{}:{}".format(self.__name, prop)
            ):
                DevMode.emit(
                    "component '{}': prop '{}' is deprecated: {}".format(
                        self.__name, prop, deprecated[prop]
                    )
                )

            if (
                prop in trusted
                and not self.__untrusted(value)
                and DevMode.mark("trusted:{}:{}".format(self.__name, prop))
            ):
                DevMode.emit(
                    "component '{}': prop '{}' is declared as markup (Trusted) but received {}. "  # noqa: E501
                    "Wrap it with Raw.of() so the value is trusted.".format(
                        self.__name, prop, type(value).__name__
                    )
                )

    def __declarations(self):
        """(trusted props, deprecated props) declared by the prepare() hook."""
        import inspect

        from ..component.Prop import Prop
        from ..component.Trusted import Trusted
        from .Registry import Registry

        prepare = Registry.prepare(self.__name)

        if prepare is None:
            return set(), {}

        trusted, deprecated = set(), {}

        try:
            parameters = inspect.signature(prepare).parameters.values()
        except (TypeError, ValueError):
            return trusted, deprecated

        for parameter in parameters:
            declaration = None
            annotation = parameter.annotation
            default = parameter.default

            for candidate in (annotation, default):
                if isinstance(candidate, Prop):
                    declaration = candidate
                    break

            if (
                annotation is Trusted
                or isinstance(annotation, Trusted)
                or default is Trusted
            ):
                trusted.add(parameter.name)

            if declaration is not None and declaration.deprecated:
                deprecated[parameter.name] = declaration.deprecated

        return trusted, deprecated

    def __untrusted(self, value) -> bool:
        if isinstance(value, Markup):
            return True

        if isinstance(value, (list, tuple)):
            return bool(value) and all(self.__untrusted(item) for item in value)

        return False

    def __data(self) -> Dict[str, Any]:
        data = dict(self.__props)
        if self.__children:
            data["children"] = [self.__child_markup(c) for c in self.__children]
        return data

    def __child_markup(self, child) -> str:
        if isinstance(child, Tag):
            return child.render()
        if isinstance(child, Markup):
            return str(child)
        if isinstance(child, Slot):
            raise Exception(
                "component '{}': a Slot cannot be a child of a call; "
                "bind it to a raw slot instead.".format(self.__name)
            )
        return Escaper.text(str(child))

    def set(self, prop: str, value) -> "Call":
        if value is None:
            return self
        if isinstance(value, Slot):
            raise Exception(
                "component '{}': prop '{}' cannot be a Slot; "
                "a component call binds values.".format(self.__name, prop)
            )
        self.__props[self.__prop_name(prop)] = value
        return self

    @staticmethod
    def __prop_name(prop: str) -> str:
        """purephp's `->class()` is `class_()` in Python, so a trailing
        underscore stands in for a name that is a Python keyword."""
        import keyword

        if prop.endswith("_") and keyword.iskeyword(prop[:-1]):
            return prop[:-1]

        return prop

    @staticmethod
    def __flatten(children: List[Any]) -> List[Any]:
        flat = []
        for child in children:
            if child is None:
                continue
            if isinstance(child, list):
                flat.extend(Call.__flatten(child))
            else:
                flat.append(child)
        return flat
