from abc import ABC, abstractmethod
from typing import Any, Union, List, Dict, Tuple, Callable, Optional

from .Raw import Raw


class Tag(ABC):
    def __init__(self, tag_name: str, children: Tuple[Union[str, Raw, "Tag"], ...]):
        self.__tag_name = tag_name
        self.__attrs: Dict[str, str] = {}
        self.__children: List[Union[str, Raw, "Tag"]] = []
        self.__self_close = False

        self.__append_children(children)

    def __call__(self, *args: Union[str, Raw, "Tag"]):
        self.__append_children(args)
        return self

    def __str__(self):
        return str(self.to_PDom())

    def __getattr__(self, key: str):
        def missing_method(*args: str):
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
                        key, self.__tag_name, key, ",".join(args_list)
                    )
                )
            self.__set_attr(key, args_list[0])
            return self

        return missing_method

    def class_name(
        self, *args: Union[Dict[str, Any], str, None, List[Union[str, None]]]
    ) -> "Tag":
        from pure import clx

        if len(args) == 1 and type(args[0]) is str:
            self.__set_attr("class", args[0])
        else:
            result = clx(*args)  # type: ignore[operator]
            if result is not None:
                self.__set_attr("class", result)
        return self

    def style(self, value: Union[Dict[str, Any], str, None]) -> "Tag":
        from pure import sty

        if not isinstance(value, str):
            result = sty(value)  # type: ignore[operator]
            if result is not None:
                value = result
            else:
                value = ""

        self.__set_attr("style", value)  # type: ignore[arg-type]
        return self

    def htmlFor(self, value: str) -> "Tag":
        self.__set_attr("for", value)
        return self

    def get_self_close(self) -> bool:
        return self.__self_close

    def set_self_close(self, value: bool) -> "Tag":
        self.__self_close = value
        if self.__self_close and bool(self.__children):
            raise Exception(
                "Self-closing element '{}' cannot have "
                "child elements.".format(self.__tag_name)
            )
        return self

    def get_tag_name(self) -> str:
        return self.__tag_name

    def get_attrs(self) -> Dict[str, str]:
        return self.__attrs

    def get_attr(self, key: str) -> Optional[str]:
        return self.__attrs.get(key)

    def set_attrs(self, props: Dict[str, Union[str, bool, None]]) -> "Tag":
        if not props:
            return self
        for key, value in props.items():
            self.__set_attr(key, value)
        return self

    def set_attr_by_cb(
        self, key: str, callback: Callable[[Optional[str]], Optional[str]]
    ) -> None:
        value = callback(self.get_attr(key))
        if value is None and key in self.__attrs:
            del self.__attrs[key]
        elif value is not None:
            self.__attrs[key] = value

    def __set_attr(self, key: str, value: Union[str, bool, None]) -> None:
        if value is None:
            return
        if not key:
            raise Exception(
                "Element '{}' attribute name cannot "
                "be empty '{}'.".format(self.__tag_name, key)
            )
        key = key.replace("_", "-")
        if isinstance(value, bool):
            if not value:
                return
            value = key
        self.__attrs[key] = str(value)

    def get_children(self) -> List[Union[str, Raw, "Tag"]]:
        return self.__children

    def __append_children(self, children: Tuple[Union[str, Raw, "Tag"], ...]) -> None:
        if not children:
            return
        for child in children:
            self.__append_child(child)

    def __append_child(self, child: Union[str, Raw, "Tag", None, List[Any]]) -> None:
        if child is None:
            return
        if isinstance(child, list):
            self.__append_children(tuple(child))
            return
        if isinstance(child, str) or isinstance(child, Raw) or isinstance(child, Tag):
            self.__children.append(child)
            return
        self.__children.append(str(child))

    def to_JSON(self) -> Dict[str, Any]:
        def merge_dict(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
            dict1.update(dict2)
            return dict1

        def format_child(child: Union[Tag, Raw, str]):
            if isinstance(child, Raw) or isinstance(child, Tag):
                return child.to_JSON()
            return child

        return merge_dict(
            {
                "tag_name": self.__tag_name,
                "children": list(map(format_child, self.__children)),
            },
            self.__attrs,
        )

    def to_PDom(self):
        from .PDom import PDom

        return PDom(self)

    def to_print(self) -> None:
        print(self.__str__())

    @abstractmethod
    def to_save(self, path: str, header: str) -> None:
        pass
