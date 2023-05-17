import pandas as pd
import json
import praw
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

    def get_posts_from_profile(self, subreddit_posts_count = 10):
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
             subm.subreddit)
            for subm in subreddit.top(limit=subreddit_posts_count)
        ]
        df = pd.DataFrame(post_info, columns=["id", "author", "text", "url", "title", "score", "subreddit"])
        return df

n1 = 'aroushthekween'
#test_object
rid = RedditImageDownload(n1)
df = rid.get_posts_from_profile()

print(df)