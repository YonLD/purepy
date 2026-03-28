from abc import ABC, abstractmethod


class Dom(ABC):
    def __init__(self):
        self._tag_name = ""
        self._attrs = {}
        self.children = []

    @abstractmethod
    def __str__(self) -> str:
        pass
