from enum import Enum


class SlotKind(Enum):
    Value = "value"
    Raw = "raw"
    Child = "child"
    Each = "each"
    If = "if"
