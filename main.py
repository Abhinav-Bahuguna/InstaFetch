import os
import json
import requests
from time import sleep

from utility_functions import ensure_directory_exists, save_json, random_sleep

from configs import common, headers, cookies, variables as req
from config import (
    USERS_LIST,
    RETRY_ATTEMPTS,
    BACKOFF_FACTOR,
    RANDOM_SLEEP_MIN,
    RANDOM_SLEEP_MAX,
    FINAL_SLEEP_MIN,
    FINAL_SLEEP_MAX,
    RAW_DATA_PATH,
)


def fetch_user_data(
    headers, cookies, data, retries=RETRY_ATTEMPTS, backoff_factor=BACKOFF_FACTOR
):
    """Fetches user data from Instagram API with retry logic."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(
                common.URL, headers=headers, cookies=cookies, data=data
            )

            if response.status_code == 200:
                json_response = response.json()
                query_result = json_response["data"][
                    "xdt_api__v1__feed__user_timeline_graphql_connection"
                ]
                return query_result.get("edges", []), query_result.get(
                    "page_info", {"has_next_page": False}
                )

            print(
                f"⚠️ Attempt {attempt}: Request failed with status code {response.status_code}"
            )

        except requests.exceptions.RequestException as e:
            print(f"❌ Attempt {attempt}: Network error: {e}")

        # Exponential backoff for retries
        sleep_time = backoff_factor * (2 ** (attempt - 1))
        print(f"⏳ Retrying in {sleep_time} seconds...")
        sleep(sleep_time)

    return [], {"has_next_page": False}


def get_user_posts(username):
    """Retrieves all posts for a given username using pagination."""
    variables = {**req.variables, "username": username, "after": None}
    data = req.data.copy()
    data["variables"] = json.dumps(variables)

    collected_posts = []
    page_info = {"has_next_page": True}

    while page_info.get("has_next_page"):
        edges, page_info = fetch_user_data(headers.headers, cookies.cookies, data)
        collected_posts.extend(edges)

        # Update cursor for next page
        variables["after"] = page_info.get("end_cursor")
        data["variables"] = json.dumps(variables)

        print(f"📊 Posts collected so far for {username}: {len(collected_posts)}")

        random_sleep(RANDOM_SLEEP_MIN, RANDOM_SLEEP_MAX)

    return collected_posts


def main():
    for user in USERS_LIST:
        print(f"🚀 Fetching posts for user: {user}")
        user_posts = get_user_posts(user)
        print(f"✅ Total posts fetched for {user}: {len(user_posts)}")

        # Ensure directory exists and save data
        file_path = os.path.join(RAW_DATA_PATH, f"{user}.json")
        ensure_directory_exists(file_path)
        save_json(user_posts, file_path)

        random_sleep(FINAL_SLEEP_MIN, FINAL_SLEEP_MAX)


if __name__ == "__main__":
    main()
