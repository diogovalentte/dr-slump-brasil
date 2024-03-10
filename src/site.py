import re

import feedparser

from src.exceptions import InvalidDownloadFilter

RSS_FEED_URL = "https://drslumpbrasil.blogspot.com/feeds/posts/default"


def get_feed() -> list[feedparser.FeedParserDict]:
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


def get_download_urls(summary):
    """Get the download URLs from the content and return it as a list."""
    urls = []

    summary = summary.replace("mega.co.nz", "mega.nz")
    mega_urls = re.findall(r'https://mega\.nz/[^"]+', summary)
    urls.extend(mega_urls)

    gdrive_urls = re.findall(r'https://drive\.google\.com/[^"]+', summary)
    get_id_pattern = r"https://drive.google.com/file/d/([^/]+)/"
    for url in gdrive_urls:
        match = re.search(get_id_pattern, url)
        if match:
            file_id = match.group(1)
            urls.append(f"https://drive.google.com/uc?id={file_id}")

    onedrive_urls = re.findall(r'https:\/\/onedrive\.live\.com\/[^"]+', summary)
    urls.extend(onedrive_urls)

    return list(set(urls))


def filter_feed(feed: list, filter: str):
    """Filter a feed based on the filter argument. If the filter is an empty string, return the feed as is.

    Args:
        feed (list): List of feed entries.
        filter (type): Keyword to filter the feed. Can be: 80show, 90show, specials, movies, all. Defaults to "".

    Returns:
        (list): Filtered feed.
    """
    match filter:
        case "80show":
            return [
                entry
                for entry in feed
                if is_80_show_episode(entry.title, entry.summary)
            ]
        case "90show":
            return [
                entry
                for entry in feed
                if is_90_show_episode(entry.title, entry.summary)
            ]
        case "specials":
            return [entry for entry in feed if is_special(entry.title, entry.summary)]
        case "movies":
            return [entry for entry in feed if is_movie(entry.title, entry.summary)]
        case "all":
            return feed
        case _:
            raise InvalidDownloadFilter


def get_download_type(title, summary):
    """Get the download type based on the title and summary.

    Args:
        title (str): Title of the entry.
        summary (str): Summary of the entry.

    Returns:
        (str | None): Media type. Can be: 80show, 90show, specials, movies. None if unknown.
    """
    if is_80_show_episode(title, summary):
        return "80show"
    elif is_90_show_episode(title, summary):
        return "90show"
    elif is_special(title, summary):
        return "specials"
    elif is_movie(title, summary):
        return "movies"
    else:
        return None


def is_80_show_episode(title, _):
    return "Episódio" in title and "90's" not in title


def is_90_show_episode(title, _):
    return "Episódio" in title and "90's" in title


def is_special(title, _):
    return "Episódio" not in title and ("Especial" in title or "Special" in title)


def is_movie(title, content):
    # Maybe can return something that is not a movie, like a post about a movie
    return (
        "Episódio" not in title
        and "Especial" not in title
        and ("Filme" in content or "filme" in content)
    )


def get_filename_to_save(title: str, download_type: str):
    """Get the filename to save the file based on the title.

    Args:
        title (str): Title of the file.
        download_type (str): Can be: 80show, 90show, specials, movies.

    Returns:
        (str | None): Filename to save the file. None if the media_type is not supported.
    """
    match download_type:
        case "80show":
            pattern = r"\b(\d+)\b"
            match = re.search(pattern, title)
            if match:
                number = match.group(1)
            else:
                raise ValueError(f"Cannot extract the episode number of title: {title}")
            return f"Dr. Slump & Arale-chan (1981) - {number.zfill(3)}.mkv"
        case "90show":
            pattern = r"Episódio (\d+)"
            match = re.search(pattern, title)
            if match:
                number = match.group(1)
            else:
                raise ValueError(f"Cannot extract the episode number of title: {title}")
            return f"Dr. Slump (1997) - {number.zfill(3)}.mkv"
        case "specials":
            return f"Special - {title}.mkv"
        case "movies":
            return f"Movie - {title}.mkv"
        case _:
            raise InvalidDownloadFilter


def search_repost(
    title: str, feed: list, download_type: str
) -> tuple[int, feedparser.FeedParserDict | None]:
    """Search for a repost of the title in the feed and return it."""
    match download_type:
        case "80show":
            return (-1, None)
        case "90show":
            pattern = r"Dr\. Slump \(90's\) Episódio \d+:"
            result = re.search(pattern, title)
            if result:
                match = result.group()
                for index, entry in enumerate(feed):
                    if (
                        entry.title.startswith(match)
                        and "repost" in entry.title.lower()
                        and entry.title != title
                    ):
                        return index, entry
            return (-1, None)
        case "specials":
            return (-1, None)
        case "movies":
            return (-1, None)
        case _:
            return (-1, None)
