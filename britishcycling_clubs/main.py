"""Functions to retrieve information about a club."""

from __future__ import annotations

import time

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # PythonAnywhere requirement
    chrome_options.add_argument("--disable-gpu")  # PythonAnywhere requirement
    chrome_options.add_argument("--no_sandbox")  # PythonAnywhere requirement
    driver = webdriver.Chrome(options=chrome_options)
    action = ActionChains(driver)

    club_url = f"{MANAGER_BASE_URL}{club_id}/"

    # login page
    driver.get(club_url)
    username_field = driver.find_element(By.ID, "username2")
    password_field = driver.find_element(By.ID, "password2")
    login_button = driver.find_element(By.ID, "login_button")

    username_field.send_keys(username)
    password_field.send_keys(password)
    action.click(login_button)
    action.perform()

    # allow time for club manager page to load fully
    time.sleep(PROFILE_INTER_PAGE_DELAY)
    member_counts_raw = {
        "active": driver.find_element(By.ID, "members-active-count").text,
        "pending": driver.find_element(By.ID, "members-new-count").text,
        "expired": driver.find_element(By.ID, "members-expired-count").text,
    }

    # values will be blank if there aren't any members, although they appear
    # as zeros during page load
    member_counts = {
        key: 0 if value == "" else int(value)
        for key, value in member_counts_raw.items()
    }
    driver.quit()
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
