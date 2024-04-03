from abc import ABC, abstractmethod
from typing import Union, List, Dict
from .Raw import Raw

class Tag(ABC):
    def __init__(self, tag_name: str):
        self.__tag_name = tag_name;
        self.__attrs: Dict[str, str] = {}
        self.__children: List[Union[str, Raw, 'Tag']] = []
        self.__self_close = False

    def __call__(self, *args: Union[str, Raw, 'Tag']):
        self.__append_children(list(args))
        return self

    def __str__(self):
        return str(self.to_PDom())

    def __getattr__(self, key: str):
        def missing_method(*args: str):
            args = list(args)
            if not args:
                raise Exception("'{}()' accepts one parameter. '{}()->{}() is invalid.'".format(key, self.__tag_name, key))
            if len(args) != 1:
                raise Exception("'{}()' only accepts one parameter. '{}()->{}({}) is invalid.'".format(key, self.__tag_name, key, ','.join(args)))
            self.__set_attr(key, args[0])
            return self

        return missing_method

    def class_name(self, value: str):
        self.__set_attr('class', value)
        return self

    def htmlFor(self, value: str):
        self.__set_attr('for', value)
        return self

    def get_self_close(self):
        return self.__self_close

    def set_self_close(self, value: bool):
        self.__self_close = value
        if self.__self_close and bool(self.__children):
            raise Exception("Self-closing element '{}' cannot have child elements.".format(self.__tag_name))
        return self

    def get_tag_name(self):
        return self.__tag_name

    def get_attrs(self):
        return self.__attrs

    def get_attr(self, key: str):
        return self.__attrs.get(key)

    def set_attrs(self, props: Dict[str, Union[str, bool, None]]):
        if not props:
            return self
        for key, value in props.items():
            self.__set_attr(key, value)
        return self

    def set_attr_by_cb(self, key: str, callback: callable):
        value = callback(self.get_attr(key))
        if (value is None and key in self.__attrs):
            del self.__attrs[key]
        else:
            self.__attrs[key] = value


    def __set_attr(self, key: str, value: Union[str, bool, None]):
        if value is None:
            return
        if not key:
            raise Exception("Element '{}' attribute name cannot be empty '{}'.".format(self.__tag_name, key))
        key = key.replace('_', '-')
        if isinstance(value, bool):
            if value == False:
                return
            value = key
        self.__attrs[key] = str(value)

    def get_children(self):
        return self.__children

    def __append_children(self, children: List[Union[str, Raw, 'Tag']]):
        if not children:
            return
        for i in range(len(children)):
            self.__append_child(children[i])


    def __append_child(self, child: Union[str, Raw, 'Tag']):
        if child is None:
            return
        if isinstance(child, list):
            self.__append_children(child)
            return
        if isinstance(child, str) or isinstance(child, Raw) or isinstance(child, Tag):
            self.__children.append(child)
            return
        self.__children.append(str(child))

    def to_JSON(self):
        def merge_dict(dict1: Dict, dict2: Dict):
            dict1.update(dict2)
            return dict1

        def format_child(child: Union[Tag, Raw, str]):
            return child.to_JSON() if (isinstance(child, Raw) or isinstance(child, Tag)) else child

        return merge_dict({
            'tag_name': self.__tag_name,
            'children': list(map(format_child, self.__children))
        }, self.__attrs)

    def to_PDom(self):
        from .PDom import PDom
        return PDom(self)

    def to_print(self):
        print(self.__str__())

    @abstractmethod
    def to_save(self, path: str, header: str) -> None:
        pass
