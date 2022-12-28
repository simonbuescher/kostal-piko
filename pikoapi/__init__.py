from __future__ import annotations

from typing import Iterable, Tuple, Any

import aiohttp
import async_timeout
from lxml import etree

from .config import InfoEntry, InfoEntries


class Piko:
    def __init__(self, session: aiohttp.ClientSession, host: str,
                 username: str = config.DEFAULT_USERNAME, password: str = config.DEFAULT_PASSWORD,
                 timeout: int = config.DEFAULT_TIMEOUT):
        self._session = session
        self._host = host
        self._username = username
        self._password = password
        self._timeout = timeout

    async def get_data(self) -> Infos:
        html_response = await self._fetch_html()

        dom = etree.HTML(html_response)
        infos = Infos()

        for info_entry in InfoEntries.all():
            value_string = dom.xpath(info_entry.xpath)[0].text.strip()
            value = info_entry.converter(value_string)
            infos.add_entry(info_entry, value)

        return infos

    async def _fetch_html(self) -> str:
        auth = aiohttp.BasicAuth(self._username, self._password)
        try:
            async with async_timeout.timeout(self._timeout):
                async with self._session.get(self._host, auth=auth, timeout=self._timeout) as response:
                    return await response.text()

        except Exception as exception:
            print(f"error: {exception}")


class Infos:
    def __init__(self):
        self._infos = {}

    def add_entry(self, info_entry: InfoEntry, value: Any):
        self._infos[info_entry] = value

    def get(self, info: InfoEntry) -> Any:
        if info not in self._infos:
            raise ValueError(f"Key {info} is not present in {self}")
        return self._infos[info]

    def __iter__(self) -> Iterable[Tuple[InfoEntry, Any]]:
        return iter(self._infos.items())

    def __repr__(self) -> str:
        return f"Info({ {entry.key: value for entry, value in self._infos.items()} })"
