import time
from typing import Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

MANAGER_BASE_URL = "https://www.britishcycling.org.uk/uac/connect?success_url=/dashboard/club/membership?club_id="
INTER_PAGE_DELAY = 5


def get_member_counts(club_id: str, username: str, password: str) -> Dict[str, int]:
    """
    Determine how many active, pending and expired members.

    This is a slow operation (circa 10s), so get them all in one go.
    From the club manager page, return the values from these tabs:

    - 'Active Club Members'
    - 'New [i.e. pending] Club Subscriptions'
    - 'Expired Club Members'

    Parameters
    ----------
    club_id : str
        From the URL used to access Membership Manager, i.e.
        'https://www.britishcycling.org.uk/dashboard/club/membership?club_id=xxx'

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
