# List of usernames to fetch data for
USERS_LIST = [
    # "sakshimehrotraa",
    # "blogft.hirva",
    "nehasharmaofficial",
    "heer_music",
]  # Add more usernames as needed

# API request settings
RETRY_ATTEMPTS = 3
BACKOFF_FACTOR = 2

# Sleep interval settings (in seconds)
RANDOM_SLEEP_MIN = 1
RANDOM_SLEEP_MAX = 5
FINAL_SLEEP_MIN = 4
FINAL_SLEEP_MAX = 8

# Directory to save data
RAW_DATA_PATH = "./data/raw"
PROCESSED_DATA_PATH = "./data/processed"
USER_MEDIA_PATH = "./data/users"

FEED_DIR = "images"
CLIPS_DIR = "clips"
