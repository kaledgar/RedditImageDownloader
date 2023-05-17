import pandas as pd
import json
import praw
import requests
import os
from prawcore.exceptions import Forbidden
from constants import DEFAULT_CREDENTIALS_FILEPATH


class RedditImageDownload:
    def __init__(
            self,
            user_name,
            image_count = 10,
            credentials_filepath = DEFAULT_CREDENTIALS_FILEPATH,
    ):
        self.user_name = user_name
        self.image_count = image_count
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

    def get_posts(self, posts_count = 10):
        user_submissions = [subm.url for subm in self.user.submissions.top(time_filter = "all")]

        return user_submissions

    def get_posts_from_profile(self, posts_count = 10):
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
        rqst = requests.get(url)
        with open(f'{name}.{format}', "wb") as file:
            file.write(rqst.content)

    def test(self):
        self._make_directory()


name = 'kacperekk6dev'


#test_object
rid = RedditImageDownload(name)
df = rid.get_posts_from_profile()
df1 = rid.get_posts()

print(df1)