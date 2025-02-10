"""Tests for 'manager' functions."""

import pytest

from britishcycling_clubs.manager_info import ManagerInfo


def test_club_manager_url_via_login__happy_path() -> None:
    """Test that correct URL is returned."""
    # arrange
    club_id = "000"
    # act
    url = ManagerInfo.url_via_login(club_id)
    # act
    assert (
        url
        == "https://www.britishcycling.org.uk/uac/connect?success_url=/dashboard/club/membership?club_id=000/"
    )


def test__process_manager_member_counts__happy_path() -> None:
    """Test that raw values are converted to ints."""
    # arrange
    raw_counts = {
        "active": "123",
        "new": "",
        "expired": "67",
    }
    # act
    counts = ManagerInfo._process_manager_member_counts(raw_counts)
    # assert
    assert counts.active == 123
    assert counts.new == 0
    assert counts.expired == 67


def test__process_manager_member_counts__blank_active_count_raises_exception() -> None:
    """Test that ValueError is raised if active is blank."""
    # arrange
    raw_counts = {
        "active": "",
        "new": "8",
        "expired": "67",
    }
    # act, assert
    with pytest.raises(ValueError, match="Active member count was zero"):
        ManagerInfo._process_manager_member_counts(raw_counts)
