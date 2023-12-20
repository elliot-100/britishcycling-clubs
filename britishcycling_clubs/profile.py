"""Functions to get info from a club's profile page."""

from typing import TypedDict

import requests
from bs4 import BeautifulSoup, Tag

_PROFILE_BASE_URL = "https://www.britishcycling.org.uk/club/profile/"
_REQUESTS_TIMEOUT = 10  # For `requests` library operations


class ProfileInfo(TypedDict):
    """Return type for `get_profile_info()` function."""

    club_name: str
    total_members: int


def get_profile_info(club_id: str) -> ProfileInfo:
    """Return information from the club's public profile page.

    Parameters
    ----------
    club_id
        From the URL used to access club pages.

    Returns
    -------
    dict[str, str | int]
        keys: 'club_name', 'total_members'
        values: corresponding str or int
    """
    profile_url = club_profile_url(club_id)
    r = requests.get(profile_url, timeout=_REQUESTS_TIMEOUT)
    r.raise_for_status()
    if r.url != profile_url:
        error_message = f"Redirected to unexpected URL {r.url}. Is `club_id` valid?"
        raise ValueError(error_message)
    profile_soup = BeautifulSoup(r.content, "html.parser")
    return {
        "club_name": _club_name_from_profile(profile_soup),
        "total_members": _total_members_from_profile(profile_soup),
    }


def club_profile_url(club_id: str) -> str:
    """Return URL of club's profile page.

    Parameters
    ----------
    club_id
        From the URL used to access club pages.
    """
    return f"{_PROFILE_BASE_URL}{club_id}/"


def _club_name_from_profile(soup: BeautifulSoup) -> str:
    """Return the club's name from profile page soup."""
    club_name_h1 = soup.find("h1", class_="article__header__title-body__text")
    if not club_name_h1:
        error_msg = "Can't find club name heading"
        raise ValueError(error_msg)
    if not isinstance(club_name_h1, Tag):  # type-narrowing
        raise TypeError
    if not isinstance(club_name_h1.string, str):  # type-narrowing
        raise TypeError

    return club_name_h1.string


def _total_members_from_profile(soup: BeautifulSoup) -> int:
    """Return the club's total members count from profile page soup."""
    about_div = soup.find("div", id="about")
    if not about_div:
        error_msg = "Can't find 'about' div"
        raise ValueError(error_msg)
    if not isinstance(about_div, Tag):  # type-narrowing
        raise TypeError

    member_count_label = about_div.find(string="Total club members:")
    if not member_count_label:
        error_msg = "Can't find 'Total club members:'"
        raise ValueError(error_msg)

    member_count_label_outer = member_count_label.parent
    if not isinstance(member_count_label_outer, Tag):  # type-narrowing
        raise TypeError

    member_count_label_outer2 = member_count_label_outer.parent
    if not isinstance(member_count_label_outer2, Tag):  # type-narrowing
        raise TypeError

    strings = list(member_count_label_outer2.strings)
    return int(strings[-1])
