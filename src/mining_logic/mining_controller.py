# src/mining_logic/mining_controller.py

import logging
import time

import config.settings as settings
from .mining_actions import mine_ore, retry


def continuous_mining(driver):
    """
    Continuously mine with a primary focus on Pure_Crystal, switching only necessary.
    Args:
        driver : The Selenium WebDriver instance used to control the browser.
    """
    logging.info("Starting continuous mining operation.")
    currently_mining = None  # Track the ore currently being mined

    try:
        while True:
            ores_data = fetch_ore_data(driver)  # Fetching ore data including maxHP

            # Check if primary ore Pure_Crystal is available and prioritize its mining if it's not what's currently being mined
            primary_ore_data = ores_data.get(
                settings.ORE_PRIORITIES["primary_ore"], None
            )
            if primary_ore_data and primary_ore_data["currentHP"] > 0:
                if currently_mining != settings.ORE_PRIORITIES["primary_ore"]:
                    logging.info(
                        f"{settings.ORE_PRIORITIES['primary_ore']} is available with HP {primary_ore_data['currentHP']}, switching to mine it."
                    )
                    mine_ore(driver, settings.ORE_PRIORITIES["primary_ore"])
                    currently_mining = settings.ORE_PRIORITIES["primary_ore"]
                continue

            # Mine fallback ores only if primary ore is not available
            for ore in settings.ORE_PRIORITIES["fallback_ores"]:
                ore_data = ores_data.get(ore, None)
                if ore_data and ore_data["currentHP"] > 0:
                    if currently_mining != ore:
                        logging.info(
                            f"Starting mining on fallback ore {ore} with HP {ore_data['currentHP']}"
                        )
                        mine_ore(driver, ore)
                        currently_mining = ore
                        break  # Mine one ore at a time

            time.sleep(10)  # Delay before rechecking ore status

    except Exception as e:
        logging.error(f"Error during mining operation: {e}")
        raise


def fetch_ore_data(driver):
    """
    Fetch the current HP and maximum HP for all ores.
    """
    script = """
    return Object.fromEntries(
        Array.from(game.mining.actions.registeredObjects.entries()).map(([key, ore]) => [
            key, {currentHP: ore.currentHP, maxHP: ore.maxHP}
        ])
    );
    """
    return retry(lambda: driver.execute_script(script))
