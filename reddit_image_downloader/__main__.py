import asyncio
import logging
from pprint import pformat
from pathlib import Path
from .config import get_config_from_cli
from .constants import DEFAULT_DOWNLOADS_PATH
from .reddit_image_downloader import RedditImageDownloader
from .duplicate_removal import FileDuplicateRemover


async def main():
    config = get_config_from_cli()

    # Set up logger
    logging.basicConfig(level=logging.DEBUG if config.verbose else logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"Running {__name__} with config:\n {pformat(config)}")

    # Download images for each user
    for name in config.users:
        rid = RedditImageDownloader(name)
        await rid.get_images_async(name_by=config.naming)

        # Remove duplicate images if configured to do so
        logger.info(f"Deleting duplicate images in {config.directory}/{name}")
        if config.remove_duplicates:
            FileDuplicateRemover(directory_path=f"{config.directory}/{name}")


if __name__ == "__main__":
    asyncio.run(main())
