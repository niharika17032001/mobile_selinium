import sys
import time
# General imports
import pytest
from selenium import webdriver

# Imports to get chrome driver working
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Imports to get firefox driver working
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Import options for headless mode
from selenium.webdriver.chrome.options import Options



import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# Imports to get firefox driver working
from selenium.webdriver.firefox.service import Service as FirefoxService
# Imports to get chrome driver working
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import ImportantVariables as imp_val

# Important variables
user_data_directory = imp_val.new_user_data_directory
profile_directory = "Default"


def launch_browser(browser="chrome"):
    driver = None

    if browser == "chrome":
        print("Launching Chrome...")
        chrome_options = uc.ChromeOptions()

        if user_data_directory:
            chrome_options.add_argument(f"--user-data-dir={user_data_directory}")
        if profile_directory:
            chrome_options.add_argument(f"--profile-directory={profile_directory}")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')  # Recommended for CI environments
        chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm issues in CI
        chrome_options.add_argument('--disable-gpu')  # Optional: Disable GPU usage
        chrome_options.add_argument('--window-size=1920,1080')  # Ensure proper resolution

        driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    elif browser == "firefox":
        print("Launching Firefox...")
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")

        # Set custom Firefox profile directory
        if user_data_directory:
            firefox_options.add_argument(f"-profile")
            firefox_options.add_argument(user_data_directory)

        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)


    else:
        print("Unsupported browser:", browser)
        sys.exit(1)

    driver.implicitly_wait(10)
    return driver


if __name__ == "__main__":
    # Choose browser: "chrome" or "firefox"
    # browser = input("Enter browser (chrome/firefox): ").strip().lower()
    browser = "chrome"
    # browser = "firefox"
    driver = launch_browser(browser)

    try:
        driver.get("https://www.instagram.com")
        time.sleep(5)  # Let page load
        print("Page title:", driver.title)
    finally:
        print("Closing browser...")
        driver.quit()
