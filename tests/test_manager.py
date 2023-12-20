"""Tests for 'manager' functions."""
import pytest

from britishcycling_clubs.manager import (
    _process_manager_member_counts,
    club_manager_url_via_login,
)


def test_club_manager_url_via_login__happy_path() -> None:
    """Test that correct URL is returned."""
    assert (
        club_manager_url_via_login("000")
        == "https://www.britishcycling.org.uk/uac/connect?success_url=/dashboard/club/membership?club_id=000/"
    )


def test__process_manager_member_counts__happy_path() -> None:
    """Test that raw values are converted to ints."""
    raw_counts = {
        "active": "123",
        "new": "",
        "expired": "67",
    }
    assert _process_manager_member_counts(raw_counts) == {
        "active": 123,
        "new": 0,
        "expired": 67,
    }


def test__process_manager_member_counts__blank_active_count_raises_exception() -> None:
    """Test that ValueError is raised if active is blank."""
    raw_counts = {
        "active": "",
        "new": "8",
        "expired": "67",
    }
    with pytest.raises(ValueError):
        _process_manager_member_counts(raw_counts)
