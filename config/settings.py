# config/settings.py

import os

from dotenv import load_dotenv

load_dotenv()

# Game settings
GAME_URL = "https://melvoridle.com/"
USERNAME = os.getenv("MELVOR_USERNAME")
PASSWORD = os.getenv("MELVOR_PASSWORD")
CHARACTER_NAME = os.getenv("CHARACTER_NAME")


# Priority list of ores to be mined, ordered by value
ORE_PRIORITIES = [
    "melvorAoD:Pure_Crystal",
    "melvorTotH:Corundumite_Ore",
    "melvorD:Dragonite_Ore",
]
