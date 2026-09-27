from typing import TYPE_CHECKING, Any, Dict, Optional

from ..core.ShapeContract import ShapeContract
from ..core.Tag import Tag

if TYPE_CHECKING:
    from .Renderer import Renderer


class Shape(ShapeContract):
    def __init__(self, tree: Tag):
        self.__tree = tree
        self.__renderer: Optional[Renderer] = None

    def __call__(self, data: Dict[str, Any]) -> str:
        return self.compile().render(data)

    def compile(self) -> "Renderer":
        if self.__renderer is None:
            from .Compile import Compile

            self.__renderer = Compile.renderer(self.__tree)

        return self.__renderer

    def id(self) -> str:
        from .Internal.ShapeIndex import ShapeIndex

        return ShapeIndex.of(self.__tree).id()

    def print(self, data: Dict[str, Any]) -> None:
        print(self.compile().render(data))

    def save(self, path: str, data: Dict[str, Any], header: Optional[str] = None):
        rendered = self.compile().render(data)
        if header is None:
            header = (
                self.__tree.documentHeader()
                if hasattr(self.__tree, "documentHeader")
                else ""
            )
        with open(path, "w") as f:
            f.write(header + rendered)

    def tree(self) -> Tag:
        return self.__tree
