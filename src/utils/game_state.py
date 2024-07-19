# src/game_state.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_game_ready(browser, timeout=30):
    """
    Checks if the game is ready by evaluating JavaScript in the browser context.
    """
    script = 'return typeof game !== "undefined" && game !== null;'
    try:
        WebDriverWait(browser, timeout).until(
            lambda driver: driver.execute_script(script)
        )
        return True
    except Exception as e:
        print(f"Game is not ready: {e}")
        return False
