"""Base entity for Liquid Check."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import LiquidCheckCoordinator


class LiquidCheckEntity(CoordinatorEntity[LiquidCheckCoordinator]):
    """Base class for Liquid Check entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: LiquidCheckCoordinator,
        key: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._attr_unique_id = (
            f"{coordinator.entry.unique_id or coordinator.entry.entry_id}_{key}"
        )
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    coordinator.entry.unique_id
                    or coordinator.entry.entry_id,
                )
            },
            name=coordinator.entry.title,
            manufacturer="Liquid Check",
            model="Liquid Check",
            configuration_url=coordinator.api.base_url,
        )
