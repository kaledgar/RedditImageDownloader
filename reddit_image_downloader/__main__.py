import logging
from pprint import pformat

from .config import get_config_from_cli
from .constants import DEFAULT_USER_NAMES
from .reddit_image_downloader import RedditImageDownloader

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    config = get_config_from_cli()
    logger.info(f"Running {__name__} with config:\n {pformat(config)}")

for name in DEFAULT_USER_NAMES:
    rid = RedditImageDownloader(name)
    df = rid._get_posts()
    df1 = rid.classify_urls(df)

print(df1.to_string())

rid.get_images(name_by="id")
