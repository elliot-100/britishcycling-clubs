"""Example script to get member counts from the club manager page.

Loads credentials from `config.ini`, retrieves and prints info.
"""

import configparser
import logging
import pprint
from pathlib import Path

from britishcycling_clubs import ManagerInfo

CONFIG_FILE = "config.ini"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)
config = configparser.ConfigParser()
config_filepath = Path(__file__).with_name(CONFIG_FILE)
with Path.open(config_filepath, encoding="utf-8") as file:
    config.read_file(file)

member_counts = ManagerInfo.extract(
    config["club"]["id"], config["club"]["username"], config["club"]["password"]
)
pprint.pprint(member_counts)
