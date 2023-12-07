"""Module with functions to retrieve information about a club."""

from __future__ import annotations

import logging
import time
from typing import TypedDict

import requests
from bs4 import BeautifulSoup, Tag
from playwright.sync_api import sync_playwright

PROFILE_BASE_URL = "https://www.britishcycling.org.uk/club/profile/"
MANAGER_BASE_URL = "https://www.britishcycling.org.uk/uac/connect?success_url=/dashboard/club/membership?club_id="
REQUESTS_TIMEOUT = 10  # For `requests` library operations

log = logging.getLogger(__name__)


class ClubProfileInfo(TypedDict):
    """Return type for `get_club_profile_info()` function."""

    club_name: str
    total_members: int


def get_club_profile_info(club_id: str) -> ClubProfileInfo:
    """Return information from the club's public profile page.

    Parameters
    ----------
    club_id
        From the URL used to access club pages.

    Returns
    -------
    ClubProfileInfo
    """
    profile_url = f"{PROFILE_BASE_URL}{club_id}/"
    r = requests.get(profile_url, timeout=REQUESTS_TIMEOUT)
    r.raise_for_status()
    if r.url != profile_url:
        error_message = f"Redirected to unexpected URL {r.url}. Is `club_id` valid?"
        raise ValueError(error_message)
    profile_soup = BeautifulSoup(r.content, "html.parser")
    return {
        "club_name": _club_name_from_profile(profile_soup),
        "total_members": _total_members_from_profile(profile_soup),
    }


def _club_name_from_profile(soup: BeautifulSoup) -> str:
    """Return the club's name from profile page soup."""
    club_name_h1 = soup.find("h1", class_="article__header__title-body__text")
    if not club_name_h1:
        raise ValueError("Can't find club name heading")
    if not isinstance(club_name_h1, Tag):  # type-narrowing
        raise TypeError
    if not isinstance(club_name_h1.string, str):  # type-narrowing
        raise TypeError

    return club_name_h1.string


def _total_members_from_profile(soup: BeautifulSoup) -> int:
    """Return the club's total members count from profile page soup."""
    about_div = soup.find("div", id="about")
    if not about_div:
        raise ValueError("Can't find 'about' div")
    if not isinstance(about_div, Tag):  # type-narrowing
        raise TypeError

    member_count_label = about_div.find(string="Total club members:")
    if not member_count_label:
        raise ValueError("Can't find 'Total club members:'")

    member_count_label_outer = member_count_label.parent
    if not isinstance(member_count_label_outer, Tag):  # type-narrowing
        raise TypeError

    member_count_label_outer2 = member_count_label_outer.parent
    if not isinstance(member_count_label_outer2, Tag):  # type-narrowing
        raise TypeError

    strings = list(member_count_label_outer2.strings)
    return int(strings[-1])


def get_manager_member_counts(
    club_id: str,
    username: str,
    password: str,
    manager_page_load_delay: int = 5,
) -> dict[str, int]:
    """Get number of active, pending, expired members from the Club Manager page.

    This is a slow operation (circa 10s), so get them all in one go.
    From the club manager page, return the values from these tabs:

    - 'Active Club Members'
    - 'New [i.e. pending] Club Subscriptions'
    - 'Expired Club Members'

    Parameters
    ----------
    club_id
        From the URL used to access club pages.

    username
        Username

    password
        Password

    manager_page_load_delay
        Time (s) allowed for club manager page to load. Defaults to 5.
        Consider increasing if 'Active member count was zero' exceptions occur.

    Returns
    -------
    dict[str, int]
        keys: 'active', 'pending', 'expired'
        values: corresponding ints

    Raises
    ------
    ValueError if zero 'active members' would be returned, as this probably means
    values hadn't populated correctly.

    """
    club_manager_url = f"{MANAGER_BASE_URL}{club_id}/"

    start_time = time.time()
    _log_info("Started timer for Playwright operations", start_time)

    with sync_playwright() as p:
        _log_info("Launching browser", start_time)
        browser = p.chromium.launch()
        page = browser.new_page()

        # login page
        page.goto(club_manager_url)
        page.locator("id=username2").fill(username)
        page.locator("id=password2").fill(password)
        page.locator("id=login_button").click()
        _log_info("Got club manager page; logging in", start_time)

        # allow time for club manager page to load fully,
        # as page.wait_for_load_state() is ineffective
        _log_info(
            f"Waiting extra {manager_page_load_delay} s for page load",
            start_time,
        )
        time.sleep(manager_page_load_delay)

        raw_member_counts = {
            "active": page.locator("id=members-active-count").inner_text(),
            "pending": page.locator("id=members-new-count").inner_text(),
            "expired": page.locator("id=members-expired-count").inner_text(),
        }

        _log_info("Raw data retrieved", start_time)
        browser.close()
        _log_info("Closed browser", start_time)

        return _process_manager_member_counts(raw_member_counts)


def _process_manager_member_counts(member_counts: dict[str, str]) -> dict[str, int]:
    """Process raw values.

    Values are blank if there aren't any members (although they appear as zeros
    during page load); convert these to 0 and ensure all are ints.

    Raise exception if zero 'active members' value.
    """
    processed_member_counts = {
        key: int(value) if value else 0 for key, value in member_counts.items()
    }
    # Assume an error if zero 'active' value.
    # 'active' appears to be the slowest value to populate.
    # 'pending' will often be genuinely zero; 'expired' could be genuinely zero
    if processed_member_counts["active"] == 0:
        error_message = (
            "Active member count was zero; assuming error. "
            f"{processed_member_counts['active']=}; "
            f"{processed_member_counts['pending']=}; "
            f"{processed_member_counts['expired']=}. "
            "Consider increasing `manager_page_load_delay`."
        )
        raise ValueError(error_message)
    return processed_member_counts


def _log_info(message: str, start_time: float) -> None:
    """Add INFO level log entry, with elapsed time since `start_time`."""
    elapsed_time = time.time() - start_time
    log_message = f"Elapsed: {elapsed_time:.1f} s. {message}"
    log.info(log_message)
