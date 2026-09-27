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
            perms = os.stat(dir).st_mode & 0o777
        except OSError:
            perms = 0

        if perms & 0o022:
            raise ValueError(
                "compile cache directory '{}' must not be writable by group or others; use a private directory such as 0700.".format(  # noqa: E501
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

        body = contents[match.end() :].strip()
        if body.startswith("def "):
            body = body[4:]

        return Renderer(closure, id, slots)

    @staticmethod
    def write(file: str, source: str, id: str) -> None:
        py_version = "{}.{}".format(sys.version_info[0], sys.version_info[1])
        contents = (
            RendererCache.HEADER_PREFIX
            + "id={} v={} py={}\n".format(id, Compile.CACHE_VERSION, py_version)
            + "def render(data):\n"
            + source
            + "\n"
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
