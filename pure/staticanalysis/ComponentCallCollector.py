import ast
from typing import Any, Dict, Optional


class ComponentCallCollector:
    """Collects component names declared or used through the ``register()`` and
    ``component()`` helper functions: ``kind`` is ``'registered'`` for a definition
    and ``'call'`` for a reference.

    A definition is the call function itself (``register(Icon(...), ...)`` — the
    first-class callable's name is the registered name). A reference is a name
    literal (``component('X')``), a unit path (skipped), or
    ``component(__function__)``, whose name is the enclosing function's name.
    """

    def get_node_type(self) -> type:
        return ast.Call

    def process_node(self, node: ast.Call, scope: Any) -> Optional[Dict[str, Any]]:
        if not isinstance(node.func, ast.Name):
            return None

        called = scope.resolve_name(node.func)
        first = node.args[0] if node.args else None

        if called == "pure.component.register":
            if first is None:
                return None

            value = first

            if (
                isinstance(value, ast.Call)
                and isinstance(value.func, ast.Name)
                and len(value.args) == 1
                and isinstance(value.args[0], ast.Starred)
            ):
                return {
                    "kind": "registered",
                    "name": scope.resolve_name(value.func),
                    "file": scope.get_file(),
                    "line": node.lineno,
                }

            return None

        if called != "pure.component.component":
            return None

        if first is None:
            return None

        value = first

        if isinstance(value, ast.Name) and value.id == "__function__":
            function = scope.get_function()

            if function is None or "{closure" in function.get_name():
                return None

            return {
                "kind": "call",
                "name": function.get_name(),
                "file": scope.get_file(),
                "line": node.lineno,
            }

        if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
            return None

        name = value.value

        if "/" in name or "\\" in name or name.endswith(".php"):
            return None

        return {
            "kind": "call",
            "name": name,
            "file": scope.get_file(),
            "line": node.lineno,
        }
