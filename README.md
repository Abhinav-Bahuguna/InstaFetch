**Instagram Media Downloader**

This repository contains a set of Python scripts to download and process media from Instagram accounts. The code allows you to:
Scrape data from Instagram user profiles.
Download posts and media like images, videos, and clips from a specific user.
Save the data and media locally in an organized structure.
Customize download directories, filenames, and handle various media types.

**Features**

Scrapes Instagram user profile data.
Downloads posts, images, videos, and carousel media.
Generates random filenames for downloaded media.
Allows for retrying failed requests with exponential backoff.
Saves processed data in JSON format to perform analytics.

```bash
/data
    /raw                # Raw JSON data for user profiles
    /processed          # Processed user profile data (removes unwanted fields)
    /users              # Downloaded media (images, videos)
        /username       # Downloaded media is group under username
            /images
            /clips

/configs
    common.py           # Configuration file with common URL and settings
    headers.py          # HTTP headers configuration
    cookies.py          # Cookies used for requests
    variables.py        # Variables used for requests

clean_data.py          # script to clean the data, removes unwanted fileds and places cleaned json under preprocessed directory
config.py              # configuration file
downloader.py          # script to download posts from insta profile, reads data from processed directory
main.py                # script to fetch profile data from insta and creates json file under raw
utility_functions.py   # utiltity functions used across all thee scripts
```

**Important Notes**

Rate Limiting and Retries: The scraper includes automatic retries with exponential backoff if a request fails due to network or server issues.
Media Types: The script supports downloading both images (feed) and videos (clips). It also supports carousel media, where multiple media items (images or videos) are part of a single post.
File Naming: Media files are saved with randomly generated filenames to avoid conflicts. The filenames are generated using the generateRandomString function.
Customization: The script allows you to customize file paths and directories for saving data. For example, you can specify where to save raw JSON data or downloaded media files.

**Disclaimer**

This project is intended for educational purposes only. Be mindful of Instagram's terms of service when scraping data from their platform.
This tool is for personal use and does not guarantee any compliance with Instagram's usage policies. Always ensure you are following Instagram's guidelines when scraping data.
