from typing import TYPE_CHECKING, Any, Dict, Optional

from ..core.ShapeContract import ShapeContract
from ..core.Tag import Tag

if TYPE_CHECKING:
    from .Renderer import Renderer


class Shape(ShapeContract):
    def __init__(self, tree: Tag):
        self.__tree = tree
        self.__renderer: Optional[Renderer] = None
        self.__generation = -1

    def __call__(self, data: Dict[str, Any]) -> str:
        return self.compile().render(data)

    def compile(self) -> "Renderer":
        from .Compile import Compile

        generation = Compile.generation()

        # A flushed generation recompiles the tree, so a shape that was mutated
        # after a previous compile is described by code that matches it.
        if self.__renderer is None or self.__generation != generation:
            self.__renderer = Compile.renderer(self.__tree)
            self.__generation = generation

        return self.__renderer

    def id(self) -> str:
        from .Internal.ShapeIndex import ShapeIndex

        return ShapeIndex.of(self.__tree).id()

    def print(self, data: Dict[str, Any]) -> None:
        print(self.compile().render(data))

    def save(
        self, path: str, data: Dict[str, Any], header: Optional[str] = None
    ) -> int:
        """Write the rendered shape to a file and return how many bytes it took.

        The bytes are UTF-8 whatever the locale says, which is also what
        purephp's `save()` reports.
        """
        rendered = self.compile().render(data)
        if header is None:
            header = (
                self.__tree.documentHeader()
                if hasattr(self.__tree, "documentHeader")
                else ""
            )

        with open(path, "wb") as f:
            return f.write((header + rendered).encode("utf-8"))

    def tree(self) -> Tag:
        return self.__tree
