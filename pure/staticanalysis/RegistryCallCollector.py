import ast
from typing import Any, Dict, Optional


class RegistryCallCollector:
    """Collects component names declared or used through the static facade:
    ``kind`` is ``'registered'`` for ``Registry.register('X', ...)`` and ``'call'``
    for ``Registry.component('X')``.
    """

    def get_node_type(self) -> type:
        return ast.Call

    def process_node(self, node: ast.Call, scope: Any) -> Optional[Dict[str, Any]]:
        if not isinstance(node.func, ast.Attribute):
            return None

        if not isinstance(node.func.value, ast.Name):
            return None

        if scope.resolve_name(node.func.value) != "pure.component.Registry":
            return None

        method = node.func.attr
        first = node.args[0] if node.args else None

        if method == "register":
            if (
                first is None
                or not isinstance(first, ast.Constant)
                or not isinstance(first.value, str)
            ):
                return None

            return {
                "kind": "registered",
                "name": first.value,
                "file": scope.get_file(),
                "line": node.lineno,
            }

        if method != "component":
            return None

        if (
            first is None
            or not isinstance(first, ast.Constant)
            or not isinstance(first.value, str)
        ):
            return None

        name = first.value

        if "/" in name or "\\" in name or name.endswith(".php"):
            return None

        return {
            "kind": "call",
            "name": name,
            "file": scope.get_file(),
            "line": node.lineno,
        }
