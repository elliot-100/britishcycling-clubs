"""Tests for 'profile' functions."""

from bs4 import BeautifulSoup

from britishcycling_clubs import club_profile_url
from britishcycling_clubs.profile import (
    _club_name_from_profile,
    _total_members_from_profile,
)


def test_club_profile_url__happy_path() -> None:
    """Test that correct URL is returned."""
    assert (
        club_profile_url("000") == "https://www.britishcycling.org.uk/club/profile/000/"
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


def test__club_name_from_profile__happy_path() -> None:
    """Test that club name is returned from 'profile' soup."""
    profile_soup = BeautifulSoup(
        PROFILE_PAGE_EXTRACT,
        "html.parser",
    )
    assert _club_name_from_profile(profile_soup) == "My Cycling Club"


def test__total_members_from_profile__happy_path() -> None:
    """Test that total members count is returned from 'profile' soup."""
    profile_soup = BeautifulSoup(
        PROFILE_PAGE_EXTRACT,
        "html.parser",
    )
    assert _total_members_from_profile(profile_soup) == 42
