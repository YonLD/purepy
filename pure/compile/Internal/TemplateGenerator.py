from typing import List, Optional

from ...core.Tag import Tag
from .CodeGenerator import CodeGenerator


class TemplateGenerator:
    """Generates the Python source of a compiled artifact.

    The artifact is a `pure_body(data)` function that renders the tree through
    the same runtime helpers the in-process renderer uses, so an artifact and a
    `Shape` produce byte-identical output:

        from pure.compile.Internal.SlotRuntime import SlotRuntime

        def pure_body(data):
            out = []
            out.append('<' + 'div')
            ...
            return ''.join(out)
    """

    NAME = "pure_body"

    @staticmethod
    def source(tree: Tag) -> str:
        return CodeGenerator.function(TemplateGenerator.NAME, tree)

    @staticmethod
    def imports(source: Optional[str] = None) -> List[str]:
        return CodeGenerator.imports()
