import os
import warnings
from typing import Set


class DevMode:
    enabled = None
    _warned: Set[str] = set()

    @classmethod
    def enable(cls, enabled=True):
        cls.enabled = enabled

    @classmethod
    def reset(cls):
        cls.enabled = None
        cls._warned = set()

    @classmethod
    def resolve(cls) -> bool:
        env = os.environ.get("PURE_COMPILE_GUARD", "")
        cls.enabled = env in ("1", "true", "True")
        return cls.enabled

    @classmethod
    def mark(cls, subject: str) -> bool:
        if subject in cls._warned:
            return False
        cls._warned.add(subject)
        return True

    @classmethod
    def warn(cls, subject: str, message: str):
        if cls.mark(subject):
            cls.emit(message)

    @classmethod
    def emit(cls, message: str):
        warnings.warn(message, UserWarning, stacklevel=3)
