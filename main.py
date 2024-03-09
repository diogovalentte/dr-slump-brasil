import logging
import os

from pytfy import NtfyPublisher

from src.db import DB
from src.mega import download_from_url
from src.site import filter_feed, get_feed, get_mega_urls

logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s :: %(levelname)-8s :: %(name)s :: %(message)s",
)
logger = logging.getLogger()


def get_configs():
    """Read configs from environment variables and return it as a Python dictionary.

    Returns:
        dict: The keys of the JSON file.
    """
    download_folder = os.environ.get("DOWNLOAD_FOLDER")
    if not download_folder:
        raise ValueError("The DOWNLOAD_FOLDER environment variable is missing.")
    if not os.path.isabs(download_folder):
        raise ValueError("The download_folder key must be an absolute path.")
    if not os.path.exists(download_folder) or not os.path.isdir(download_folder):
        raise ValueError("The download_folder path does not exist or is not a folder.")

    db_path = os.environ.get("DB_PATH")

    configs = {
        "download_folder": download_folder,
        "db_path": db_path,
        "download_filter": os.environ.get("DOWNLOAD_FILTER"),
        "ntfy": {
            "domain": os.environ.get("NTFY_DOMAIN"),
            "topic": os.environ.get("NTFY_TOPIC"),
            "token": os.environ.get("NTFY_TOKEN"),
        },
    }

    return configs


def main(configs):
    download_folder = configs["download_folder"]
    db_path = configs["db_path"]

    db = DB(db_path)
    db.create_tables()

    logger.info("Getting the feed from the RSS feed.")
    feed = get_feed()
    logger.info(f"Feed retrieved successfully. Got {len(feed)} entries.")

    feed = filter_feed(feed, configs["download_filter"])

    for entry in feed:
        title = entry.title
        r = db.select(title)
        if r is not None:
            logger.info(f"The entry {title} has already been processed.")
            continue

        logger.info(f"Processing the entry: {title}")
        content = entry.summary

        mega_urls = get_mega_urls(content)
        if not mega_urls:
            continue
        for url in mega_urls:
            download_from_url(url, download_folder)

        db.insert(title)
        logger.info(f"Entry {title} processed successfully.")


if __name__ == "__main__":
    configs = get_configs()
    ntfy = NtfyPublisher(
        configs["ntfy"]["domain"], configs["ntfy"]["topic"], configs["ntfy"]["token"]
    )

    if configs["ntfy"]["domain"] is None:
        main(configs)
    else:
        try:
            main(configs)
        except Exception as ex:
            ntfy.post(
                f"A error occurred while downloading episodes from Dr. Slump Brasil:\n{ex}",
                "Dr. Slump Brasil download error",
            )
            raise ex
