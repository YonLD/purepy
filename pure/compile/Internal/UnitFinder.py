import os
from typing import List

from .ArtifactCompiler import ArtifactCompiler


class UnitFinder:
    @staticmethod
    def discover(path: str) -> List[str]:
        if os.path.isfile(path):
            resolved = os.path.realpath(path)
            ArtifactCompiler.artifactPath(resolved)
            return [resolved]

        if os.path.isdir(path):
            found: List[str] = []

            for root, dirs, files in os.walk(path):
                for filename in files:
                    for suffix in ArtifactCompiler.UNIT_SUFFIXES:
                        if filename.endswith(suffix):
                            found.append(os.path.realpath(os.path.join(root, filename)))
                            break

            if not found:
                suffixes = " or ".join("*" + s for s in ArtifactCompiler.UNIT_SUFFIXES)
                raise ValueError("no {} files found in '{}'.".format(suffixes, path))

            found.sort()
            return found

        raise ValueError("'{}' does not exist.".format(path))
