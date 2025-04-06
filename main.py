import crediantials
from insta_login import get_instagram_links, save_links_to_json


def main():
    username = crediantials.USER
    password = crediantials.PWD
    target_username = "tamannaahspeaks"

    post_links = get_instagram_links(username, password, target_username, 3)
    save_links_to_json(post_links)
    print(f"Extracted {len(post_links)} links saved to instagram_links.json")

if __name__ == "__main__":
    main()
