import logging
import os
import re

import feedparser
from megapy import Mega
from pytfy import NtfyPublisher

RSS_FEED_URL = "https://drslumpbrasil.blogspot.com/feeds/posts/default"

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

    configs = {
        "download_folder": download_folder,
        "ntfy": {
            "domain": os.environ.get("NTFY_DOMAIN"),
            "topic": os.environ.get("NTFY_TOPIC"),
            "token": os.environ.get("NTFY_TOKEN"),
        },
    }

    return configs


def get_feed():
    """Get the complete feed from the RSS_FEED_URL and return it as a list of entries."""
    start_index = 1
    max_results = 150
    total_feed = []
    while True:
        url = f"{RSS_FEED_URL}?start-index={start_index}&max-results={max_results}"
        feed = feedparser.parse(url)
        feed_len = len(feed.entries)

        if feed_len == 0:
            break

        start_index += feed_len
        total_feed.extend(feed.entries)

    return total_feed


def get_mega_urls(content):
    """Get the mega URLs from the content and return it as a list."""
    urls = re.findall(r'https://mega\.nz/[^"]+', content)

    return urls


def download_from_content(download_url: str, download_folder: str):
    """Download the file from the mega_url and save it to the download_folder."""
    mega = Mega()
    mega.download_url(download_url, download_folder)


def main(configs):
    download_folder = configs["download_folder"]

    logger.info("Getting the feed from the RSS feed.")
    feed = get_feed()
    logger.info(f"Feed retrieved successfully. Got {len(feed)} entries.")

    for entry in feed:
        title = entry.title
        # Get only the 80's episodes
        if "Episódio" in title and "90's" not in title:
            logger.info(f"Processing the entry: {title}")
            content = entry.summary

            mega_urls = get_mega_urls(content)
            if not mega_urls:
                continue
            for url in mega_urls:
                download_from_content(url, download_folder)
            logger.info(f"Entry {title} processed successfully.")
        else:
            continue


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
