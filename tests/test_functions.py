"""Tests for functions."""
import pytest
from bs4 import BeautifulSoup

from britishcycling_clubs import (
    _get_club_name_from_profile,
    _get_total_members_from_profile,
    _process_member_counts,
)

# Partial extract from actual page
PROFILE_PAGE_EXTRACT = """
        <html>
        
        <h1 class="article__header__title-body__text">My Cycling Club</h1>
    
        <div class="tabs__content" id="about">
        <h2>Club Information</h2>
        <div class="grid-tablet-wrap grid-tablet-wide-wrap grid-desktop-wrap">
        <div class="grid-tablet-col-full grid-tablet-wide-col-1-2 grid-desktop-col-1-2">
        <p>
        <b>Club type:</b> Club Commercial<br/>
        <b>Affiliated: </b>31/12/2023<br/>
        <b>Affilation status:</b> Active </p>
        <p><b>Total club members:</b> 42<br/></p>
        </div>

        </html>
"""


def test__get_club_name_from_profile__happy_path() -> None:
    """Test that club name is returned from 'profile' soup."""
    profile_soup = BeautifulSoup(PROFILE_PAGE_EXTRACT)
    assert _get_club_name_from_profile(profile_soup) == "My Cycling Club"


def test__get_total_members_from_profile__happy_path() -> None:
    """Test that total members count is returned from 'profile' soup."""
    profile_soup = BeautifulSoup(PROFILE_PAGE_EXTRACT)
    assert _get_total_members_from_profile(profile_soup) == 42


def test__process_member_counts__happy_path() -> None:
    """Test that raw values are converted to ints."""
    raw_counts = {
        "active": "123",
        "pending": "",
        "expired": "67",
    }
    assert _process_member_counts(raw_counts) == {
        "active": 123,
        "pending": 0,
        "expired": 67,
    }


def test__process_member_counts__blank_active_count_raises_exception() -> None:
    """Test that ValueError is raised if active is blank."""
    raw_counts = {
        "active": "",
        "pending": "8",
        "expired": "67",
    }
    with pytest.raises(ValueError):
        _process_member_counts(raw_counts)
