import ast
import inspect
import re
import textwrap
from typing import Dict, List, Optional

# A line that already starts a statement — a `def`, a `return`, a bare
# expression — parses as it is. Only a fragment that begins with a keyword
# argument, such as `prepare=lambda n: {...})`, needs a `x = ` in front.
_STATEMENT_START = re.compile(r"^\s*(def |async def |return |lambda )")
_DECORATOR = re.compile(r"^\s*@")


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
    def __parse(source: str):
        """Parse a `register()` fragment back into a tree, or None.

        `inspect.getsource()` on a lambda returns the whole line it was written
        on, so an inline `prepare=lambda n: {...}` inside a `register(...)` call
        comes back as `prepare=lambda n: {...})`: a fragment that opens no
        bracket and closes one it never opened. Prefixing it turns it into an
        assignment, and the trailing closer is then dropped one at a time until
        the expression parses. The lambda itself is untouched throughout.
        """
        # A decorated `def` already parses, and so does a statement; only a
        # fragment that opens nothing needs the assignment in front of it.
        if _STATEMENT_START.match(source) or _DECORATOR.match(source):
            return Bindings.__try_parse(source)

        return Bindings.__try_parse("x = " + source)

    @staticmethod
    def __try_parse(candidate: str):
        while candidate:
            try:
                return ast.parse(candidate)
            except SyntaxError:
                stripped = candidate.rstrip()
                if not stripped or stripped[-1] not in ")]}":
                    return None
                candidate = stripped[:-1]

        return None

    @staticmethod
    def __function_node(function):
        """Parse the source of `function` back into a node, or None.

        The node is a `def` when the source has one, and otherwise the first
        lambda: a call carrying both `factory=lambda:` and `prepare=lambda:`
        parses into two, and a `def` is never nested inside a lambda the way a
        lambda can be nested inside a call.
        """
        try:
            source = textwrap.dedent(inspect.getsource(function))
        except (OSError, TypeError):
            return None

        tree = Bindings.__parse(source)

        if tree is None:
            return None

        nodes = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))
        ]

        if not nodes:
            return None

        # The target is the node that spans the definition itself: a lambda or
        # a def whose own line range covers the source, rather than any lambda
        # nested inside another expression on the same line.
        for node in nodes:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return node

        return nodes[0]

    @staticmethod
    def __walk_body(func):
        if isinstance(func, ast.Lambda):
            yield from ast.walk(func.body)
        else:
            for stmt in func.body:
                yield from ast.walk(stmt)
