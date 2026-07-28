"""Sensor platform for Liquid Check."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfLength,
    UnitOfVolume,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import LiquidCheckCoordinator
from .entity import LiquidCheckEntity


@dataclass(frozen=True, kw_only=True)
class LiquidCheckSensorDescription(SensorEntityDescription):
    """Describe a Liquid Check sensor."""

    value_fn: Callable[[dict[str, Any]], Any]


SENSOR_DESCRIPTIONS = (
    LiquidCheckSensorDescription(
        key="content",
        translation_key="content",
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        icon="mdi:water",
        value_fn=lambda data: data.get("content"),
    ),
    LiquidCheckSensorDescription(
        key="level",
        translation_key="level",
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        icon="mdi:arrow-expand-vertical",
        value_fn=lambda data: data.get("level"),
    ),
    LiquidCheckSensorDescription(
        key="percent",
        translation_key="percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        icon="mdi:gauge",
        value_fn=lambda data: data.get("percent"),
    ),
    LiquidCheckSensorDescription(
        key="last_success",
        translation_key="last_success",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:clock-check-outline",
        value_fn=lambda data: data.get("last_success"),
    ),
    LiquidCheckSensorDescription(
        key="last_error",
        translation_key="last_error",
        icon="mdi:alert-circle-outline",
        entity_registry_enabled_default=False,
        value_fn=lambda data: data.get("last_error") or "Kein Fehler",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Liquid Check sensors."""
    coordinator: LiquidCheckCoordinator = entry.runtime_data

    async_add_entities(
        LiquidCheckSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    )


class LiquidCheckSensor(LiquidCheckEntity, SensorEntity):
    """Representation of a Liquid Check sensor."""

    entity_description: LiquidCheckSensorDescription

    def __init__(
        self,
        coordinator: LiquidCheckCoordinator,
        description: LiquidCheckSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, description.key)
        self.entity_description = description


    @property
    def native_value(self) -> float | str | datetime | None:
        """Return the current sensor value."""
        if not self.coordinator.data:
            return None

        return self.entity_description.value_fn(
            self.coordinator.data
        )
