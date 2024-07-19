# src/browser_management/login.py

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def login(browser, username, password):
    # Set language to English
    browser.execute_script("cloudManager.showPageLoader(); setLanguage('en'); location.reload();")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "formElements-signIn-username")))

    # Enter username and password
    username_field = browser.find_element(By.ID, "formElements-signIn-username")
    password_field = browser.find_element(By.ID, "formElements-signIn-password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Click sign in
    sign_in_button = browser.find_element(By.XPATH, "//*[@id='formElements-signIn-submit']")
    sign_in_button.click()

    # Wait for login to complete
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//button[@onclick='toggleSaveSelectionView();']")))
