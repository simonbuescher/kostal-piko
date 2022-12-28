from __future__ import annotations

import datetime
import logging
from typing import Any

import aiohttp
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from lxml import etree

from .const import (
    DOMAIN,
    PIKO_DEFAULT_USERNAME,
    PIKO_DEFAULT_PASSWORD,
    PIKO_DEFAULT_TIMEOUT,
    PIKO_INFORMATION_ENTRIES,
    PikoInformationEntry,
)

_LOGGER = logging.Logger(__name__)
PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    host = entry.data[CONF_HOST]
    user = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    try:
        piko = Piko(aiohttp_client.async_get_clientsession(hass), host=host, username=user, password=password)
    except Exception as exception:
        raise ConfigEntryNotReady from exception

    coordinator = PikoUpdateCoordinator(hass, piko)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    success = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if success:
        hass.data[DOMAIN].pop(entry.entry_id)
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)

    return success


class PikoUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, piko: Piko):
        self._hass = hass
        self._piko = piko

        self._keys_to_fetch = set()

        super().__init__(self._hass, _LOGGER, name=DOMAIN, update_interval=datetime.timedelta(seconds=15))

    def start_fetch_data(self, key: str):
        self._keys_to_fetch.add(key)

    def stop_fetch_data(self, key: str):
        if key in self._keys_to_fetch:
            self._keys_to_fetch.remove(key)

    async def _async_update_data(self):
        try:
            infos = await self._piko.get_data()
            return {key: value for key, value in infos.items() if key in self._keys_to_fetch}

        except Exception as exception:
            _LOGGER.warning("Fetching data from Piko failed: %s", exception, exc_info=True)
            raise UpdateFailed()


class Piko:
    def __init__(self, session, host: str,
                 username: str = PIKO_DEFAULT_USERNAME, password: str = PIKO_DEFAULT_PASSWORD,
                 timeout: int = PIKO_DEFAULT_TIMEOUT):
        self._session = session
        self._host = host
        self._username = username
        self._password = password
        self._timeout = timeout

    async def get_data(self) -> dict[str, Any]:
        html_response = await self._fetch_html()
        dom = etree.HTML(html_response)

        infos = {}
        for info_entry in PIKO_INFORMATION_ENTRIES:
            value_string = dom.xpath(info_entry.xpath)[0].text.strip()
            value = info_entry.converter(value_string)
            infos[info_entry.key] = value

        return infos

    async def _fetch_html(self) -> str:
        auth = aiohttp.BasicAuth(self._username, self._password)
        async with async_timeout.timeout(self._timeout):
            async with self._session.get(self._host, auth=auth, timeout=self._timeout) as response:
                return await response.text()
