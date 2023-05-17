import pandas as pd
import json
import praw
import requests
import os
from prawcore.exceptions import Forbidden
from constants import *


class RedditImageDownload:
    def __init__(
            self,
            user_name,
            credentials_filepath = DEFAULT_CREDENTIALS_FILEPATH,
    ):
        self.user_name = user_name
        self.reddit = self._get_reddit_from_filepath(credentials_filepath)
        self.user = self.reddit.redditor(self.user_name)

    def _get_reddit_from_filepath(self, credentials_filepath):
        credentials: dict
        with open(credentials_filepath, "r") as file:
            file_content = file.read()
            credentials = json.loads(file_content)
        return praw.Reddit(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            password=credentials["password"],
            user_agent=credentials["user_agent"],
            username=credentials["username"],
        )

    def _make_directory(self):
        path = f'./{self.user_name}'
        if not os.path.exists(path):
            os.mkdir(path)
            print("Folder %s created!" % path)
        else:
            print("Folder %s already exists" % path)

    def _get_posts(self, posts_count = POST_COUNT):
        user_submissions = [
            (subm.id,
             subm.url,
             subm.created_utc)
            for subm in self.user.submissions.new(limit = None)]
        df = pd.DataFrame(user_submissions, columns=["id", "url", "created_utc"])
        return df

    def _get_posts_from_profile(self, posts_count = POST_COUNT):
        #profile is attribute display_name of class UserSubreddit, its a name of user profile/wall/user's subreddit
        profile = self.user.subreddit.display_name
        subreddit = self.reddit.subreddit(profile)
        post_info = [
            (subm.id,
             str(subm.author),
             str(subm.selftext),
             str(subm.url),
             str(subm.title),
             int(subm.score),
             int(subm.created_utc),
             subm.subreddit)
            for subm in subreddit.top(limit=posts_count)
        ]
        df = pd.DataFrame(post_info, columns=["id", "author", "text", "url",
                                              "title", "score", "created_utc", "subreddit"])
        return df

    def download_from_url(self, url, name, format):
        ## remember to check if self.user_name directory exists
        rqst = requests.get(url)
        with open(f'{self.user_name}/{name}.{format}', "wb") as file:
            file.write(rqst.content)

    def get_images(self):
        self._make_directory()
        df = self._get_posts()
        for i, url in enumerate(df['url']):
            print(url)
            self.download_from_url(url, i, 'jpg')

        return df



name = 'kacperekk6dev'
