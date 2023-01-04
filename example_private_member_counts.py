"""
Example script: loads credentials from `config.ini`, retrieves and prints club member
counts.
"""

import configparser
from pathlib import Path

import britishcycling_clubs.main as bc

CONFIG_FILE = "config.ini"

config = configparser.ConfigParser()
config_filepath = Path(__file__).with_name(CONFIG_FILE)
config.read_file(open(config_filepath))


member_counts = bc.get_private_member_counts(
    config["club"]["id"], config["club"]["username"], config["club"]["password"]
)

print(f"{member_counts['active']=}")
print(f"{member_counts['pending']=}")
print(f"{member_counts['expired']=}")
