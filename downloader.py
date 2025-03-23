from utility_functions import (
    ensure_directory_exists,
    generate_random_string,
    read_json,
    download_file,
)
from config import PROCESSED_DATA_PATH, USER_MEDIA_PATH, USERS_LIST, FEED_DIR, CLIPS_DIR


def get_carousel_media(media):
    if media["product_type"] == "feed":
        return {"type": "feed", "url": media["url"]}
    elif media["product_type"] == "clips":
        return {"type": "clip", "url": media["url"]}
    else:
        return {"type": "unknown", "url": None}


def get_urls(post):
    if post["product_type"] == "carousel_container":
        return [get_carousel_media(media) for media in post["media"]]
    else:
        return [{"type": post["product_type"], "url": post["media"]["url"]}]


if __name__ == "__main__":
    for username in USERS_LIST:
        required_dirs = [
            f"{USER_MEDIA_PATH}/{username}/{FEED_DIR}",
            f"{USER_MEDIA_PATH}/{username}/{CLIPS_DIR}",
        ]
        for dir in required_dirs:
            ensure_directory_exists(dir)

        posts = read_json(f"{PROCESSED_DATA_PATH}/{username}.json")["posts"]

        posts_urls = [get_urls(post) for post in posts]

        for post_urls in posts_urls:
            for post in post_urls:
                filename = generate_random_string(15)

                download_file(
                    post["url"],
                    f"{USER_MEDIA_PATH}/{username}/{FEED_DIR}/{filename}.jpg"
                    if post["type"] == "feed"
                    else f"{USER_MEDIA_PATH}/{username}/{CLIPS_DIR}/{filename}.mp4",
                )
