"""
Example script: loads club ID from `config.ini`, retrieves and prints member
counts.
"""

import configparser
from pathlib import Path

import britishcycling_clubs.main as bc

CONFIG_FILE = "config.ini"

config = configparser.ConfigParser()
config_filepath = Path(__file__).with_name(CONFIG_FILE)
config.read_file(open(config_filepath))


member_count = bc.get_public_member_count(config["club"]["id"])
print(member_count)
