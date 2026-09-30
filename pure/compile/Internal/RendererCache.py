import os
import re
import sys
import tempfile
from typing import Dict, List, Optional

from ..Compile import Compile
from ..Renderer import Renderer


class RendererCache:
    HEADER_PREFIX = "# purepy-shape "

    @staticmethod
    def prepare(dir: str) -> str:
        if not os.path.isdir(dir):
            try:
                os.makedirs(dir, mode=0o700, exist_ok=True)
            except OSError:
                if not os.path.isdir(dir):
                    raise ValueError(
                        "compile cache directory '{}' could not be created.".format(dir)
                    )

        try:
            info = os.stat(dir)
            perms = info.st_mode & 0o777
            owner = info.st_uid
        except OSError:
            # An unreadable directory cannot be vetted either; the writability
            # check below is what reports it.
            perms = 0
            owner = os.getuid()

        if perms & 0o022:
            raise ValueError(
                "compile cache directory '{}' must not be writable by group or others; use a private directory such as 0700.".format(  # noqa: E501
                    dir
                )
            )

        if owner != os.getuid():
            # A private mode is no protection on a directory another user owns:
            # they can replace what is inside it between two compiles. This is
            # the owner check purephp runs after the mode check.
            raise ValueError(
                "compile cache directory '{}' is not owned by the current user.".format(  # noqa: E501
                    dir
                )
            )

        if not os.access(dir, os.W_OK):
            raise ValueError(
                "compile cache directory '{}' is not writable.".format(dir)
            )

        return dir.rstrip("/\\")

    @staticmethod
    def clear(dir: str) -> int:
        removed = 0

        for filename in os.listdir(dir):
            if not filename.endswith(".php") and not filename.endswith(".py"):
                continue

            path = os.path.join(dir, filename)

            try:
                with open(path, "r") as f:
                    header = f.read(len(RendererCache.HEADER_PREFIX))
            except OSError:
                continue

            if header != RendererCache.HEADER_PREFIX:
                continue

            try:
                os.unlink(path)
                removed += 1
            except OSError:
                pass

        return removed

    @staticmethod
    def load(
        file: str, id: str, slots: Optional[List[str]] = None
    ) -> Optional[Renderer]:
        try:
            with open(file, "r") as f:
                contents = f.read()
        except OSError:
            return None

        py_version = "{}.{}".format(sys.version_info[0], sys.version_info[1])
        pattern = r"\A# purepy-shape id=([0-9a-f]{40}) v=(\d+) py=([0-9]+\.[0-9]+)\n"
        match = re.match(pattern, contents)

        if (
            match is None
            or match.group(1) != id
            or int(match.group(2)) != Compile.CACHE_VERSION
            or match.group(3) != py_version
        ):
            try:
                os.unlink(file)
            except OSError:
                pass
            return None

        namespace: Dict = {}
        try:
            exec(contents, namespace)
        except Exception:
            try:
                os.unlink(file)
            except OSError:
                pass
            return None

        closure = namespace.get("render")

        if not callable(closure):
            try:
                os.unlink(file)
            except OSError:
                pass
            return None

        # The cached file stores the whole module behind a header line, so the
        # header is dropped before the source is handed back with the callable:
        # a renderer loaded from disk stays byte-identical to a freshly compiled
        # one, the way purephp's `new Renderer($closure, $body, ...)` does.
        return Renderer(contents[match.end() :], id, slots, render_fn=closure)

    @staticmethod
    def write(file: str, source: str, id: str) -> None:
        py_version = "{}.{}".format(sys.version_info[0], sys.version_info[1])
        # `source` is a whole generated module and already opens with
        # `def render(data):`, so the header is the only thing prepended here;
        # adding a second function head would nest the body at column zero and
        # make the file unimportable.
        body = source if source.endswith("\n") else source + "\n"
        contents = (
            RendererCache.HEADER_PREFIX
            + "id={} v={} py={}\n".format(id, Compile.CACHE_VERSION, py_version)
            + body
        )

        dir_name = os.path.dirname(file)
        fd, tmp = tempfile.mkstemp(prefix="shape-", dir=dir_name)

        try:
            with os.fdopen(fd, "w") as f:
                f.write(contents)

            os.chmod(tmp, 0o600)

            # The temp file lives in the target directory, so the rename is
            # atomic and replaces any previous entry. It raises on failure,
            # which is what the cleanup below is for.
            os.rename(tmp, file)
        except OSError:
            try:
                os.unlink(tmp)
            except OSError:
                pass
