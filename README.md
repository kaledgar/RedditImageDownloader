# ArtSnap - Reddit Media Downloading Automator 🎨📸
Welcome to ArtSnap, a simple Python wraper for effortlessly batch downloading media from Reddit! 🌟 

This tool leverages the Reddit API and the PRAW library to seamlessly fetch post information and download the corresponding images.

# How tu run

## Preliminary

- clone the repository
```shell
git clone https://github.com/kkinastowski66/reddit-image-download.git
```
- Create [`authorized reddit application`](https://www.reddit.com/prefs/apps), read about [`Reddit API`](https://www.reddit.com/dev/api/) and obtain the necessary credentials, such as the client ID, client secret, username, password, and user agent. Store these credentials in a JSON file `user_credentials.json` in your local repository that you cloned.

```json
{
"username":"your reddit username",
"password":"pw to your reddit account",
"user_agent":"anything here",
"client_secret":"...",
"client_id":"..."
}
```


## Using Docker
To use the "Reddit Image Downloader", follow these steps:
 - Adjust the Dockerfile up to your preferences 
 ```shell
 # build docker image 
docker build -t reddit-image-downloader .
# run
 docker run -v /your/local/directory:/app/downloads reddit-image-downloader
 ```

## Standard method
 - Customize the constants.py file if needed, adjusting default file paths or other constants according to your preferences.
 - Install the required dependencies:
```sh
pip install -r requirements.txt 
python3 -m reddit_image_downloader -u "user1" "user2" "user3"
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

## FAQ

### What is client_id and secret_id?

In [`authorized reddit application`](https://www.reddit.com/prefs/apps) settings:

![image](https://github.com/kkinastowski66/reddit-image-download/assets/101144906/1b76c851-373d-4065-9ffe-f20e86c30a17)

### No permissions error

1. WIN - Run the script in Powershell Admin session
2. Linux - run script with sudo
