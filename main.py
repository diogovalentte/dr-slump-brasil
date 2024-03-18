import logging
import os

from megapy.exceptions import NotFoundException as MegaNotFoundException
from pytfy import NtfyPublisher

from src.db import DB
from src.download import download_from_url
from src.exceptions import InvalidDownloadFilter
from src.site import (
    filter_feed,
    get_download_type,
    get_download_urls,
    get_feed,
    get_filename_to_save,
    search_repost,
)

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

    download_filter = os.environ.get("DOWNLOAD_FILTER")
    if download_filter not in ["80show", "90show", "specials", "movies", "all"]:
        if not download_filter or download_filter == "":
            download_filter = "all"
        else:
            raise InvalidDownloadFilter

    files_uid = os.environ.get("FILES_UID")
    files_gid = os.environ.get("FILES_GID")
    if files_uid is None or files_gid is None:
        raise ValueError(
            "Environment variables FILES_UID and FILES_GID should be defined"
        )
    try:
        files_uid = int(files_uid)
        files_gid = int(files_gid)
    except ValueError as ex:
        raise ex

    configs = {
        "download_folder": download_folder,
        "download_filter": download_filter,
        "files_uid": files_uid,
        "files_gid": files_gid,
        "db_path": os.environ.get("DB_PATH"),
        "ntfy": {
            "address": os.environ.get("NTFY_ADDRESS"),
            "topic": os.environ.get("NTFY_TOPIC"),
            "token": os.environ.get("NTFY_TOKEN"),
        },
    }

    return configs


def main(configs):
    download_folder = configs["download_folder"]
    download_filter = configs["download_filter"]
    files_uid = configs["files_uid"]
    files_gid = configs["files_gid"]
    db_path = configs["db_path"]

    db = DB(db_path)
    db.create_tables()

    logger.info("Getting the feed from the RSS feed.")
    feed = get_feed()
    feed = filter_feed(feed, download_filter)
    feed.reverse()
    logger.info(f"Feed retrieved successfully. Got {len(feed)} entries.")

    for index, entry in enumerate(feed):
        title = entry.title
        if db.select(title) is not None:
            logger.info(f"The entry {title} has already been processed.")
            continue

        logger.info(f"Processing the entry: {title}")
        summary = entry.summary

        if download_filter == "all":
            download_type = get_download_type(title, summary)
            if download_type is None:
                raise ValueError(
                    f"The entry's download type could not be determined from the title and summary.\nTitle: {title}\nSummary: {summary}"
                )
        else:
            download_type = download_filter

        download_urls = get_download_urls(summary)
        is_double_episode = "Episódios 29 e 30" in title
        double_episode_names = ["Episódio 29", "Episódio 30"]
        for url in download_urls:
            try:
                if is_double_episode:
                    title = double_episode_names.pop(0)
                filename = get_filename_to_save(title, download_type)
                download_path = os.path.join(download_folder, filename)
                download_from_url(url, download_path, files_uid, files_gid)
            except MegaNotFoundException as ex:
                logger.error(f"Error while downloading {title} from url: {url}:\n{ex}")
                download_urls.pop(0)

                if len(download_urls) < 1:
                    repost = search_repost(title, feed, download_type)
                    repost_index = repost[0]
                    repost_entry = repost[1]
                    if repost_entry is not None:
                        logger.info(
                            f"Could not download {title}, but found repost {repost_entry.title}, will download it instead."
                        )
                        feed.pop(repost_index)
                        feed.insert(index + 1, repost_entry)
                        continue

                    raise ex

        db.insert(title)
        logger.info(f"Entry {title} processed successfully.")
        if ntfy is not None:
            ntfy.post(
                f"Dr. Slump episode {title} downloaded successfully.",
                "Dr. Slump Brasil download success",
            )


if __name__ == "__main__":
    configs = get_configs()

    if configs["ntfy"]["address"] is None or configs["ntfy"]["address"] == "":
        ntfy = None
        try:
            main(configs)
        except Exception as ex:
            logger.error(
                "A error occurred while downloading episodes from Dr. Slump Brasil"
            )
            raise ex
    else:
        ntfy = NtfyPublisher(
            configs["ntfy"]["address"],
            configs["ntfy"]["topic"],
            configs["ntfy"]["token"],
        )
        try:
            main(configs)
        except Exception as ex:
            logger.error(
                "A error occurred while downloading episodes from Dr. Slump Brasil"
            )
            ntfy.post(
                f"A error occurred while downloading episodes from Dr. Slump Brasil:\n{ex}",
                "Dr. Slump Brasil download error",
            )
            raise ex
