import logging

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import PikoUpdateCoordinator
from .const import DOMAIN, UNIQUE_ID, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    device_info = DeviceInfo(
        configuration_url=entry.data[CONF_HOST],
        identifiers={(DOMAIN, UNIQUE_ID)},
        manufacturer="Kostal",
        name="Piko",
    )

    async_add_entities(PikoSensor(coordinator, description, device_info) for description in SENSOR_TYPES)


class PikoSensor(CoordinatorEntity[PikoUpdateCoordinator], SensorEntity):
    def __init__(self, coordinator: PikoUpdateCoordinator, description: SensorEntityDescription,
                 device_info: DeviceInfo):
        super().__init__(coordinator)
        self._info_key = description.key
        self._attr_device_info = device_info
        self._attr_unique_id = f"piko_{description.key.lower()}"
        self.entity_description = description

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.coordinator.start_fetch_data(self._info_key)

    async def async_will_remove_from_hass(self):
        self.coordinator.stop_fetch_data(self._info_key)
        await super().async_will_remove_from_hass()

    @property
    def available(self) -> bool:
        return super().available and self.coordinator.data is not None and self._info_key in self.coordinator.data

    @callback
    def _handle_coordinator_update(self):
        if self.available:
            new_value = self.coordinator.data[self._info_key]
            self._attr_native_value = new_value
            self.async_write_ha_state()
