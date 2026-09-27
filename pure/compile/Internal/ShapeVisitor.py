from abc import ABC, abstractmethod
from typing import Any, Dict, Union

from ...core.Slot import Slot
from ...core.Raw import Raw
from ...core.Tag import Tag


class ShapeVisitor(ABC):
    @abstractmethod
    def tag_open(self, tag: Tag, path: str, export: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def attribute(self, key: str, value: Union[str, Slot], slot_path: str) -> None:
        pass

    @abstractmethod
    def tag_self_close(self) -> None:
        pass

    @abstractmethod
    def content_start(self) -> None:
        pass

    @abstractmethod
    def tag_close(self, tag_name: str) -> None:
        pass

    @abstractmethod
    def text(self, text: str) -> None:
        pass

    @abstractmethod
    def raw(self, raw: Raw) -> None:
        pass

    @abstractmethod
    def slot_enter(self, slot: Slot, slot_path: str) -> None:
        pass

    @abstractmethod
    def slot_branch(self, label: Union[str, int]) -> None:
        pass

    @abstractmethod
    def slot_leave(self, slot: Slot, slot_path: str) -> None:
        pass
