import sys
import time

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
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
        driver = uc.Chrome(options=chrome_options)
        # driver = uc.Chrome(
        #     driver_executable_path=ChromeDriverManager(version="134.0.0").install(),  # use a specific 134 version
        #     options=chrome_options
        # )

        # driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    elif browser == "firefox":
        print("Launching Firefox...")
        firefox_options = FirefoxOptions()
        # firefox_options.add_argument("--headless")

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
    browser = "firefox"
    driver = launch_browser(browser)

    try:
        driver.get("https://www.instagram.com")
        time.sleep(5)  # Let page load
        print("Page title:", driver.title)
    finally:
        print("Closing browser...")
        driver.quit()
