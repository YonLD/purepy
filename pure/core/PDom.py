from typing import List, Union

from .Dom import Dom
from .Raw import Raw
from .Tag import Tag


class PDom(Dom):
    def __init__(self, tag: Tag):
        super().__init__()
        self._tag_name = tag.get_tag_name()
        self.__self_close = tag.get_self_close()
        self._attrs = tag.get_attrs()
        self.children: List[Union["PDom", Raw, str]] = list(
            map(
                lambda child: PDom(child) if isinstance(child, Tag) else child,
                tag.get_children(),
            )
        )

    def __str__(self) -> str:
        attrs = self.__build_attrs_str()
        attrs = "" if not attrs else " " + attrs
        if self.__self_close:
            return "<{}{} />".format(self._tag_name, attrs)

        content = self.__build_children_str()
        return "<{}{}>{}</{}>".format(self._tag_name, attrs, content, self._tag_name)

    def __build_attrs_str(self) -> str:
        attrs = []
        for key, value in self._attrs.items():
            attrs.append(self.__build_attr_str(key, value))
        return " ".join(attrs)

    def __build_attr_str(self, key: str, value: str) -> str:
        return '{}="{}"'.format(key, value)

    def __build_children_str(self) -> str:
        children = list(map(lambda child: str(child), self.children))
        return "".join(children)
