import logging

from .constants import DEFAULT_USER_NAMES
from .reddit_image_downloader import RedditImageDownloader

logger = logging.getLogger(__name__)

for name in DEFAULT_USER_NAMES:
    rid = RedditImageDownloader(name)
    df = rid._get_posts()
    df1 = rid.classify_urls(df)

print(df1.to_string())

rid.get_images(name_by="id")
