from utility_functions import read_json, save_json, ensure_directory_exists
from config import (
    RAW_DATA_PATH,
    USERS_LIST,
    PROCESSED_DATA_PATH,
)


def extract_media(item):
    def extract_user_tags(item):
        usertags = item["usertags"]["in"] if item["usertags"] is not None else []
        return [
            usertag["user"] if usertag is not None else None for usertag in usertags
        ]

    def extract_feed(item):
        return item["image_versions2"]["candidates"][0]["url"]

    def extract_clip(item):
        return item["video_versions"][0]["url"]

    def extract_audio(item):
        audio_info = {}
        if item["has_audio"] and item["clips_metadata"] is not None:
            if item["clips_metadata"]["audio_type"] == "licensed_music":
                audio_info["audio_type"] = "licensed_music"
                music_asset_info = item["clips_metadata"]["music_info"][
                    "music_asset_info"
                ]
                audio_info["title"] = music_asset_info["title"]
                audio_info["artist"] = music_asset_info["display_artist"]

            else:
                audio_info["audio_type"] = "original"

        return audio_info

    if item["product_type"] in ["clips", "igtv"]:
        return {
            "usertags": extract_user_tags(item),
            "audio": extract_audio(item),
            "url": extract_clip(item),
        }
    elif item["product_type"] == "feed":
        return {
            "usertags": extract_user_tags(item),
            "audio": extract_audio(item),
            "url": extract_feed(item),
        }
    elif item["product_type"] == "carousel_container":
        media = []
        for carousel_item in item["carousel_media"]:
            if carousel_item["media_type"] == 1:
                media.append(
                    {
                        "usertags": extract_user_tags(carousel_item),
                        "accessibility_caption": carousel_item["accessibility_caption"],
                        "product_type": "feed",
                        "url": extract_feed(carousel_item),
                    }
                )
            elif item["media_type"] == 2:
                media.append(
                    {
                        "usertags": extract_user_tags(carousel_item),
                        "accessibility_caption": carousel_item["accessibility_caption"],
                        "product_type": "clips",
                        "url": extract_clip(carousel_item),
                    }
                )
        return media
    else:
        print("Unknow Media Type Detected")
        save_json(item, "debug.json")
        return {}


def processUserDetails(user_info):
    """Processes and cleans user profile details."""

    user_info["profile_pic_url"] = user_info.get("hd_profile_pic_url_info", {}).get(
        "url", ""
    )

    # Unwanted keys
    keys_to_remove = [
        "hd_profile_pic_url_info",
        "friendship_status",
        "is_embeds_disabled",
        "is_unpublished",
        "latest_besties_reel_media",
        "latest_reel_media",
        "live_broadcast_visibility",
        "live_broadcast_id",
        "seen",
        "supervision_info",
        "__typename",
    ]

    # Remove unwanted keys
    for key in keys_to_remove:
        user_info.pop(key, None)

    return user_info


def processPostInfo(postInfo):
    def setIfPresent(item, key, value):
        if value is not None:
            return {**item, key: value}
        return item

    post = setIfPresent({}, "code", postInfo["code"])
    post = setIfPresent(post, "pk", postInfo["pk"])
    post = setIfPresent(post, "id", postInfo["id"])
    post = setIfPresent(
        post,
        "caption",
        postInfo["caption"]["text"]
        if postInfo["caption"] is not None
        else postInfo["caption"],
    )
    post = setIfPresent(
        post, "accessibility_caption", postInfo["accessibility_caption"]
    )
    post = setIfPresent(post, "added_at", postInfo["taken_at"])
    post = setIfPresent(post, "like_count", postInfo["like_count"])
    post = setIfPresent(post, "comment_count", postInfo["comment_count"])
    post = setIfPresent(post, "product_type", postInfo["product_type"])
    post = setIfPresent(post, "media", extract_media(postInfo))
    post = setIfPresent(post, "location", postInfo["location"])

    return post


if __name__ == "__main__":
    for username in USERS_LIST:
        content = read_json(f"{RAW_DATA_PATH}/{username}.json")

        data = {
            "user": processUserDetails(content[0]["node"]["user"]),
            "posts": [processPostInfo(item["node"]) for item in content],
        }

        ensure_directory_exists(PROCESSED_DATA_PATH)
        save_json(data, f"{PROCESSED_DATA_PATH}/{username}.json")
