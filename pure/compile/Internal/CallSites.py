import ast
import os
import re
from typing import Dict, List, Optional


class CallSites:
    @staticmethod
    def of(file: str, names: List[str]) -> List[Dict]:
        if not names or not os.path.isfile(file):
            return []

        with open(file) as f:
            source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        known = set(names)

        parents: Dict[int, ast.AST] = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parents[id(child)] = node

        sites: List[Dict] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            parent = parents.get(id(node))
            if (
                isinstance(parent, ast.Call)
                and isinstance(parent.func, ast.Attribute)
                and parent.func.value is node
            ):
                continue

            site = CallSites.__scan_chain(node, known)
            if site is not None:
                sites.append(site)

        return sites

    @staticmethod
    def __scan_chain(root: ast.Call, known: set) -> Optional[Dict]:
        name: Optional[str] = None
        props: Dict[str, bool] = {}
        items: Dict[str, List[Dict[str, bool]]] = {}
        dynamic = False

        node = root
        while isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                prop = node.func.attr
                if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", prop):
                    break

                if CallSites.__has_spread(node):
                    dynamic = True
                else:
                    props[prop] = True
                    literal = CallSites.__items(node)
                    if literal is not None:
                        items[prop] = literal

                node = node.func.value  # type: ignore[assignment]
            else:
                call_name = CallSites.__component_name(node, known)
                if call_name is not None:
                    name = call_name
                break

        if name is None:
            return None

        return {"name": name, "props": props, "items": items, "dynamic": dynamic}

    @staticmethod
    def __component_name(node: ast.Call, known: set) -> Optional[str]:
        if isinstance(node.func, ast.Name):
            if node.func.id == "component":
                if (
                    node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                ):
                    candidate = node.args[0].value
                    if candidate in known:
                        return candidate
            elif node.func.id in known:
                return node.func.id
        return None

    @staticmethod
    def __has_spread(node: ast.Call) -> bool:
        for arg in node.args:
            if isinstance(arg, ast.Starred):
                return True
        for kw in node.keywords:
            if kw.arg is None:
                return True
        return False

    @staticmethod
    def __items(node: ast.Call) -> Optional[List[Dict[str, bool]]]:
        if len(node.args) != 1:
            return None

        arg = node.args[0]
        if not isinstance(arg, ast.List):
            return None

        items: List[Dict[str, bool]] = []
        for element in arg.elts:
            keys = CallSites.__item_keys(element)
            if keys is None:
                return None
            items.append(keys)

        return items

    @staticmethod
    def __item_keys(element: ast.AST) -> Optional[Dict[str, bool]]:
        if not isinstance(element, ast.Dict):
            return None

        keys: Dict[str, bool] = {}
        for key in element.keys:
            if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                return None
            keys[key.value] = True

        return keys
