"""Binary sensor platform for Liquid Check."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import LiquidCheckCoordinator
from .entity import LiquidCheckEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Liquid Check connection sensor."""
    coordinator: LiquidCheckCoordinator = entry.runtime_data
    async_add_entities([LiquidCheckConnectionSensor(coordinator)])


class LiquidCheckConnectionSensor(
    LiquidCheckEntity,
    BinarySensorEntity,
):
    """Show whether Liquid Check is reachable."""

    _attr_translation_key = "connection"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_icon = "mdi:lan-connect"

    def __init__(
        self,
        coordinator: LiquidCheckCoordinator,
    ) -> None:
        """Initialize the connection sensor."""
        super().__init__(coordinator, "connection")

    @property
    def is_on(self) -> bool:
        """Return whether the device is connected."""
        if not self.coordinator.data:
            return False

        return bool(
            self.coordinator.data.get("connected", False)
        )
