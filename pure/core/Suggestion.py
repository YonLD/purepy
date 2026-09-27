from typing import List, Optional


class Suggestion:
    @staticmethod
    def nearest(needle: str, candidates: List[str]) -> Optional[str]:
        for candidate in candidates:
            if candidate != needle and Suggestion._one_edit_apart(needle, candidate):
                return candidate
        return None

    @staticmethod
    def _one_edit_apart(a: str, b: str) -> bool:
        len_a = len(a)
        len_b = len(b)

        if len_a == len_b:
            mismatch = -1
            for i in range(len_a):
                if a[i] == b[i]:
                    continue
                if mismatch >= 0:
                    return (
                        mismatch == i - 1
                        and a[mismatch] == b[i]
                        and a[i] == b[mismatch]
                    )
                mismatch = i
            return mismatch >= 0

        if abs(len_a - len_b) != 1:
            return False

        shorter, longer = (a, b) if len_a < len_b else (b, a)
        short_len = len(shorter)
        i = 0
        j = 0
        skipped = False

        while i < short_len and j < len(longer):
            if shorter[i] == longer[j]:
                i += 1
                j += 1
                continue
            if skipped:
                return False
            skipped = True
            j += 1

        return True
