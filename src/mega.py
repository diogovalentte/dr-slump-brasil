from megapy import Mega


def download_from_url(download_url: str, download_folder: str):
    """Download the file from the mega_url and save it to the download_folder."""
    mega = Mega()
    mega.download_url(download_url, download_folder)
