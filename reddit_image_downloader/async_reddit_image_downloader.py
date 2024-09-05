import json
import logging
import os
from datetime import datetime
import pandas as pd
import asyncpraw
import re
from typing import Optional, List, Dict, Any

import aiohttp
import asyncio
import aiofiles
from tqdm.asyncio import tqdm

from .constants import (
    DEFAULT_CREDENTIALS_FILEPATH,
    DEFAULT_DOWNLOADS_PATH,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

file_type_regex_mapping: Dict[str, re.Pattern] = {
    "image": re.compile(r"\.(jpg|jpeg|png)", re.IGNORECASE),
    "gif": re.compile(r"\.(gif|gifv)", re.IGNORECASE),
    "gallery": re.compile(r"reddit\.com/gallery", re.IGNORECASE),
    "reddit_video": re.compile(r"v\.redd\.it", re.IGNORECASE),
    "external_video": re.compile(r"/watch", re.IGNORECASE),
}


def categorize_string(s: str) -> str:
    """
    Categorize a given string based on its content.

    Args:
        s (str): The string to categorize.

    Returns:
        str: The category of the string.
    """
    for key, regex in file_type_regex_mapping.items():
        if regex.search(s):
            return key
    return "unknown"


class RedditImageDownloader:
    def __init__(
        self,
        user_name: str,
        submissions_limit: int = 1000,
        name_by: str = "created_utc",
        downloads_path: str = DEFAULT_DOWNLOADS_PATH,
    ) -> None:
        """
        Initialize the RedditImageDownloader.

        Args:
            user_name (str): The Reddit username.
            submissions_limit (int, optional): The maximum number of submissions to fetch. Defaults to 1000.
            name_by (str, optional): The attribute to name downloaded files by. Defaults to "created_utc".
            downloads_path (str, optional): The path to the downloads directory. Defaults to DEFAULT_DOWNLOADS_PATH.
        """
        self.user_name = user_name
        self.name_by = name_by
        self.submissions_limit = submissions_limit
        self.global_downloads_path = downloads_path
        self.user_downloads_path = os.path.join(
            self.global_downloads_path, self.user_name
        )

        logger.info(
            "\n"
            f"╔══════════════════════════════════════════════════════╗\n"
            f"║           Initialized RedditImageDownloader          ║\n"
            f"╠══════════════════════════════════════════════════════╣\n"
            f"║  Reddit Username  : {self.user_name:<33}║\n"
            f"║  Submissions Limit: {self.submissions_limit:<33}║\n"
            f"║  Naming Files By  : {self.name_by:<33}║\n"
            f"║  Downloads Path   : {self.global_downloads_path:<33}║\n"
            f"╚══════════════════════════════════════════════════════╝"
        )

    @staticmethod
    def get_reddit_from_filepath(credentials_filepath: str) -> asyncpraw.Reddit:
        """
        Load Reddit instance from credentials file.

        Args:
            credentials_filepath (str): Path to the credentials file.

        Returns:
            asyncpraw.Reddit: Initialized Reddit instance.
        """
        with open(credentials_filepath, "r") as file:
            credentials = json.loads(file.read())
        return asyncpraw.Reddit(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            password=credentials["password"],
            user_agent=credentials["user_agent"],
            username=credentials["username"],
        )

    def make_directory(self) -> None:
        """
        Create a directory for the user if it doesn't exist.
        """
        os.makedirs(self.user_downloads_path, exist_ok=True)

    async def fetch_user_submissions(self, reddit: asyncpraw.Reddit) -> pd.DataFrame:
        """
        Fetch user submissions from Reddit.

        Args:
            reddit (asyncpraw.Reddit): Reddit instance.

        Returns:
            pd.DataFrame: DataFrame containing submission details.
        """
        submissions_list: List[Dict[str, Any]] = []
        redditor = await reddit.redditor(self.user_name)
        async for submission in redditor.new(limit=self.submissions_limit):
            if hasattr(submission, "url"):
                row_dict = {
                    "id": submission.id,
                    "url": submission.url,
                    "created_utc": datetime.fromtimestamp(submission.created_utc),
                    "title": submission.title,
                }
                submissions_list.append(row_dict)
        user_content_df = pd.DataFrame(submissions_list)
        user_content_df["type"] = user_content_df["url"].apply(categorize_string)
        logger.info(f"Fetched and classified {len(user_content_df)} unique submissions")
        return user_content_df

    async def download_image_from_url(
        self,
        http_session: aiohttp.ClientSession,
        source_url: str,
        target_filepath: os.PathLike,
    ) -> None:
        """
        Download an image from a URL.

        Args:
            http_session (aiohttp.ClientSession): HTTP session for making requests.
            source_url (str): The URL of the image.
            target_filepath (os.PathLike): The file path to save the image.
        """
        os.makedirs(os.path.dirname(target_filepath), exist_ok=True)
        async with http_session.get(source_url) as response:
            content = await response.read()
            async with aiofiles.open(target_filepath, "wb") as file:
                await file.write(content)

    async def _check_none_type_submission(
        self, gallery_id: str
    ) -> Optional[asyncpraw.models.Submission]:
        """
        Check if the submission is of None type.

        Args:
            gallery_id (str): ID of the submission.

        Returns:
            Optional[asyncpraw.models.Submission]: Submission instance if it exists, None otherwise.
        """
        post = await self.reddit_client.submission(id=gallery_id)
        if post.author is None:
            logger.info(f"Submission with ID {gallery_id} was deleted.")
            return None
        if not post.is_robot_indexable:
            logger.info(f"Submission with ID {gallery_id} was removed.")
            return None
        logger.debug(f"Submission with ID {gallery_id} is UP.")
        return post

    async def download_images_from_gallery(
        self,
        http_session: aiohttp.ClientSession,
        gallery_id: str,
        target_directory: str,
        entity_name: str,
    ) -> List[str]:
        """
        Download images from a Reddit gallery.

        Args:
            http_session (aiohttp.ClientSession): HTTP session for making requests.
            gallery_id (str): ID of the gallery.
            target_directory (str): Directory to save the images.
            entity_name (str): Name to use for the images.

        Returns:
            List[str]: List of image URLs.
        """
        try:
            post = await self._check_none_type_submission(gallery_id)
            if post and hasattr(post, "media_metadata"):
                url_gallery_list = [
                    item[1]["p"][0]["u"].split("?")[0].replace("preview", "i")
                    for item in post.media_metadata.items()
                ]
                tasks = [
                    self.download_image_from_url(
                        http_session,
                        url,
                        os.path.join(
                            target_directory, f"{entity_name}-{i}.{url.split('.')[-1]}"
                        ),
                    )
                    for i, url in enumerate(url_gallery_list)
                ]
                await asyncio.gather(*tasks)
                return url_gallery_list
            logger.error(
                f"Submission with ID {gallery_id} does not have media metadata."
            )
        except Exception as e:
            logger.error(f"Error downloading images from gallery: {e}")
        return []

    async def fetch_images(self) -> None:
        """
        Fetch images based on user submissions and categorize them.
        """
        image_download_dir = os.path.join(self.user_downloads_path, "images")
        gif_download_dir = os.path.join(self.user_downloads_path, "gif")
        timeout = aiohttp.ClientTimeout(total=3600)
        async with aiohttp.ClientSession(timeout=timeout) as http_session:
            tasks = []
            for _, row in self.user_content_df.iterrows():
                url_ext = row["url"].split(".")[-1]
                if row["type"] == "image":
                    target_filepath = os.path.join(
                        image_download_dir, f"{row[self.name_by]}.{url_ext}"
                    )
                    tasks.append(
                        self.download_image_from_url(
                            http_session=http_session,
                            source_url=row["url"],
                            target_filepath=target_filepath,
                        )
                    )
                elif row["type"] == "gallery":
                    tasks.append(
                        self.download_images_from_gallery(
                            http_session=http_session,
                            gallery_id=row["id"],
                            target_directory=image_download_dir,
                            entity_name=str(row[self.name_by]),
                        )
                    )
                elif row["type"] == "gif":
                    target_filepath = os.path.join(
                        gif_download_dir, f"{row[self.name_by]}.{url_ext}"
                    )
                    tasks.append(
                        self.download_image_from_url(
                            http_session=http_session,
                            source_url=row["url"],
                            target_filepath=target_filepath,
                        )
                    )
                else:
                    logger.info(f"Skipping unsupported type: {row['type']}")
            await tqdm.gather(*tasks, desc="Downloading content", total=len(tasks))

    async def download_manager(self) -> None:
        """
        Manage the download process by fetching submissions and images.
        """
        self.reddit_client = self.get_reddit_from_filepath(DEFAULT_CREDENTIALS_FILEPATH)
        try:
            self.user_content_df = await self.fetch_user_submissions(self.reddit_client)
            await self.fetch_images()
        finally:
            await self.reddit_client.close()

    def execute(self) -> None:
        """
        Execute the download process.
        """
        self.make_directory()
        asyncio.run(self.download_manager())
