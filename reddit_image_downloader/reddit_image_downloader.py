import json
import logging
import os
from datetime import datetime
from typing import Optional, List, Tuple
import pandas as pd
import praw
import requests

import asyncio
import aiohttp

from tqdm import tqdm
from prawcore.exceptions import Forbidden

from .constants import (
    DEFAULT_CREDENTIALS_FILENAME,
    DEFAULT_DOWNLOADS_PATH,
    DEFAULT_IMAGE_FORMAT,
    DEFAULT_MOVIE_FORMAT,
)

logger = logging.getLogger(__name__)


class RedditImageDownloader:
    def __init__(
        self,
        user_name: str,
        credentials_filepath: str = DEFAULT_CREDENTIALS_FILENAME,
        downloads_path: str = DEFAULT_DOWNLOADS_PATH,
    ) -> None:
        """
        Initialize RedditImageDownloader. Images will be downloaded to:
            /downloads_path/user_name

        Args:
            user_name (str): Reddit username.
            credentials_filepath (str, optional): Path to the credentials file. Defaults to DEFAULT_CREDENTIALS_FILENAME.
            downloads_path (str, optional) : Parent directory where images will be downloaded
        """
        self.user_name = user_name

        self.downloads_path = downloads_path
        self.user_path = f"{self.downloads_path}/{self.user_name}"

        self._make_directory()
        self.reddit = self._get_reddit_from_filepath(credentials_filepath)
        self.user = self.reddit.redditor(self.user_name)

    @staticmethod
    def _get_reddit_from_filepath(credentials_filepath) -> praw.Reddit:
        """
        Load Reddit instance from credentials file.

        Args:
            credentials_filepath (str): Path to the credentials file.

        Returns:
            praw.Reddit: Initialized Reddit instance.
        """
        with open(credentials_filepath, "r") as file:
            credentials = json.load(file)
        return praw.Reddit(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            password=credentials["password"],
            user_agent=credentials["user_agent"],
            username=credentials["username"],
        )

    def _make_directory(self) -> None:
        """
        Create a directory for the user if it doesn't exist.
        """
        if not os.path.exists(self.downloads_path):
            os.mkdir(self.downloads_path)
        if not os.path.exists(self.user_path):
            os.mkdir(self.user_path)

    def _check_none_type_submission(
        self, gallery_id: str
    ) -> Optional[praw.models.Submission]:
        """
        Check if the submission is of None.

        Args:
            gallery_id (str): ID of the submission.

        Returns:
            Optional[praw.models.Submission]: Submission instance if it exists, None otherwise.
        """
        post = self.reddit.submission(id=gallery_id)
        if post.author is None:
            logger.error(f"Submission with ID {gallery_id} was deleted.")
            return None
        elif not post.is_robot_indexable:
            logger.error(f"Submission with ID {gallery_id} was removed.")
            return None
        else:
            logger.debug(f"Submission with ID {gallery_id} is UP.")
            return post

    def _get_posts(self, posts_count: int = None) -> pd.DataFrame:
        """
        Returns DataFrame with metadata from obtained posts.

        Args:
            posts_count (int): limits max number of metadata loaded to dataframe

        Returns:
            pd.DataFrame: DataFrame with posts metadata (id, url, created_utc)
        """
        user_submissions = [
            (subm.id, subm.url, subm.created_utc)
            for subm in self.user.submissions.new(limit=posts_count)
        ]
        df = pd.DataFrame(user_submissions, columns=["id", "url", "created_utc"])
        logger.debug(f"{self.user_name} posts: {df}")
        return df

    def classify_urls(self, df):
        """Applies mapping to metdata:
        - "i" - Image,
        - "g" - Gallery,
        - "v" - Video,
        - "?" - Unknown source
        Args:
            df (pd.DataFrame): classify URLs in metadata df


        Returns:
            df : dataframe with metadata
        """
        df["type"] = df["url"].apply(
            lambda x: "i"
            if any(ext in x.lower() for ext in [".jpg", ".png", ".jpeg"])
            else "gif"
            if x.lower().endswith(".gif")
            else "i"
            if "i.redd.it" in x
            else "i"
            if "i.imgur" in x
            else "g"
            if "reddit.com/gallery" in x
            else "v"
            if "v.redd.it" in x
            else "?"
        )
        return df

    async def _download_image_from_url_async(
        self, session, url: str, filepath: str, format: str
    ) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        async with session.get(url) as response:
            content = await response.read()
            with open(f"{filepath}.{format}", "wb") as file:
                file.write(content)

    async def _download_image_from_gallery_async(
        self, session, gallery_id: str, filepath: str, format: str
    ) -> List[str]:
        try:
            post = self._check_none_type_submission(gallery_id)
            if post is not None:
                if hasattr(post, "media_metadata"):
                    url_gallery_list = [
                        i[1]["p"][0]["u"].split("?")[0].replace("preview", "i")
                        for i in post.media_metadata.items()
                    ]

                    tasks = [
                        self._download_image_from_url_async(
                            session,
                            url,
                            f"{filepath}-.{format}",
                            DEFAULT_IMAGE_FORMAT,
                        )
                        for url in url_gallery_list
                    ]

                    await asyncio.gather(*tasks)
                    return url_gallery_list
                else:
                    logger.error(
                        f"Submission with ID {gallery_id} does not have media metadata."
                    )
            else:
                logger.error(f"Submission with ID {gallery_id} is None.")
        except Exception as e:
            logger.error(
                f"An error occurred while downloading images from gallery: {e}"
            )

    async def get_images_async(self, name_by: str) -> None:
        format_mapping = {
            "i": "images",
            "gif": "gifs",
            "v": "videos",
        }

        try:
            df_classified = self.classify_urls(self._get_posts())
            logger.info(df_classified.to_string())

            async with aiohttp.ClientSession() as session:
                tasks = []
                for i, url in enumerate(df_classified["url"]):
                    if name_by == "id":
                        name_i = df_classified["id"][i]
                    elif name_by == "created_utc":
                        name_i = datetime.utcfromtimestamp(
                            df_classified["created_utc"][i]
                        ).strftime("%Y-%m-%d--%H-%M-%S")
                    parent_download_directory = f"{self.user_path}"

                    if df_classified["type"][i] == "g":
                        tasks.append(
                            self._download_image_from_gallery_async(
                                session,
                                gallery_id=df_classified["id"][i],
                                filepath=f"{parent_download_directory}/images/{name_i}",
                                format=DEFAULT_IMAGE_FORMAT,
                            )
                        )
                    elif df_classified["type"][i] == "?":
                        pass
                    else:
                        tasks.append(
                            self._download_image_from_url_async(
                                session,
                                url,
                                f"{parent_download_directory}/{format_mapping[df_classified['type'][i]]}/{name_i}",
                                format=url.split(".")[-1],
                            )
                        )

                await asyncio.gather(*tasks)

        except Exception as e:
            logger.error(f"An error occurred while getting images: {e}")
