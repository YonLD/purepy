from typing import Optional
from .SlotKind import SlotKind
from .ShapeContract import ShapeContract


class Slot:
    def __init__(
        self,
        kind: SlotKind,
        name: str,
        shape=None,
        is_required=True,
        default_value=None,
        else_shape=None,
    ):
        self.kind = kind
        self.name = name
        self.shape = shape
        self.is_required = is_required
        self.default_value = default_value
        self.else_shape = else_shape

    @staticmethod
    def value(name: str) -> "Slot":
        return Slot(SlotKind.Value, name, None, True, None)

    @staticmethod
    def raw(name: str) -> "Slot":
        return Slot(SlotKind.Raw, name, None, True, None)

    @staticmethod
    def child(name: str, shape: ShapeContract) -> "Slot":
        return Slot(SlotKind.Child, name, shape, True, None)

    @staticmethod
    def each(name: str, shape: ShapeContract) -> "Slot":
        return Slot(SlotKind.Each, name, shape, True, None)

    @staticmethod
    def if_(
        name: str, then: ShapeContract, else_shape: Optional[ShapeContract] = None
    ) -> "Slot":
        return Slot(SlotKind.If, name, then, False, False, else_shape)

    def required(self, required=True) -> "Slot":
        if self.kind == SlotKind.If:
            raise TypeError(
                "slot '{}' is a condition slot; required() does not apply.".format(
                    self.name
                )
            )
        return Slot(
            self.kind,
            self.name,
            self.shape,
            required,
            self.default_value,
            self.else_shape,
        )

    def default(self, value) -> "Slot":
        if self.kind == SlotKind.If:
            raise TypeError(
                "slot '{}' is a condition slot; default() does not apply.".format(
                    self.name
                )
            )
        if not self._is_value_type(value):
            raise TypeError(
                "slot '{}' default must be None, a scalar or an array of value types.".format(  # noqa: E501
                    self.name
                )
            )
        return Slot(self.kind, self.name, self.shape, False, value, self.else_shape)

    @staticmethod
    def _is_value_type(value) -> bool:
        if isinstance(value, list):
            return all(Slot._is_value_type(item) for item in value)
        return value is None or isinstance(value, (int, float, str, bool))
