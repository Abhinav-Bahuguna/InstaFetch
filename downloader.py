import requests
import json
import random
import string
import os


def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes

        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"File downloaded successfully: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")


def readDataFrom(filename):
    with open(filename, "r") as f:
        return f.read()


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


def generateRandomString(length=10):
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(length)
    )


if __name__ == "__main__":
    raw_data_path = "./data/processed/"
    raw_files = [
        f
        for f in os.listdir(raw_data_path)
        if os.path.isfile(os.path.join(raw_data_path, f))
    ]

    raw_files = ["bishtaashima1.json"]

    for raw_file in raw_files:
        content = readDataFrom(f"{raw_data_path}/{raw_file}")
        posts = json.loads(content)["posts"]

        posts_urls = [get_urls(post) for post in posts]

        for post_urls in posts_urls:
            for post_url in post_urls:
                filename = generateRandomString(15)
                post_type = post_url["type"]
                post_url = post_url["url"]

                if post_type == "feed":
                    download_file(
                        post_url, f"./data/users/bishtaashima1/images/{filename}.jpg"
                    )
                else:
                    download_file(
                        post_url, f"./data/users/bishtaashima1/clips/{filename}.mp4"
                    )
