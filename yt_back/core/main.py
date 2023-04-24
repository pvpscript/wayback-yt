import sys
import csv
import yt_dlp
import asyncio

from yt_back.wayback.cdx_iterator import CDXIterator
from yt_back.wayback.cdx_fetcher import CDXFetcher

def archive_url_fmt(timestamp, url):
    return f'https://web.archive.org/web/{timestamp}/{url}'

async def task(orig, url):
    with yt_dlp.YoutubeDL() as dl:
        info = dl.extract_info(url, download=False)
        return orig, info.get('format')

async def main():
    urls = sys.argv[1:]

    async with CDXFetcher(urls) as f:
        for r in await f.fetch():
            iterator = CDXIterator(r)

            tasks = []
            for row in csv.DictReader(iterator, delimiter=iterator.delimiter):
                #print(row['timestamp'], row['statuscode'])
                original = row['original']
                archive_url = archive_url_fmt(row['timestamp'], original)
                tasks.append(asyncio.ensure_future(task(original, archive_url)))

            for i in await asyncio.gather(*tasks):
                print(i)
