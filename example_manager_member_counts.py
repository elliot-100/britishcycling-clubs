"""Example script to get member counts from the club manager page.

Loads credentials from `config.ini`, retrieves and prints info.
"""

import configparser
from pathlib import Path

import britishcycling_clubs as bc

CONFIG_FILE = "config.ini"

config = configparser.ConfigParser()
config_filepath = Path(__file__).with_name(CONFIG_FILE)
with Path.open(config_filepath, encoding="utf-8") as file:
    config.read_file(file)

member_counts = bc.get_manager_member_counts(
    config["club"]["id"],
    config["club"]["username"],
    config["club"]["password"],
)

print(f"{member_counts['active']=}")
print(f"{member_counts['pending']=}")
print(f"{member_counts['expired']=}")
