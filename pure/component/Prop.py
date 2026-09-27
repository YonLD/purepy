from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Prop:
    slot: Optional[str] = None
    required: Optional[bool] = None
    item: Optional[str] = None
    deprecated: Optional[str] = None
