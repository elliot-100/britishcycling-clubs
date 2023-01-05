# britishcycling-clubs

## About

**Unofficial, not affiliated or endorsed by British/Scottish/Welsh Cycling.**

Library to automate aspects of British Cycling's Club Management Tool, in order to
simplify administration for clubs using it. It probably works for Scottish/Welsh
Cycling clubs too, but this hasn't been tested.

Priority is to read data in order to create reports/notifications to club
administrators.

## Prerequisites

- Some functions use [Selenium](https://www.selenium.dev/) to automate a headless Chrome 
browser, so needs Chrome and compatible ChromeDriver executable installed, and 
ChromeDriver executable on the system PATH. Originally intended to be deployed on the
[PythonAnywhere](https://www.pythonanywhere.com/) platform, which covers this
requirement out-of-the box.

- Credentials for a club using the Club Management Tool

## Installation

Not yet available at PyPI. Install from GitHub, e.g:

`
pip install git+https://github.com/elliot-100/britishcycling-clubs.git#egg=britishcycling-clubs
`

Or for a specific version:

`
pip install git+https://github.com/elliot-100/britishcycling-clubs.git@v0.0.3#egg=britishcycling-clubs
`

## Example scripts

You'll need to copy `config_dist.ini`, rename to `config.ini` and populate.

`example_public_club_info.py` loads club ID from `config.ini`. It then retrieves and
prints the club name and total member count from the club's public profile page.

`example_private_member_counts.py` loads  club ID and credentials from `config.ini`.
It then retrieves and prints the number of active, expired and new/pending club member
counts from the club's Club Manager pages. This takes about 10s.


