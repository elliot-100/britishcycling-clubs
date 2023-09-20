"""Functions to retrieve information about a club."""

from __future__ import annotations

import time

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from playwright.sync_api import sync_playwright

PROFILE_BASE_URL = "https://www.britishcycling.org.uk/club/profile/"
PROFILE_INTER_PAGE_DELAY = 5

MANAGER_BASE_URL = "https://www.britishcycling.org.uk/uac/connect?success_url=/dashboard/club/membership?club_id="
REQUESTS_TIMEOUT = 10


def get_private_member_counts(
    club_id: str,
    username: str,
    password: str,
) -> dict[str, int]:
    """Get number of active, pending, expired members from the club manager page.

    This is a slow operation (circa 10s), so get them all in one go.
    From the club manager page, return the values from these tabs:

    - 'Active Club Members'
    - 'New [i.e. pending] Club Subscriptions'
    - 'Expired Club Members'

    Parameters
    ----------
    club_id : str
        From the URL used to access club pages.

    username : str
        Username

    password : str
        Password

    Returns
    -------
    dict
        keys: 'active', 'pending', 'expired'
        values: corresponding ints
    """

    club_manager_url = f"{MANAGER_BASE_URL}{club_id}/"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # login page
        page.goto(club_manager_url)
        page.locator("id=username2").fill(username)
        page.locator("id=password2").fill(password)
        page.locator("id=login_button").click()

        # allow time for club manager page to load fully,
        # as page.wait_for_load_state() is ineffective
        time.sleep(PROFILE_INTER_PAGE_DELAY)

        member_counts_raw = {
            "active": page.locator("id=members-active-count").inner_text(),
            "pending": page.locator("id=members-new-count").inner_text(),
            "expired": page.locator("id=members-expired-count").inner_text(),
        }

        browser.close()

        # raw values will be blank if there aren't any members (although they appear
        # as zeros during page load), convert to 0 and ensure ints.
        member_counts = {
            key: 0 if value == "" else int(value)
            for key, value in member_counts_raw.items()
        }

    return member_counts


def get_public_club_info(club_id: str) -> dict[str, int | str]:
    """Return information from the club's public profile page.

    Parameters
    ----------
    club_id : str
        From the URL used to access club pages.

    Returns
    -------
    dict
        key 'club_name' : str
        value : str
        key 'total_members' : str
        value : int
    """
    profile_page = requests.get(
        f"{PROFILE_BASE_URL}{club_id}/",
        timeout=REQUESTS_TIMEOUT,
    )
    profile_soup = BeautifulSoup(profile_page.content, "html.parser")
    return {
        "club_name": get_club_name_from_profile(profile_soup),
        "total_members": get_total_members_from_profile(profile_soup),
    }


def get_club_name_from_profile(soup: BeautifulSoup) -> str:
    """Return the club's name from BeautifulSoup object."""
    club_name_h1 = soup.find("h1", class_="article__header__title-body__text")
    # Ensures unambiguous type is passed
    assert isinstance(club_name_h1, Tag)
    # Ensures unambiguous type is passed
    assert isinstance(club_name_h1.string, str)
    return club_name_h1.string


def get_total_members_from_profile(soup: BeautifulSoup) -> int:
    """Return the club's total members count from BeautifulSoup object."""
    about_div = soup.find("div", id="about")
    # AssertionError is raised if page other than a club profile page is returned
    # e.g. club_id is incorrect; club's profile is offline pending reaffiliation
    # Consider checking URL returned as a more explicit check
    assert isinstance(about_div, Tag)

    # AssertionError raised if string is not found as exact tag content
    member_count_label = about_div.find(string="Total club members:")
    assert isinstance(member_count_label, NavigableString)

    member_count_label_outer = member_count_label.parent
    # Not expected to raise, but ensures unambiguous type is passed
    assert isinstance(member_count_label_outer, Tag)

    member_count_label_outer2 = member_count_label_outer.parent
    # Not expected to raise, but ensures unambiguous type is passed
    assert isinstance(member_count_label_outer2, Tag)

    strings = list(member_count_label_outer2.strings)
    return int(strings[-1])
