# britishcycling-clubs

## About

**Unofficial, not affiliated or endorsed by British/Scottish/Welsh Cycling.**

Library to automate aspects of British Cycling's Membership Manager
system, in order to simplify administration for clubs using it.
It probably works for Scottish/Welsh Cycling clubs too, but this hasn't been tested.


Priority is to enable useful email reports/notifications to club administrators.

Relies on [Selenium](https://www.selenium.dev/) to automate a headless Chrome
browser.

## Prerequisites

- Ensure Chrome and compatible ChromeDriver executable are installed, and ChromeDriver 
executable is on the system PATH. Originally intended to be deployed on the
[PythonAnywhere](https://www.pythonanywhere.com/) platform, which covers this
requirement out-of-the box.

## Example script

`example.py` loads credentials from `config.ini` (populate and rename from
`config_dist.ini`), retrieves and prints club member
counts. This takes about 10s.