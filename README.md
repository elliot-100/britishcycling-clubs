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
to be installed:

`playwright install chromium`

If you're installing in e.g. a bare-bones server/CI environment, you'll probably be 
prompted to install system dependencies, which you can do with:

`playwright install-deps chromium`

See also https://playwright.dev/python/docs/browsers#install-system-dependencies


## Usage


### Get member counts from a club's Club Manager pages

```
def get_manager_member_counts(
    club_id: str,
    username: str,
    password: str,
    manager_page_load_delay: int = 5,
) -> dict[str, int]:
```
Get numbers of active, new, expired members from the club manager page.

Specifically, returns the counts from these tabs:

- Active Club Members
- New Club Subscriptions
- Expired Club Members

This takes about 10s.

Example script `example_manager_member_counts.py` loads club ID and credentials from
`config.ini` (you'll need to copy `config_dist.ini`, populate and rename to 
`config.
ini`). It then retrieves and prints the number of active, expired and new/pending 
club member counts from the club's Club Manager pages. 


### Get info from a club's profile page

```
get_profile_info(club_id: str) -> dict[str, int | str]
```
Return information from the club's public profile page; doesn't require login.

Specifically, returns these values:

- Club name
- Total club members

Example script `example_profile_info.py` loads club ID from `config.ini` (you'll
need to copy `config_dist.ini`, populate club ID only and rename).  It 
then retrieves and prints the club name and total member count.
