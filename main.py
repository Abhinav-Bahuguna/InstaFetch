import requests
import json

from time import sleep
from configs import common
from configs import headers
from configs import cookies
from configs import variables as req
from utils import random_sleep as rs


def saveAsJson(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def requestUserDataViaInstaApi(headers, cookies, data, retries=3, backoff_factor=2):
    for attempt in range(1, retries + 1):
        try:
            _response = requests.post(
                common.URL, headers=headers, cookies=cookies, data=data
            )

            if _response.status_code == 200:
                response = json.loads(_response.text)
                query_result = response["data"][
                    "xdt_api__v1__feed__user_timeline_graphql_connection"
                ]
                edges = query_result["edges"]
                page_info = query_result["page_info"]

                return edges, page_info
            else:
                print(
                    f"Attempt {attempt} failed with status code {_response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed with error: {e}")
            sleep_time = backoff_factor * (2 ** (attempt - 1))
            print(f"Retrying in {sleep_time} seconds...")
            sleep(sleep_time)

    return [], {"has_next_page": False}


def getUserData(username):
    variables = {**req.variables, "username": username, "after": "null"}
    data = req.data.copy()
    data["variables"] = json.dumps(variables)

    page_info = {"has_next_page": True}
    _data = []

    while page_info["has_next_page"]:
        edges, page_info = requestUserDataViaInstaApi(
            headers.headers, cookies.cookies, data
        )
        _data.extend(edges)

        variables["after"] = page_info["end_cursor"]
        data["variables"] = json.dumps(variables)
        print(f"Number of Posts Collected So Far: {len(_data)}")

        rs.random_sleep(1, 5)

    return _data


if __name__ == "__main__":
    # users_list = ["blokewithabind"]
    users_list = ["_aayuuuuuuu_"]
    # users_list = ["bishtaashima1"]

    for user in users_list:
        userData = getUserData(user)
        print(f"Posts Count [{user}]: {len(userData)}")

        # Saving Data
        download_at = f"./data/raw/{user}.json"
        saveAsJson(userData, download_at)
        print(f"Data Saved [{user}]: {download_at}")

        rs.random_sleep(4, 8)

