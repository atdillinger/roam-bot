import pytest

from src.roam_bot.functions import check_if_system_is_wormhole


@pytest.mark.parametrize(
    "system, wh_status", [("J151718", True), ("Jita", False), ("KLMT-W", False)]
)
def test_check_if_system_is_wormhole(system, wh_status):
    assert check_if_system_is_wormhole(system=system) == wh_status
