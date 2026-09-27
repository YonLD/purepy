"""`CompileException`, re-exported at the namespace root it is thrown from.

The class itself lives beside the compiler internals that raise it; this module
is the `Compile\\CompileException` path callers import.
"""

from .Internal.CompileException import CompileException

__all__ = ["CompileException"]
