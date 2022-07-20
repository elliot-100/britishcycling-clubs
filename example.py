"""
Example script: loads credentials from `config.ini`, retrieves and prints club member
counts.
"""

import configparser
import os

import britishcycling_clubs.main as bc

config = configparser.ConfigParser()
folder_path = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(folder_path, "config.ini")
config.read_file(open(config_file))

member_counts = bc.get_member_counts(
    config["club"]["id"], config["club"]["username"], config["club"]["password"]
)

print(f"{member_counts['active']=}")
print(f"{member_counts['pending']=}")
print(f"{member_counts['expired']=}")
