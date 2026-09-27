from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Tag import Tag


class ShapeContract(ABC):
    @abstractmethod
    def tree(self) -> "Tag":
        pass
