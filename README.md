# britishcycling-clubs

## About

**Unofficial, not affiliated or endorsed by British/Scottish/Welsh Cycling.**

Library to automate aspects of British Cycling's Club Management Tool, in order to
simplify administration for clubs using it. It probably works for Scottish/Welsh
Cycling clubs too, but this hasn't been tested.


Priority is to enable useful email reports/notifications to club administrators.

Relies on [Selenium](https://www.selenium.dev/) to automate a headless Chrome
browser.

## Prerequisites

- Ensure Chrome and compatible ChromeDriver executable are installed, and ChromeDriver 
executable is on the system PATH. Originally intended to be deployed on the
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

## Example script

`example.py` loads credentials from `config.ini` (you'll need to copy, rename and
populate `config_dist.ini`). It then retrieves and prints the number of active,
expired and new/pending club member counts. This takes about 10s.
