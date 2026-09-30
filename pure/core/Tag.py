from __future__ import annotations

import keyword
from abc import ABC, ABCMeta
from typing import Any, Union, List, Dict, Tuple, Optional

from .Raw import Raw
from .Slot import Slot
from .Markup import Markup
from .Escaper import Escaper
from .DevMode import DevMode
from .AttributeNames import AttributeNames


class TagFactory(ABCMeta):
    """The static tag constructors purephp reaches through `__callStatic`.

    Reading any other attribute off a tag class builds an element of that name,
    so `HTML.div('x')` and the module-level `div('x')` are the same element,
    and a custom element needs no declaration the way a magic static call does
    not need one in PHP either.

    It derives from `ABCMeta` rather than `type` because `Tag` is an abstract
    base class, and a subclass of an ABC may only use a metaclass derived from
    the one its base uses.

    An attribute that starts with an underscore is left alone, so the
    machinery Python probes for (copy, pickle, the ABC registry) still finds a
    real `AttributeError` instead of an element named after it.
    """

    def __getattr__(cls, tag: str):
        if tag.startswith("_"):
            raise AttributeError(tag)

        def build(*children: Any):
            return cls(tag, children)

        return build


class Tag(ABC):
    def __init__(
        self, tag_name: str, children: Tuple[Union[str, Raw, Tag, Slot], ...] = ()
    ):
        self.__tag_name = tag_name
        self.__attrs: Dict[str, Union[str, Slot]] = {}
        self.__children: List[Union[str, Raw, Tag, Slot]] = []
        self.__self_close = False

        if isinstance(children, (list, tuple)):
            self.__append_children(tuple(children))
        else:
            self.__append_child(children)

    def tree(self) -> Tag:
        return self

    def export(self) -> Dict[str, Any]:
        return {
            "tagName": self.__tag_name,
            "attrs": self.__attrs,
            "children": self.__children,
            "selfClose": self.__self_close,
        }

    def isDocumentRoot(self) -> bool:
        return False

    def __call__(self, *args: Union[str, Raw, Tag, Slot]):
        self.__append_children(args)
        return self

    def __str__(self):
        return self.render()

    def __getattr__(self, key: str):
        def missing_method(*args):
            args_list = list(args)
            if not args_list:
                raise Exception(
                    "'{}()' accepts one parameter. "
                    "'{}()->{}() is invalid.'".format(key, self.__tag_name, key)
                )
            if len(args_list) != 1:
                raise Exception(
                    "'{}()' only accepts one parameter. "
                    "'{}()->{}({}) is invalid.'".format(
                        key, self.__tag_name, key, ",".join(str(a) for a in args_list)
                    )
                )
            self.__set_attr(key, args_list[0])
            return self

        return missing_method

    def class_name(self, *args) -> Tag:
        from pure.clx import clx

        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, Slot):
                return self.__set_attr("class", arg)
            return self.__set_attr("class", clx(arg))

        classes = []
        for arg in args:
            if isinstance(arg, Slot):
                raise Exception(
                    "Slot values cannot be combined with other 'class' arguments."
                )
            classes.append(arg)

        return self.__set_attr("class", clx(*classes))

    def class_(self, *args) -> Tag:
        return self.class_name(*args)

    def className(self, *args) -> Tag:
        return self.class_name(*args)

    def style(self, value: Union[Dict[str, Any], str, Slot, None]) -> Tag:
        from pure.sty import sty

        if isinstance(value, Slot):
            return self.__set_attr("style", value)

        if value is None:
            return self.__set_attr("style", None)

        if not isinstance(value, str):
            result = sty(value)
            if result is not None:
                value = result
            else:
                value = ""

        self.__set_attr("style", value)
        return self

    def htmlFor(self, value: str) -> Tag:
        self.__set_attr("for", value)
        return self

    def get_self_close(self) -> bool:
        return self.__self_close

    def set_self_close(self, value: bool) -> Tag:
        if value and self.__children:
            raise Exception(
                "Self-closing element '{}' cannot have "
                "child elements.".format(self.__tag_name)
            )
        self.__self_close = value
        return self

    def get_tag_name(self) -> str:
        return self.__tag_name

    def get_attrs(self) -> Dict[str, Union[str, Slot]]:
        return self.__attrs

    def get_attr(self, key: str) -> Optional[Union[str, Slot]]:
        if key in self.__attrs:
            return self.__attrs[key]
        if key == "className":
            key = "class"
        else:
            key = key.replace("_", "-")
        return self.__attrs.get(key)

    def get_children(self) -> List[Union[str, Raw, Tag, Slot]]:
        return self.__children

    def set_attrs(self, props: Dict[str, Union[str, bool, Slot, None]]) -> Tag:
        if not props:
            return self
        for key, value in props.items():
            if value is not None and not isinstance(
                value, (str, bool, int, float, Slot)
            ):
                value = Escaper.to_string(value)
            self.__set_attr(key, value)
        return self

    def __set_attr(self, key: str, value: Union[str, bool, Slot, None]) -> Tag:
        if value is None:
            return self
        if not key:
            raise Exception(
                "Element '{}' attribute name cannot "
                "be empty.".format(self.__tag_name)
            )
        # A trailing underscore escapes a Python keyword (`for_` -> `for`),
        # following the `class_()` convention. Everything else is a hyphen.
        if len(key) > 1 and key.endswith("_") and keyword.iskeyword(key[:-1]):
            key = key[:-1]
        else:
            key = key.replace("_", "-")
        self.guardAttributeName(key)
        if isinstance(value, bool):
            if not value:
                return self
            value = key
        if isinstance(value, Slot):
            self.__attrs[key] = value
            return self
        if not isinstance(value, (str, int, float)):
            raise Exception(
                "Element '{}' attribute '{}' must be a scalar, Stringable, Slot or null, "  # noqa: E501
                "{} given; use class()/style() for arrays.".format(
                    self.__tag_name, key, Escaper.debug_type(value)
                )
            )
        self.__attrs[key] = Escaper.to_string(value)
        return self

    def __append_children(
        self, children: Tuple[Union[str, Raw, Tag, Slot, None], ...]
    ) -> None:
        if not children:
            return
        for child in children:
            self.__append_child(child)

    def __append_child(
        self, child: Union[str, Raw, Tag, Slot, None, List[Any]]
    ) -> None:
        if child is None:
            return
        if isinstance(child, list):
            self.__append_children(tuple(child))
            return
        if isinstance(child, (str, Markup, Tag, Slot)):
            self.__children.append(child)
            return
        # Everything else is frozen to a string here, so a value that is merely
        # stringable is text like any other and gets escaped on render. Only an
        # explicit Markup (Raw, a Call) is output the caller vouched for. The
        # freeze goes through the PHP `(string)` cast, so a bool child renders as
        # `1` or nothing rather than its repr.
        self.__children.append(Escaper.to_string(child))

    def render(self) -> str:
        tag_name = self.__tag_name
        attrs = self.__build_attrs_str()

        if self.__self_close:
            return "<{}{} />".format(tag_name, attrs)

        content = self.__build_children_str()
        return "<{}{}>{}</{}>".format(tag_name, attrs, content, tag_name)

    def __build_attrs_str(self) -> str:
        if not self.__attrs:
            return ""

        attrs = ""
        for key, value in self.__attrs.items():
            if isinstance(value, Slot):
                raise Exception(
                    "Tag trees containing slots cannot be rendered directly; "
                    "use Compile.shape() and render with data."
                )
            attrs += Escaper.attribute(key, value)

        return attrs

    def __build_children_str(self) -> str:
        content = ""
        for child in self.__children:
            if isinstance(child, Tag):
                content += child.render()
            elif isinstance(child, Markup):
                content += str(child)
            elif isinstance(child, Slot):
                raise Exception(
                    "Tag trees containing slots cannot be rendered directly; "
                    "use Compile.shape() and render with data."
                )
            else:
                content += Escaper.text(str(child))
        return content

    def to_JSON(self) -> Dict[str, Any]:
        def format_child(child):
            if isinstance(child, Slot):
                return {"slot": child.name}
            if isinstance(child, Raw):
                return child._value
            if isinstance(child, Markup):
                return {"markup": type(child).__name__}
            if isinstance(child, Tag):
                return child.to_JSON()
            return str(child)

        attrs: Dict[str, Any] = {}
        for key, value in self.__attrs.items():
            if isinstance(value, Slot):
                attrs[key] = {"slot": value.name}
            else:
                attrs[key] = value

        return {
            "tagName": self.__tag_name,
            "attrs": attrs,
            "children": [format_child(c) for c in self.__children],
        }

    def documentHeader(self) -> str:
        return self.defaultHeader()

    def defaultHeader(self) -> str:
        return ""

    def save(self, path: str, header: Optional[str] = None) -> int:
        """Write the element to a file and return how many bytes it took.

        The bytes are UTF-8 whatever the locale says, so the count is the count
        the file holds; that is also what purephp's `save()` reports.
        """
        rendered = self.render()
        if header is None:
            header = self.defaultHeader()

        with open(path, "wb") as f:
            return f.write((header + rendered).encode("utf-8"))

    def print(self) -> None:
        print(self.__str__())

    def guardAttributeName(self, key: str) -> None:
        """Development guard hook: a vocabulary class warns when an attribute
        setter carries a near-miss standard attribute name. The base class
        accepts any attribute name, so this is a no-op; HTML and SVG override
        it with `guardStandardAttribute`.
        """
        pass

    def guardStandardAttribute(self, key: str) -> None:
        """Warn once per attribute name when a setter carries a name one edit
        away from a standard attribute, so `div().clas('x')` is not a silent
        custom attribute. Development guard only, off by default.
        """
        if not (DevMode.enabled if DevMode.enabled is not None else DevMode.resolve()):
            return

        nearest = AttributeNames.nearest(key)

        if nearest is None:
            return

        DevMode.warn(
            "attribute:" + key,
            "Element '{}' has no standard attribute '{}'; did you mean '{}'? "
            "Ignore this warning for a custom attribute, or disable the "
            "guard with Compile.guard(False).".format(self.__tag_name, key, nearest),
        )
