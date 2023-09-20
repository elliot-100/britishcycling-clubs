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

Not yet available at PyPI. Install from GitHub, e.g:

`pip install git+https://github.com/elliot-100/britishcycling-clubs.git#egg=britishcycling-clubs`

Or for a specific version:

`pip install git+https://github.com/elliot-100/britishcycling-clubs.git@v0.0.3#egg=britishcycling-clubs`

Some functions use [Playwright](https://playwright.dev/python/) to automate a 
headless Chromium browser. Ths needs to be installed:

`playwright install chromium`

## Example scripts

You'll need to copy `config_dist.ini`, rename to `config.ini` and populate it with club
ID and (optionally) credentials.

`example_public_club_info.py` loads club ID from `config.ini`. It then retrieves and
prints the club name and 'total member count' from the club's public profile page. 
Note that 'total member count' isn't necessarily a live value.

`example_private_member_counts.py` loads  club ID and credentials from `config.ini`.
It then retrieves and prints the number of active, expired and new/pending club member
counts from the club's Club Manager pages. This takes about 10s.

