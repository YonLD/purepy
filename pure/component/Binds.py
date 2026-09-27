from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class Binds:
    """Declares the bindings a prepare() closure or a bindings helper returns.

    The returned dict literal of a prepare() hook is what binds the template,
    and `pure check` reads its keys when it is one dict literal. A hook that
    builds its bindings in steps — or merges them from a service — leaves the
    checker nothing to read, so the keys are declared instead:

        register(PricingHeader(...),
            factory=lambda: Compile.shape(...),
            prepare=Binds('title', 'desc')(lambda: PricingService.pricing())
        )

    The declared keys are what the checker compares against the template: a
    required slot no declared key covers is an error, as is a declared key the
    template does not read. The declaration is read by `pure check` only and
    never takes part in rendering.
    """

    keys: Tuple[str, ...] = field(default_factory=tuple)

    def __init__(self, *keys: str):
        object.__setattr__(self, "keys", tuple(keys))

    def __call__(self, prepare):
        """Attach the declaration to a prepare() callable and return it."""
        setattr(prepare, "binds", self)
        return prepare
