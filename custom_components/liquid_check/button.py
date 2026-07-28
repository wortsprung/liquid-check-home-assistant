"""Button platform for Liquid Check."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
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
    """Set up the Liquid Check measurement button."""
    coordinator: LiquidCheckCoordinator = entry.runtime_data
    async_add_entities([LiquidCheckMeasureButton(coordinator)])


class LiquidCheckMeasureButton(LiquidCheckEntity, ButtonEntity):
    """Button that starts a physical measurement."""

    _attr_translation_key = "measure"
    _attr_icon = "mdi:refresh"

    def __init__(
        self,
        coordinator: LiquidCheckCoordinator,
    ) -> None:
        """Initialize the measurement button."""
        super().__init__(coordinator, "measure")

    async def async_press(self) -> None:
        """Start a new measurement."""
        await self.coordinator.async_measure()
