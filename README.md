# Reddit Image Downloader
The "Reddit Image Downloader" is a Python application that allows users to download images from a Reddit user's submissions. It utilizes the Reddit API and [`PRAW`](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html) library to fetch post information and download the corresponding images.

## Getting Started
To use the "Reddit Image Downloader", follow these steps:

 - Clone the repository.

 - Install the required dependencies:

```sh
pandas~=2.0.1
praw~=7.7.0
requests~=2.31.0
```

 - Create a [`Reddit API`](https://www.reddit.com/dev/api/) and obtain the necessary credentials, such as the client ID, client secret, username, password, and user agent. Store these credentials in a JSON file.

```json
{
"username":"...",
"password":"...",
"user_agent":"...",
"client_secret":"...",
"client_id":"..."
}

```

 - Customize the constants.py file if needed, adjusting default file paths or other constants according to your preferences.
 
 - Start scrapping with:

```sh
python3 -m reddit_image_downloader -u [requested_reddit_usernames_list]
```

The following command runs the script and downloads media from users given in list and saves it in separate directories.

## Pre-commit

To use [`pre-commit`](https://pre-commit.com) during the development run:

```sh
python3 -m venv .vev
source .venv/bin/activate
pip install pre-commit
pre-commit install
```

`.pre-commit-config.yaml` stores the `pre-commit` configuration.
