import pytest

from src.main import _check_if_system_is_wormhole


@pytest.mark.parametrize("system, wh_status", [("J356666", True), ("Jita", False)])
def test_check_if_system_is_wormhole(system, wh_status):
    print("test")
    assert _check_if_system_is_wormhole(system=system) == wh_status
