import os
from typing import TYPE_CHECKING, Dict, Optional

from ..core.Tag import Tag
from ..core.DevMode import DevMode
from .Shape import Shape

if TYPE_CHECKING:
    from .Renderer import Renderer


class Compile:
    CACHE_VERSION = 1

    # Generated sources memoized per shape fingerprint, so a tree rebuilt in the
    # same process reuses its code. The budget is MEMO_BYTES unless
    # PURE_COMPILE_MEMO_BYTES overrides it; 0 disables the memo.
    MEMO_BYTES = 4194304
    _sources: Dict[str, str] = {}
    _memo_bytes = 0

    _generation = 0
    _cache_path = None

    @staticmethod
    def shape(shape: Tag) -> Shape:
        # Imported here, not at module scope: `Internal/__init__` imports
        # ShapeIndex, which imports this module back.
        from .Internal.ShapeGuard import ShapeGuard

        ShapeGuard.check()

        return Shape(shape)

    @staticmethod
    def toShape(result) -> Optional[Shape]:
        if isinstance(result, Shape):
            return result
        if isinstance(result, Tag):
            return Shape(result)

        return None

    @staticmethod
    def cachePath(dir):
        """Point the on-disk renderer cache at a directory.

        The directory is validated the way purephp validates it: it must not
        be writable by group or others, and it must be writable at all.
        """
        if dir is None:
            Compile._cache_path = None
            return None

        from .Internal.RendererCache import RendererCache

        Compile._cache_path = RendererCache.prepare(dir)
        return Compile._cache_path

    @staticmethod
    def clearCache() -> int:
        """Remove this library's cache files, leaving foreign files alone."""
        if Compile._cache_path is None:
            return 0

        from .Internal.RendererCache import RendererCache

        return RendererCache.clear(Compile._cache_path)

    @staticmethod
    def flush():
        Compile._generation += 1
        Compile._sources = {}
        Compile._memo_bytes = 0

    @staticmethod
    def guard(enabled=True):
        DevMode.enable(enabled)

    @staticmethod
    def generation() -> int:
        return Compile._generation

    @staticmethod
    def memoLimit() -> int:
        raw = os.environ.get("PURE_COMPILE_MEMO_BYTES", "")

        if raw == "":
            return Compile.MEMO_BYTES

        try:
            return int(raw)
        except ValueError:
            return Compile.MEMO_BYTES

    @staticmethod
    def memoize(id: str, source: str) -> None:
        """Keep a generated source, dropping the oldest entries over budget."""
        limit = Compile.memoLimit()

        if limit <= 0 or id in Compile._sources:
            return

        Compile._sources[id] = source
        Compile._memo_bytes += len(source)

        while Compile._memo_bytes > limit and Compile._sources:
            oldest = next(iter(Compile._sources))
            Compile._memo_bytes -= len(Compile._sources.pop(oldest))

    @staticmethod
    def memoized(id: str) -> Optional[str]:
        return Compile._sources.get(id)

    @staticmethod
    def renderer(tree: Tag) -> "Renderer":
        import os

        from .Internal.CodeGenerator import CodeGenerator
        from .Internal.ShapeIndex import ShapeIndex
        from .Internal.RootSlots import RootSlots
        from .Internal.RendererCache import RendererCache
        from .Renderer import Renderer

        index = ShapeIndex.of(tree)
        slots = RootSlots.of(tree)
        id = index.id()

        # Disk cache first, then the in-process memo, then compile.
        disk = None

        if Compile._cache_path is not None:
            disk = RendererCache.load(
                os.path.join(Compile._cache_path, id + ".py"), id, slots
            )

            if disk is not None:
                return disk

        source = Compile.memoized(id)

        if source is not None:
            renderer = Renderer(source, id, slots)
        else:
            renderer = CodeGenerator.compile(tree, index, slots)

            if renderer.source is not None:
                Compile.memoize(id, renderer.source)

        if Compile._cache_path is not None and renderer.source is not None:
            RendererCache.write(
                os.path.join(Compile._cache_path, id + ".py"), renderer.source, id
            )

        return renderer
