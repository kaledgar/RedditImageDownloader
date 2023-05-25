# Reddit Image Download
The "Reddit Image Downloader" project is a Python application that allows users to download images from a Reddit user's submissions or a subreddit's top posts. It utilizes the Reddit API and the PRAW library to fetch post information and download the corresponding images.

## Project Structure
The project consists of the following files:

__init__.py: This file is an empty file and serves as a marker to indicate that the containing directory should be treated as a Python package.

__main__.py: This file serves as the entry point of the application. It allows users to initialize objects from the RedditImageDownload class and execute the image downloading process.

image_downloader_module.py: This file contains the implementation of the RedditImageDownload class, which encapsulates the functionality of fetching post information and downloading images from Reddit. It also includes supporting methods for interacting with the Reddit API, handling file operations, and managing the directory structure.

constants.py: This file defines constants used throughout the project, such as default file paths, post counts, or user agent information.

## Getting Started
To use the "Reddit Image Downloader" project, follow these steps:

 - Install the required dependencies, including the pandas, praw, and requests libraries.

 - Create a Reddit API application and obtain the necessary credentials, such as the client ID, client secret, username, password, and user agent. Store these credentials in a JSON file.

 - Customize the constants.py file if needed, adjusting default file paths or other constants according to your preferences.

- Initialize an object from the RedditImageDownload class in the __main__.py file, providing the Reddit username and the path to the credentials JSON file.

 - Run the __main__.py file to execute the image downloading process.

## Usage
The RedditImageDownload class provides the following methods:

 - __init__(self, user_name, credentials_filepath): Initializes a RedditImageDownload object with the specified Reddit username and the path to the credentials JSON file.

 - get_images(self) -> pd.DataFrame: Fetches the user's submissions from Reddit, creates a directory for the user, and downloads the corresponding images. Returns a pandas DataFrame containing the post information.

Other internal methods: These methods, marked with a leading underscore (_), handle various internal functionalities of the RedditImageDownload class, such as retrieving Reddit instances, creating directories, fetching posts, and downloading images.

## Pre-commit

To use [`pre-commit`](https://pre-commit.com) during the development run:

```sh
python3 -m venv .vev
source .venv/bin/activate
pip install pre-commit
pre-commit install
```

`.pre-commit-config.yaml` stores the `pre-commit` configuration.
