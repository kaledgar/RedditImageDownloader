# Reddit Image Downloader
The "Reddit Image Downloader" is a Python application that allows users to download images from a Reddit user's submissions. It utilizes the Reddit API and [`PRAW`](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html) library to fetch post information and download the corresponding images.

# How tu run

## Preliminary

- clone the repository
```shell
git clone https://github.com/kkinastowski66/reddit-image-download.git
```
- Create [`authorized reddit application`](https://www.reddit.com/prefs/apps), read about [`Reddit API`](https://www.reddit.com/dev/api/) and obtain the necessary credentials, such as the client ID, client secret, username, password, and user agent. Store these credentials in a JSON file `user_credentials.json`

```json
{
"username":"your reddit username",
"password":"pw to your reddit account",
"user_agent":"anything here",
"client_secret":"...",
"client_id":"..."
}
```

![image](https://github.com/kkinastowski66/reddit-image-download/assets/101144906/1b76c851-373d-4065-9ffe-f20e86c30a17)

## Using Docker (Recommended)
To use the "Reddit Image Downloader", follow these steps:
 - Clone the repository.
 - Adjust the Dockerfile upt to your preferences 
 ```shell
 # build docker image 
docker build -t reddit-image-downloader .

# run
 docker run -v /your/local/directory:/app/downloads reddit-image-downloader
 ```

## Standard method

To use the "Reddit Image Downloader", follow these steps:
 - Clone the repository
 - Customize the constants.py file if needed, adjusting default file paths or other constants according to your preferences.
 - Install the required dependencies:
```sh
pip install -r requirements.txt 
python3 -m reddit_image_downloader -u "your", "users", "list"
```

The last command runs the script and downloads media from users given in list and saves it in separate directories.

## Pre-commit

To use [`pre-commit`](https://pre-commit.com) during the development run:

```sh
python3 -m venv .vev
source .venv/bin/activate
pip install pre-commit
pre-commit install
```

`.pre-commit-config.yaml` stores the `pre-commit` configuration.
