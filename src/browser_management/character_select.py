# src/browser_management/character_select.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
import logging


def select_character(browser, character_name):
    # Click show cloud saves
    cloud_saves_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@onclick='toggleSaveSelectionView();']")
        )
    )
    cloud_saves_button.click()

    # Click the toggle button for "Enable warning popup to overwrite saves"
    toggle_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[2]/div/div/div[2]/div[5]/div[2]/div[2]/div[1]/div[1]/div/label",
            )
        )
    )
    toggle_button.click()

    # Click on the character name
    character_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//h5[contains(text(), '{character_name}')]")
        )
    )
    character_button.click()

    try:
        # Click on the currently active mod profile button
        active_mod_profile_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="swal2-html-container"]/div/div/div/div[2]/a')
            )
        )
        active_mod_profile_button.click()
    except TimeoutException:
        logging.warning("Active mod profile button did not appear.")

    try:
        # Confirm character selection
        confirm_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.swal2-confirm.btn.btn-primary.m-1")
            )
        )
        try:
            confirm_button.click()
        except ElementClickInterceptedException:
            # Use JavaScript click if the element is intercepted
            browser.execute_script("arguments[0].click();", confirm_button)
    except TimeoutException:
        logging.warning("Confirm button did not appear.")

    # Wait for the game to load by checking for the "Welcome Back!" dialog
    welcome_back_dialog_locator = (
        By.XPATH,
        "//h2[@class='swal2-title' and contains(text(), 'Welcome Back!')]",
    )
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located(welcome_back_dialog_locator)
    )
