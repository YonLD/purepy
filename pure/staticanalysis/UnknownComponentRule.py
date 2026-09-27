import ast
from typing import Any, Dict, List

from ..core.Suggestion import Suggestion
from .ComponentCallCollector import ComponentCallCollector
from .RegistryCallCollector import RegistryCallCollector


class UnknownComponentRule:
    """Reports a ``component('X')`` / ``Registry.component('X')`` whose literal name
    no analysed ``register(Icon(...))`` or ``Registry.register()`` declares: the
    typo that otherwise only explodes at render time.

    Needs a full-project run (collected data arrives after the last file) and
    is disabled for single-file runs via ``is_only_files_analysis()``.
    """

    IDENTIFIER = "purepy.unknownComponent"

    def get_node_type(self) -> type:
        return ast.Module

    def process_node(self, node: ast.Module, scope: Any) -> List[Dict[str, Any]]:
        if scope.is_only_files_analysis():
            return []

        registered: Dict[str, bool] = {}
        calls: List[Dict[str, Any]] = []

        for collector_class in (ComponentCallCollector, RegistryCallCollector):
            for entries in scope.get_collected_data(collector_class):
                for entry in entries:
                    if entry["kind"] == "registered":
                        registered[entry["name"]] = True
                        continue

                    calls.append(entry)

        if not registered:
            return []

        known = list(registered.keys())
        errors: List[Dict[str, Any]] = []

        for call in calls:
            if call["name"] in registered:
                continue

            nearest = Suggestion.nearest(call["name"], known)
            hint = f" (did you mean '{nearest}'?)" if nearest else ""

            errors.append(
                {
                    "message": f"The component '{call['name']}' is not registered{hint}.",  # noqa: E501
                    "identifier": self.IDENTIFIER,
                    "file": call["file"],
                    "line": call["line"],
                }
            )

        return errors
