"""Example script to get public club info.

Loads club ID from `config.ini`, retrieves and prints info.
"""

import configparser
import pprint
from pathlib import Path

import britishcycling_clubs as bc

CONFIG_FILE = "config.ini"

config = configparser.ConfigParser()
config_filepath = Path(__file__).with_name(CONFIG_FILE)
with Path.open(config_filepath, encoding="utf-8") as file:
    config.read_file(file)

info = bc.get_profile_info(config["club"]["id"])
pprint.pprint(info)
