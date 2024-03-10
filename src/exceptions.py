class InvalidDownloadFilter(Exception):
    def __str__(self) -> str:
        return "The DOWNLOAD_FILTER must be one of the following values: 80show, 90show, specials, movies, all."
