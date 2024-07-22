# RedditImageDownloader 🎨📸

Welcome to RedditImageDownloader, a simple Python module for effortlessly batch downloading media from Reddit! 🌟

This tool leverages the Reddit API and the PRAW library to seamlessly fetch post information and download the corresponding images in async/await method. The script uses built-in md5-based duplicate removal for initial data cleaning purpose to avoid downloading the same image that was posted to multiple subreddits.

# Usage

## Preliminary

- clone the repository
```shell
git clone https://github.com/kaledgar/RedditImageDownloader
```
- Create [`authorized reddit application`](https://www.reddit.com/prefs/apps), read about [`Reddit API`](https://www.reddit.com/dev/api/) and obtain the necessary credentials, such as the client ID, client secret, username, password, and user agent. Store these credentials in a JSON file `credentials.json` in your local repository that you cloned.

```json
{
    "username": "your reddit username",
    "password": "pw to your reddit account",
    "user_agent": "anything here",
    "client_secret": "client secret of reddit app you create",
    "client_id": "app id, see below for details"
}
```

## Run the script

 - Customize the constants.py file if needed, adjusting default file paths or other constants according to your preferences.
 - Install the required dependencies:

```sh
# Install requirements
pip install -r requirements.txt 

# Check possible arguments
python3 -m reddit_image_downloader -h

# Run module with your custom arguments
python3 -m reddit_image_downloader -u example_user -d 'mnt/d/Downloads'
```

The last command runs the script and downloads media from users given in list and saves it in separate directories.

### Run with Docker
To use the "Reddit Image Downloader" with Docker, follow these steps:
 - Adjust the Dockerfile up to your preferences 
 ```shell
 # build docker image 
docker build -t reddit-image-downloader .
# run
 docker run -v /your/local/directory:/app/downloads reddit-image-downloader
 ```

## Pre-commit

To use [`pre-commit`](https://pre-commit.com) during the development run:

```sh
python3 -m venv .vev
source .venv/bin/activate
pip install pre-commit
pre-commit install
```

`.pre-commit-config.yaml` stores the `pre-commit` configuration.

## FAQ

### What is client_id and secret_id?

In [`authorized reddit application`](https://www.reddit.com/prefs/apps) settings:

![image](https://github.com/user-attachments/assets/765b4371-371b-4c70-ad25-3f49cd8eb411)

### No permissions error

1. WIN - Run the script in Powershell Admin session
2. Linux - run script with sudo
