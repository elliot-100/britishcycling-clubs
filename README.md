# britishcycling-clubs


## About

**Unofficial, not affiliated or endorsed by British/Scottish/Welsh Cycling.**

Library to automate aspects of British Cycling's Club Management Tool, in order to
simplify administration for clubs using it. It probably works for Scottish/Welsh
Cycling clubs too, but this hasn't been tested.

Priority is to read data in order to create reports/notifications to club
administrators.


## Prerequisites

- Credentials for a club using the Club Management Tool


## Installation

Install from PyPI, e.g:

`pip install britishcycling-clubs`

Some functions use [Playwright](https://playwright.dev/python/) to automate a headless Chromium browser. This needs
to be installed separately before first use, and after most Playwright updates, e.g.:

`playwright install chromium`

If you're installing in e.g. a bare-bones server/CI environment, you'll probably be 
prompted to install system dependencies, which you can do with e.g.:

`playwright install-deps chromium`

See also https://playwright.dev/python/docs/browsers#install-system-dependencies


## Usage

### Club profile URL

```
britishcycling_clubs.club_profile_url(
    club_id: str
) -> str
```

### Get info from a club's profile

```
britishcycling_clubs.get_profile_info(
    club_id: str
) -> dict[str, int | str]
```
Return information from the club's public profile page; doesn't require login.

Specifically, return a dict with these keys and corresponding values:

- `"club_name"`: Club name
- `"total_members"`: Total club members

Example script `example_profile_info.py` loads club ID from `config.ini` (you'll
need to copy `config_dist.ini`, populate club ID only and rename).
It then retrieves and prints the club name and total member count.


### Club manager URL (via login)

```
britishcycling_clubs.club_manager_url_via_login(
    club_id: str
) -> str
```
URL which redirects to Club Manager URL, via login if needed.


### Get member counts from Club Manager

```
britishcycling_clubs.get_manager_member_counts(
    club_id: str,
    username: str,
    password: str,
    manager_page_load_delay: int = 5,
) -> dict[str, int]:
```
Get numbers of active, new, expired members from the club manager page.

Specifically, return a dict with these keys, and values from badges on corresponding
tabs:

- `"active"`: Active Club Members
- `"expired"`: Expired Club Members
- `"new"`: New Club Subscriptions

This takes about 10s.

Example script `example_manager_member_counts.py` loads club ID and credentials from
`config.ini` (you'll need to copy `config_dist.ini`, populate and rename to 
`config.ini`).
It then retrieves and prints the number of active, expired and new 
club member counts from the club's Club Manager pages. 
