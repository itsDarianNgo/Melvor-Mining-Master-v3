# config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

GAME_URL = "https://melvoridle.com/"
USERNAME = os.getenv("MELVOR_USERNAME")
PASSWORD = os.getenv("MELVOR_PASSWORD")
CHARACTER_NAME = os.getenv("CHARACTER_NAME")

