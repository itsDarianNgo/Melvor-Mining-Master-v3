# src/mining_logic/mining_actions.py

import logging
import textwrap
import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    WebDriverException,
)


def retry(func, retries=3, delay=1):
    for i in range(retries):
        try:
            return func()
        except StaleElementReferenceException:
            if i < retries - 1:
                time.sleep(delay)
            else:
                logging.error(
                    "Stale element reference exception after multiple retries."
                )
                raise


def fetch_current_hp(driver):
    """
    Fetch the current HP of all ores and store it in a dictionary.
    Args:
        driver: The Selenium WebDriver instance.
    Returns:
        dict: A dictionary with ore localID as keys and their current HP as values.
    """
    script = """
    const oreHpMap = {};
    const ores = game.mining.actions.registeredObjects;
    ores.forEach((value, key) => {
        oreHpMap[key] = value.currentHP;
    });
    return oreHpMap;
    """
    try:
        ore_hp_map = retry(lambda: driver.execute_script(script))
        # logging.info(f"Fetched ore HP data: {ore_hp_map}")
        return ore_hp_map
    except WebDriverException as e:
        logging.error(f"Failed to execute script to fetch ore HP: {str(e)}")
        return {}


def mine_ore(driver, ore_name):
    try:
        local_id = ore_name.split(":")[-1]
        logging.info(f"Attempting to mine ore: {ore_name} with local ID: {local_id}")

        script = textwrap.dedent(
            f"""
            console.log('Initiating mining operation for localID:', '{local_id}');
            function startMiningSpecifiedRock(rock) {{
                if (typeof game !== 'undefined' && game.mining) {{
                    if (rock) {{
                        game.mining.onRockClick(rock);
                        console.log('Mining initiated for rock:', rock._localID);
                        return rock.currentHP;
                    }} else {{
                        console.error('No rock object provided for mining.');
                        return null;
                    }}
                }} else {{
                    console.error('Game mining object not available or undefined.');
                    return null;
                }}
            }}

            function selectRockByProperty(property, value) {{
                if (typeof game !== 'undefined' && game.mining) {{
                    const rocks = game.mining.actions.registeredObjects;
                    for (let [key, rock] of rocks) {{
                        if (rock && rock[property] === value) {{
                            console.log('Rock selected:', rock._localID);
                            return rock;
                        }}
                    }}
                }}
                console.error('No rock found with', property, '=', value);
                return null;
            }}

            const selectedRock = selectRockByProperty('_localID', '{local_id}');
            if (selectedRock && selectedRock.currentHP > 0) {{
                console.log('Proceeding with mining rock:', selectedRock._localID);
                return startMiningSpecifiedRock(selectedRock);
            }} else {{
                console.error('Rock not available or depleted:', selectedRock?._localID);
                return null;
            }}
            """
        )

        initial_hp = retry(lambda: driver.execute_script(script))
        if initial_hp is not None and initial_hp > 0:
            time.sleep(15)
            current_hp = driver.execute_script(
                "return game.mining.selectedRock.currentHP"
            )
            if current_hp < initial_hp:
                logging.info(
                    f"Mining successful. Initial HP: {initial_hp}, Current HP: {current_hp}"
                )
            else:
                raise AssertionError(
                    f"Expected HP decrement after mining, but found Initial HP: {initial_hp}, Current HP: {current_hp}"
                )
        else:
            raise AssertionError("Failed to select and mine the specified rock.")
    except WebDriverException as e:
        logging.error("WebDriverException occurred during mining operation.")
        raise e
    except AssertionError as e:
        logging.error(e)
        raise e
