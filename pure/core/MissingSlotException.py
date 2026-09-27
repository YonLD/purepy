from typing import Optional
from .Suggestion import Suggestion


class MissingSlotException(RuntimeError):
    _HINT_KEYS = 8

    @staticmethod
    def for_path(path: str, scope: Optional[dict] = None) -> "MissingSlotException":
        if scope is None:
            scope = {}
        key = MissingSlotException._key_of(path)

        if key in scope:
            return MissingSlotException(
                "slot '{}' is required but was null.".format(path)
            )

        return MissingSlotException(
            "slot '{}' is required but was not provided{}".format(
                path, MissingSlotException._hint(key, scope)
            )
        )

    @staticmethod
    def _hint(key: str, scope: dict) -> str:
        if not scope:
            return "."

        keys = [str(k) for k in scope.keys()]
        nearest = Suggestion.nearest(key, keys)

        if nearest is not None:
            return "; did you mean '{}'?".format(nearest)

        listed = keys[: MissingSlotException._HINT_KEYS]
        listing = ", ".join("'{}'".format(k) for k in listed)

        if len(keys) > MissingSlotException._HINT_KEYS:
            listing += ", ..."

        return "; provided keys: {}.".format(listing)

    @staticmethod
    def _key_of(path: str) -> str:
        position = path.rfind(".")
        return path if position == -1 else path[position + 1 :]
