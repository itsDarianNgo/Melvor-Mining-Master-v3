# src/mining_logic/mining_controller.py

import logging
import time

import config.settings as settings
from src.equipment_optimization.glove_switching import switch_gloves_if_needed
from .mining_actions import mine_ore, retry


def continuous_mining(driver):
    """
    Continuously mine with a focus on the primary ore, switching to fallback ores only when necessary,
    and revert back to the primary ore when it fully respawns.
    Args:
        driver: The Selenium WebDriver instance used to control the browser.
    """
    logging.info("Starting continuous mining operation.")
    currently_mining = None  # Track the ore currently being mined

    try:
        while True:
            ores_data = fetch_ore_data(driver)
            primary_ore = settings.ORE_PRIORITIES["primary_ore"]
            primary_ore_data = ores_data.get(primary_ore, None)

            # Log current status of the primary ore
            logging.info(
                f"Status of {primary_ore}: Current HP = {primary_ore_data['currentHP']}, Max HP = {primary_ore_data['maxHP']}"
            )

            # Check if the primary ore has fully respawned and currently not mining it
            if primary_ore_data["currentHP"] == primary_ore_data["maxHP"] and (
                currently_mining != primary_ore
            ):
                logging.info(
                    f"{primary_ore} has fully respawned with Max HP {primary_ore_data['maxHP']}, switching to mine it."
                )
                switch_gloves_if_needed(driver, primary_ore)
                mine_ore(driver, primary_ore)
                currently_mining = primary_ore
                continue

            # If the primary ore is not being mined and no ore is being mined or current ore depleted
            if (
                currently_mining is None
                or ores_data[currently_mining]["currentHP"] <= 0
            ):
                # Iterate over fallback ores if the primary ore is depleted or respawning
                for ore in settings.ORE_PRIORITIES["fallback_ores"]:
                    ore_data = ores_data.get(ore, None)
                    if ore_data and ore_data["currentHP"] > 0:
                        logging.info(
                            f"Starting mining on fallback ore {ore} with HP {ore_data['currentHP']}"
                        )
                        switch_gloves_if_needed(driver, ore)
                        mine_ore(driver, ore)
                        currently_mining = ore
                        break

            # If currently mining some ore and it's not depleted, continue mining
            elif currently_mining and ores_data[currently_mining]["currentHP"] > 0:
                logging.info(
                    f"Continuing to mine {currently_mining}. Current HP: {ores_data[currently_mining]['currentHP']}"
                )
                time.sleep(5)  # Mimic ongoing mining activity

            time.sleep(5)  # Slight delay before rechecking ore statuses

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
