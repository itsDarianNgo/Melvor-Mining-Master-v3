import logging
import os
import sys

# Adds the parent directory to sys.path to make the 'config' package available
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from browser_management.browser_init import setup_browser
from browser_management.character_select import select_character
from browser_management.login import login
from browser_management.navigate import navigate_to_homepage
from mining_logic.mining_controller import continuous_mining
from utils.game_state import check_game_ready
import config.settings as settings


def main():
    logging.basicConfig(level=logging.INFO)
    driver = None

    try:
        driver = setup_browser()
        navigate_to_homepage(driver, settings.GAME_URL)
        login(driver, settings.USERNAME, settings.PASSWORD)
        select_character(driver, settings.CHARACTER_NAME)

        if check_game_ready(driver):
            logging.info("Game Loaded. Beginning continuous mining operation.")
            continuous_mining(driver)  # This initiates the mining process

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if driver:
            logging.info("Closing the game driver.")
            driver.quit()


if __name__ == "__main__":
    main()
