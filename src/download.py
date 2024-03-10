import os

import gdown
from megapy import Mega

from src.site import get_filename_to_save


def download_from_url(
    download_url: str, download_folder: str, title: str, media_type: str
):
    if "mega.nz" in download_url:
        download_mega(download_url, download_folder)
    elif "drive.google.com" in download_url:
        filename = get_filename_to_save(title, media_type)
        if filename is None:
            raise ValueError(
                f"Media type: {media_type} is not supported while getting filename to save."
            )
        download_gdrive(download_url, download_folder, filename)
    else:
        raise ValueError("The download_url is not supported.")


def download_mega(download_url: str, download_folder: str):
    """Download the file from the download_url and save it to the download_folder."""
    mega = Mega()
    mega.download_url(download_url, download_folder)


def download_gdrive(download_url: str, download_folder: str, filename: str):
    """Download the file from the download_url and save it to the download_folder."""
    file_path = os.path.join(download_folder, filename)
    gdown.download(download_url, file_path)
