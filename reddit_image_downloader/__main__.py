import logging
from pprint import pformat

from .config import get_config_from_cli
from .constants import DEFAULT_USER_NAMES, DEFAULT_DOWNLOADS_PATH
from .reddit_image_downloader import RedditImageDownloader
from .duplicate_removal import ImageDuplicateRemoval

if __name__ == "__main__":
    config = get_config_from_cli()
    logging.basicConfig(level=logging.DEBUG if config.verbose else logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"Running {__name__} with config:\n {pformat(config)}")

    for name in config.users:
        rid = RedditImageDownloader(name)
        rid.get_images(name_by=config.naming)

        logger.info(
            f"""Deleting duplicate images in {f"{DEFAULT_DOWNLOADS_PATH}/{name}"}"""
        )

        if config.remove_duplicates is True:
            duplicate_remover = ImageDuplicateRemoval(
                paths=[f"{DEFAULT_DOWNLOADS_PATH}/{name}"],
                username=name,
            )
