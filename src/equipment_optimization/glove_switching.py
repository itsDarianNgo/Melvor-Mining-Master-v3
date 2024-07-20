import logging
import textwrap
import time

from selenium.common.exceptions import StaleElementReferenceException

import config.settings as settings


def retry(func, retries=3, delay=1):
    for i in range(retries):
        try:
            return func()
        except StaleElementReferenceException:
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise


def get_current_glove(driver):
    """
    Get the currently equipped glove.
    Args:
            driver: The Selenium WebDriver instance.
    Returns:
            str: The local ID of the currently equipped glove.
    """
    script = """
    return game.combat.player.equipment.equippedItems["melvorD:Gloves"].item._localID;
    """
    try:
        current_glove_id = driver.execute_script(script)
        return current_glove_id
    except Exception as e:
        print(f"[Error] Unable to get current glove: {e}")
        return None


def equip_item(driver, item_name, set=0):
    """
    Equip a specified item.
    Args:
            driver: The Selenium WebDriver instance.
            item_name: The local ID of the item to be equipped.
            set: The equipment set to use (default is 0).
    """
    script = textwrap.dedent(
        """
		function equipItem(itemName, set = 0) {
			const item = game.items.equipment.registeredObjects.get(`melvorD:${itemName}`);
			if (item) {
				console.log("Retrieved item:", item);
				const slot = item.validSlots[0];
				try {
					game.combat.player.equipItem(item, set, slot, 1);
					console.log(`${item._name} equipped successfully!`);
				} catch (error) {
					console.error("Error equipping item:", error);
				}
			} else {
				console.log(`Item ${itemName} not found!`);
			}
		}

		equipItem(arguments[0], arguments[1]);
	"""
    )
    retry(lambda: driver.execute_script(script, item_name, set))


def switch_gloves_if_needed(driver, ore_id):
    current_glove = get_current_glove(driver)
    required_glove = settings.GLOVE_MAP.get(ore_id, None)

    if required_glove and current_glove != required_glove:
        logging.info(
            f"Switching gloves: Current ({current_glove}), Required ({required_glove})"
        )
        equip_item(driver, required_glove)
    elif required_glove:
        logging.info("No glove switch needed. Current glove is already appropriate.")
    else:
        logging.error(f"No mapping found for required gloves for the ore: {ore_id}")
    # Handle error scenario, potentially pausing mining as mentioned
