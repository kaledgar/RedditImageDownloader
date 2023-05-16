import pandas as pd
import json
import praw
from prawcore.exceptions import Forbidden
from constants import DEFAULT_CREDENTIALS_FILEPATH


class RedditImageDownload:
    def __init__(
            self,
            image_count,
            credentials_filepath = DEFAULT_CREDENTIALS_FILEPATH,
    ):
        self.image_count = image_count
        self.reddit = self._get_reddit_from_filepath(credentials_filepath)

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

    def api_test(self, name = "kacperekk6dev"):
        user = self.reddit.redditor(name)
        print(user.name)
        print(user.subreddit)

        return 0




#test_object
rid = RedditImageDownload(10)
test = rid.api_test()