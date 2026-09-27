import ast
import inspect
import textwrap
from typing import Dict, List, Optional


class Bindings:
    @staticmethod
    def variables(function) -> Optional[Dict[str, bool]]:
        func = Bindings.__function_node(function)
        if func is None:
            return None

        variables: Dict[str, bool] = {}
        for node in Bindings.__walk_body(func):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                variables[node.id] = True

        return variables

    @staticmethod
    def literalKeys(function) -> Optional[Dict[str, bool]]:
        func = Bindings.__function_node(function)
        if func is None:
            return None

        if isinstance(func, ast.Lambda):
            if not isinstance(func.body, ast.Dict):
                return None
            return Bindings.__dict_keys(func.body)

        returns: List[ast.Return] = []
        for node in Bindings.__walk_body(func):
            if isinstance(node, ast.Return):
                returns.append(node)

        if len(returns) != 1:
            return None

        if not isinstance(returns[0].value, ast.Dict):
            return None

        return Bindings.__dict_keys(returns[0].value)

    @staticmethod
    def __dict_keys(dict_node: ast.Dict) -> Optional[Dict[str, bool]]:
        keys: Dict[str, bool] = {}
        for key in dict_node.keys:
            if key is None:
                return None
            if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                return None
            keys[key.value] = True
        return keys

    @staticmethod
    def __function_node(function):
        try:
            source = inspect.getsource(function)
        except (OSError, TypeError):
            return None

        try:
            tree = ast.parse(textwrap.dedent(source))
        except SyntaxError:
            return None

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                return node

        return None

    @staticmethod
    def __walk_body(func):
        if isinstance(func, ast.Lambda):
            yield from ast.walk(func.body)
        else:
            for stmt in func.body:
                yield from ast.walk(stmt)
