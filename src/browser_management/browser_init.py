# src/browser_management/browser_init.py

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options


def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("user-agent=DN")  # Corrected user agent option

    browser = uc.Chrome(options=chrome_options)
    return browser
