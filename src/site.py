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
