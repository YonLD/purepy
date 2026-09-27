import pytest

from pure.component.Registry import Registry
from pure.core.DevMode import DevMode


@pytest.fixture(autouse=True)
def reset_registry():
    Registry.reset()
    DevMode.reset()
    yield
    Registry.reset()
    DevMode.reset()
