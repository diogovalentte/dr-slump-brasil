import re

import feedparser

RSS_FEED_URL = "https://drslumpbrasil.blogspot.com/feeds/posts/default"


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


def filter_feed(feed: list, filter: str = ""):
    """Filter a feed based on the filter argument. If the filter is an empty string, return the feed as is.

    Args:
        feed (list): List of feed entries.
        filter (type): Keyword to filter the feed. Can be: 80show, 90show, special, movie, "". Defaults to "".

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
        case "special":
            return [entry for entry in feed if is_special(entry.title, entry.summary)]
        case "movie":
            return [entry for entry in feed if is_movie(entry.title, entry.summary)]
        case _:
            return feed


def is_80_show_episode(title, _):
    return "Episódio" in title and "90's" not in title


def is_90_show_episode(title, _):
    return "Episódio" in title and "90's" in title


def is_special(title, _):
    return "Episódio" not in title and "Especial" in title


def is_movie(title, content):
    # Maybe can return something that is not a movie, like a post about a movie
    return (
        "Episódio" not in title
        and "Especial" not in title
        and ("Filme" in content or "filme" in content)
    )
