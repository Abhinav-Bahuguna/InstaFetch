import os
import json
import random
import time
import string
import requests


def download_file(url, filename):
    """Downloads a file from a URL and saves it locally."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raises an error for bad HTTP responses (4xx, 5xx)

        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"✅ File downloaded: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading {url}: {e}")


def generate_random_string(length=10):
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(length)
    )


def random_sleep(min, max):
    random_number = random.randint(min, max)
    time.sleep(random_number)


def read_json(filename):
    """Reads JSON data from a file."""
    with open(filename, "r") as f:
        return json.load(f)


def ensure_directory_exists(directory_path):
    """Creates the directory if it does not exist."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"📁 Directory ensured: {directory_path}")
    except OSError as e:
        print(f"❌ Error creating directory {directory_path}: {e}")


def save_json(data, filename):
    """Saves the given data to a JSON file"""

    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Data successfully saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving data: {e}")
