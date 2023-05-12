import sys
import csv
import yt_dlp
import asyncio
import time

from yt_dlp.utils import DownloadError
from typing import Optional, Mapping, Any

from yt_back.wayback.cdx_iterator import CDXIterator
from yt_back.wayback.cdx_fetcher import CDXFetcher


def archive_url_fmt(timestamp: str, url: str) -> str:
    return f'https://web.archive.org/web/{timestamp}/{url}'

def check_url(url: str) -> bool:
    # Suppress the yt_dlp logger here
    # Add log for attempt
    with yt_dlp.YoutubeDL() as dl:
        try:
            info = dl.extract_info(url, download=False)
            return info not in (None, {})
        except DownloadError as exp:
            pass

    return False

async def filter_url(cdx: CDXFetcher) -> str:
    for data in await cdx.fetch():
        iterator = CDXIterator(data)

        for row in csv.DictReader(iterator, delimiter=iterator.delimiter):
            archive_url = archive_url_fmt(
                timestamp=row['timestamp'],
                url=row['original'],
            )

            # Maybe skip the test and download it at once
            # If that's the case, there will be no need to suppress yt_dlp's logger
            if check_url(archive_url):
                yield archive_url
                break

async def main():
    urls = sys.argv[1:]

    async with CDXFetcher(urls) as cdx:
        archived_urls = [a_url async for a_url in filter_url(cdx)]

        with yt_dlp.YoutubeDL() as ydl:
            ydl.download(archived_urls)
