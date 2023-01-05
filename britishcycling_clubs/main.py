"""
Functions to retrieve club member counts
"""

import time
from typing import Dict

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

PROFILE_BASE_URL = "https://www.britishcycling.org.uk/club/profile/"
MANAGER_BASE_URL = "https://www.britishcycling.org.uk/uac/connect?success_url=/dashboard/club/membership?club_id="
INTER_PAGE_DELAY = 5


def get_private_member_counts(
    club_id: str, username: str, password: str
) -> Dict[str, int]:
    """
    Determine how many active, pending and expired members from the club manager page.

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
    time.sleep(INTER_PAGE_DELAY)
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


def get_public_member_count(club_id: str) -> int:
    """
    Return the 'Total club members' count from the club's profile page.

    Parameters
    ----------
    club_id : str
        From the URL used to access club pages.

    Returns
    -------
    int
        Total members count

    """

    profile_page = requests.get(f"{PROFILE_BASE_URL}{club_id}/")
    soup = BeautifulSoup(profile_page.content, "html.parser")
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
