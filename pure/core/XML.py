from typing import Union, Tuple

from .Raw import Raw
from .Tag import Tag


class XML(Tag):
    def __init__(self, tag_name: str, children: Tuple[Union[str, Raw, Tag], ...] = ()):
        super().__init__(tag_name, children)

    def to_save(self, path: str, header: str = '<?xml version="1.0"?>') -> None:
        with open(path, "w") as file:
            file.write(header + str(self.to_PDom()))
