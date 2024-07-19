# src/mining_logic/mining_controller.py

import logging
import time

import config.settings as settings
from .mining_actions import fetch_current_hp, mine_ore


def continuous_mining(driver):
    """
    Continuously mine the highest-priority ore that has HP remaining.
    Args:
            driver : The Selenium WebDriver instance used to control the browser.
    """
    logging.info("Starting continuous mining operation.")

    try:
        while True:
            ores_hp = fetch_current_hp(driver)
            for ore_priority in settings.ORE_PRIORITIES:
                if ores_hp.get(ore_priority, 0) > 0:
                    logging.info(
                        f"Starting mining on {ore_priority} with HP {ores_hp[ore_priority]}"
                    )
                    mine_ore(driver, ore_priority)

                    # Loop to handle ore respawning and continuous mining
                    while True:
                        current_hp = fetch_current_hp(driver).get(ore_priority, 0)
                        if current_hp > 0:
                            time.sleep(5)  # mining interval delay
                            logging.info(
                                f"Continuing to mine {ore_priority}. Current HP: {current_hp}"
                            )
                        else:
                            logging.info(
                                f"{ore_priority} depleted. Moving to next ore or waiting for respawn."
                            )
                            break
                    break  # If mining started on a higher-priority ore, break out of the priority check loop

            # Small delay before checking ores status again
            time.sleep(10)

    except Exception as e:
        logging.error(f"Error during mining operation: {e}")
        raise
