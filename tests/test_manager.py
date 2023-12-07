"""Tests for 'manager' functions."""
import pytest

from britishcycling_clubs import _process_manager_member_counts


def test__process_manager_member_counts__happy_path() -> None:
    """Test that raw values are converted to ints."""
    raw_counts = {
        "active": "123",
        "pending": "",
        "expired": "67",
    }
    assert _process_manager_member_counts(raw_counts) == {
        "active": 123,
        "pending": 0,
        "expired": 67,
    }


def test__process_manager_member_counts__blank_active_count_raises_exception() -> None:
    """Test that ValueError is raised if active is blank."""
    raw_counts = {
        "active": "",
        "pending": "8",
        "expired": "67",
    }
    with pytest.raises(ValueError):
        _process_manager_member_counts(raw_counts)
