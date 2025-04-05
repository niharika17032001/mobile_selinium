from setup_browser import launch_browser


def main():
    browser = "chrome"
    # browser = "firefox"
    driver = launch_browser(browser)

if __name__ == "__main__":
    main()
