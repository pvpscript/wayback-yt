import asyncio
import aiohttp

from typing import List
from collections.abc import Iterator

class CdxFetcher:
    def __init__(self, url_list: List[str]):
        self._url_list = url_list

    def _format(self, url: str) -> str:
        return f'https://web.archive.org/cdx/search/cdx?url={url}&output=json'

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()

        return self

    async def __aexit__(self, *args):
        await self._session.close()

    async def fetch(self) -> Iterator[List[List[str]]]:
        for url in self._url_list:
            async with self._session.get(self._format(url)) as r:
                yield await r.json()
