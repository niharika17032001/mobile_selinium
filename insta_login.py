import json
import time

from selenium import webdriver
# Imports to get chrome driver working
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# Imports to get firefox driver working
from selenium.webdriver.firefox.service import Service as FirefoxService
# Imports to get chrome driver working
from webdriver_manager.firefox import GeckoDriverManager

# Imports to get firefox driver working
# Imports to get chrome driver working
import ImportantVariables as imp_val

# General imports
# Imports to get firefox driver working
# Import options for headless mode

# Important variables
user_data_directory = imp_val.new_user_data_directory
profile_directory = "Default"
chrome_driver_path = imp_val.chrome_driver_path
chrome_executable_path = imp_val.chrome_executable_path

import crediantials


def create_firefox_driver(headless=True):
    print("Launching Firefox...")
    firefox_options = FirefoxOptions()
    if headless:
        firefox_options.add_argument('--headless')  # Run in headless mode
        firefox_options.add_argument('--no-sandbox')  # Recommended for CI environments
        firefox_options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm issues in CI
        firefox_options.add_argument('--disable-gpu')  # Optional: Disable GPU usage
        firefox_options.add_argument('--window-size=1920,1080')  # Ensure proper resolution
    # firefox_options.add_argument("--headless")

    # Set custom Firefox profile directory
    if user_data_directory:
        firefox_options.add_argument(f"-profile")
        firefox_options.add_argument(user_data_directory)

    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
    return driver


def is_logged_in(driver):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)
    current_url = driver.current_url
    if "login" in current_url or "challenge" in current_url:
        print("Login required.")
        return False
    print("Session is active.")
    return True


def login(username, password, driver):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(4)
    user_input = driver.find_element(By.NAME, "username")
    pass_input = driver.find_element(By.NAME, "password")
    user_input.send_keys(username)
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.ENTER)
    time.sleep(10)
    if "login" in driver.current_url:
        raise Exception("Login failed.")
    else:
        print("Login successful.")


def login_with_browser(username, password):
    driver = create_firefox_driver(headless=False)
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(4)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password + Keys.ENTER)
    time.sleep(5)
    with open(crediantials.page_content_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    driver.save_screenshot(crediantials.screenshot_path)
    is_logged_in(driver)
    driver.quit()


def get_instagram_links(username, password, target_username, max_scrolls, max_attempts_without_new_links=3,
                        headless=True):
    driver = create_firefox_driver(headless=headless)
    driver.get("https://www.instagram.com/")

    time.sleep(3)
    if not is_logged_in(driver):
        login(username, password, driver)

    instagram_url = f"https://www.instagram.com/{target_username}/reels/"
    driver.get(instagram_url)
    time.sleep(5)

    links = set()
    attempts_without_new_links = 0

    while attempts_without_new_links < max_attempts_without_new_links:
        previous_count = len(links)
        anchors = driver.find_elements(By.TAG_NAME, "a")
        for a in anchors:
            href = a.get_attribute("href")
            if href and ("/reel/" in href or "/p/" in href):
                links.add(href)

        if max_scrolls is None:
            if len(links) == previous_count:
                attempts_without_new_links += 1
            else:
                attempts_without_new_links = 0
        else:
            max_attempts_without_new_links = max_scrolls
            attempts_without_new_links += 1

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    driver.quit()
    return list(links)


def save_links_to_json(links, filename="instagram_links.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(links, file, indent=4)


if __name__ == "__main__":
    username = crediantials.USER
    password = crediantials.PWD
    target_username = "tamannaahspeaks"

    post_links = get_instagram_links(username, password, target_username, 3, headless=False)
    save_links_to_json(post_links)
    print(f"Extracted {len(post_links)} links saved to instagram_links.json")
