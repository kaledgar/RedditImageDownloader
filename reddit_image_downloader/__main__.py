import logging
from pprint import pformat
from pathlib import Path

from .config import get_config_from_cli
from .constants import DEFAULT_DOWNLOADS_PATH
from .reddit_image_downloader import RedditImageDownloader
from .duplicate_removal import FileDuplicateRemover

if __name__ == "__main__":
    config = get_config_from_cli()

    # set logger
    logging.basicConfig(level=logging.DEBUG if config.verbose else logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"Running {__name__} with config:\n {pformat(config)}")

    for name in config.users:
        rid = RedditImageDownloader(name)
        rid.get_images(name_by=config.naming)

        logger.info(f"""Deleting duplicate images in {f"{config.directory}/{name}"}""")

        if config.remove_duplicates is True:
            duplicate_remover = FileDuplicateRemover(
                directory_path=f"{config.directory}/{name}"
            )
