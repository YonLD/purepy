from .Markup import Markup


class Raw(Markup):
    def __init__(self, value: str):
        self._value = value

    @staticmethod
    def of(value: str) -> "Raw":
        return Raw(value)

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value
