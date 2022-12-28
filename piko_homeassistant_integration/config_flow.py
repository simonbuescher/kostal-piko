import logging

import voluptuous
from homeassistant import config_entries
from homeassistant.const import CONF_BASE, CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import aiohttp_client

from . import Piko
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SETUP_SCHEMA = voluptuous.Schema({
    voluptuous.Required(CONF_HOST): str,
    voluptuous.Required(CONF_USERNAME): str,
    voluptuous.Required(CONF_PASSWORD): str,
})


class PikoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            try:
                session = aiohttp_client.async_get_clientsession(self.hass)
                piko = Piko(
                    session,
                    host=user_input[CONF_HOST],
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD]
                )
                await piko.get_data()

                return self.async_create_entry(title=f"Piko at {user_input[CONF_HOST]}", data=user_input)

            except Exception as exception:
                _LOGGER.exception("Exception while trying to connect to Piko: %s", exception)
                errors[CONF_BASE] = "general"

        return self.async_show_form(step_id="user", data_schema=SETUP_SCHEMA, errors=errors)
