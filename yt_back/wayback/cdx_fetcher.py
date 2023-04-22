import asyncio
import aiohttp

from typing import List
from collections.abc import Awaitable 

class CDXFetcher:
    def __init__(self, url_list: List[str]):
        self._url_list = url_list

    def _format(self, url: str) -> str:
        return f'https://web.archive.org/cdx/search/cdx?url={url}&output=json'

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()

        return self

    async def __aexit__(self, *args):
        await self._session.close()

    async def _get_cdx_data(self, url) -> Awaitable[List[List[str]]]:
        async with self._session.get(url) as r:
            return await r.json()

    async def fetch(self) -> List[List[str]]:
        tasks = []
        for raw_url in self._url_list:
            url = self._format(raw_url)
            tasks.append(asyncio.ensure_future(self._get_cdx_data(url)))

        return await asyncio.gather(*tasks)
