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
ORE_PRIORITIES = {
    "primary_ore": "melvorAoD:Pure_Crystal",
    "fallback_ores": [
        "melvorTotH:Corundumite_Ore",
        "melvorD:Dragonite_Ore",
        # Add more ores here as needed
    ],
}

GLOVE_MAP = {
    "melvorAoD:Pure_Crystal": "Mining_Gloves",
    "melvorTotH:Corundumite_Ore": "Gem_Gloves",
    "melvorD:Dragonite_Ore": "Gem_Gloves",
}
