import json
import logging
import os
from datetime import datetime

import pandas as pd
import praw
import requests

## add error handling!!!!!!!
from prawcore.exceptions import Forbidden

from .constants import DEFAULT_CREDENTIALS_FILEPATH, DEFAULT_POST_COUNT

logger = logging.getLogger(__name__)


class RedditImageDownloader:
    def __init__(self, user_name, credentials_filepath=DEFAULT_CREDENTIALS_FILEPATH):
        self.user_name = user_name
        self.reddit = self._get_reddit_from_filepath(credentials_filepath)
        self.user = self.reddit.redditor(self.user_name)

    @staticmethod
    def _get_reddit_from_filepath(credentials_filepath):
        with open(credentials_filepath, "r") as file:
            credentials = json.load(file)
        return praw.Reddit(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            password=credentials["password"],
            user_agent=credentials["user_agent"],
            username=credentials["username"],
        )

    def _make_directory(self):
        path = f"./{self.user_name}"
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            pass

    def _test_none_type_submission(self, gallery_id):
        post = self.reddit.submission(id=gallery_id)
        if post.author is None:
            logger.error(f"Submission with ID {gallery_id} was deleted.")
            return None
        elif not post.is_robot_indexable:
            logger.error(f"Submission with ID {gallery_id} was removed.")
            return None
        else:
            logger.info(f"Submission with ID {gallery_id} is UP.")
            return post

    def _get_posts(self, posts_count=None):
        user_submissions = [
            (subm.id, subm.url, subm.created_utc)
            for subm in self.user.submissions.new(limit=posts_count)
        ]
        df = pd.DataFrame(user_submissions, columns=["id", "url", "created_utc"])
        logger.debug(f"{self.user_name} posts: {df}")
        return df

    def _get_posts_from_profile(self, posts_count=DEFAULT_POST_COUNT):
        profile = self.user.subreddit.display_name
        subreddit = self.reddit.subreddit(profile)
        post_info = [
            (
                subm.id,
                str(subm.url),
                str(subm.title),
                int(subm.created_utc),
                subm.subreddit,
            )
            for subm in subreddit.top(limit=posts_count)
        ]

        df = pd.DataFrame(post_info, columns=["id", "url", "title", "created_utc"])
        return df

    def classify_urls(self, df):
        df["type"] = df["url"].apply(
            lambda x: "image"
            if "i.redd.it" in x
            else "image"
            if "i.imgur" in x
            else "gallery"
            if "reddit.com/gallery" in x
            else "video"
            if "v.redd.it" in x
            else "unknown"
        )
        logger.info(df)
        return df

    def download_image_from_url(self, url, name, format):
        rqst = requests.get(url)

        with open(f"{name}.{format}", "wb") as file:
            file.write(rqst.content)

    def download_image_from_gallery(self, gallery_id, filepath, format):
        post = self._test_none_type_submission(gallery_id)
        if post is None:
            pass
        else:
            url_gallery_list = [
                i[1]["p"][0]["u"].split("?")[0].replace("preview", "i")
                for i in post.media_metadata.items()
            ]

            for i, url in enumerate(url_gallery_list):
                rqst = requests.get(url)

                with open(f"{filepath}_{i}.{format}", "wb") as file:
                    file.write(rqst.content)

            return url_gallery_list

    def get_images(self, name_by="id"):
        if not os.path.isdir(f"{self.user_name}"):
            self._make_directory()
            logger.info(f"Created directory /{self.user_name}")
        else:
            logger.error(f"Directory /{self.user_name} already exists")

        df = self._get_posts()
        df_classified = self.classify_urls(df)

        for i, url in enumerate(df_classified["url"]):
            if name_by == "id":
                name_i = df_classified["id"][i]
            elif name_by == "created_utc":
                name_i = datetime.utcfromtimestamp(
                    df_classified["created_utc"][i]
                ).strftime("%Y-%m-%d--%H-%M-%S")

            filepath = f"{self.user_name}/{name_i}"
            if df_classified["type"][i] == "image":
                self.download_image_from_url(url, filepath, "jpg")
            elif df_classified["type"][i] == "gallery":
                self.download_image_from_gallery(
                    df_classified["id"][i], filepath, "jpg"
                )
            elif df_classified["type"][i] == "unknown":
                pass
