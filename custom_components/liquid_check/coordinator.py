"""Data coordinator for Liquid Check."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import LiquidCheckApi, LiquidCheckApiError
from .const import (
    CONF_KEEP_LAST_VALUE,
    CONF_MEASURE_DELAY,
    DEFAULT_KEEP_LAST_VALUE,
    DEFAULT_MEASURE_DELAY,
)


class LiquidCheckCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinate updates from a Liquid Check device."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api: LiquidCheckApi,
        update_interval: timedelta,
        max_volume: float,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger=__import__("logging").getLogger(__name__),
            name=entry.title,
            update_interval=update_interval,
        )
        self.entry = entry
        self.api = api
        self.max_volume = max_volume
        self._last_valid_data: dict[str, Any] | None = None

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch fresh data from Liquid Check."""
        keep_last = self.entry.options.get(
            CONF_KEEP_LAST_VALUE,
            self.entry.data.get(
                CONF_KEEP_LAST_VALUE,
                DEFAULT_KEEP_LAST_VALUE,
            ),
        )

        try:
            measurement = await self.api.async_get_measurement()
        except LiquidCheckApiError as err:
            if keep_last and self._last_valid_data is not None:
                retained = dict(self._last_valid_data)
                retained["connected"] = False
                retained["last_error"] = str(err)
                return retained

            raise UpdateFailed(str(err)) from err

        content = measurement["content"]
        level = measurement["level"]
        percent = (
            min(max((content / self.max_volume) * 100, 0), 100)
            if self.max_volume > 0
            else 0
        )

        result = {
            "content": content,
            "level": level,
            "percent": percent,
            "connected": True,
            "last_success": datetime.now(UTC),
            "last_error": None,
        }
        self._last_valid_data = result
        return result

    async def async_measure(self) -> None:
        """Start a measurement and refresh after the configured delay."""
        delay = self.entry.options.get(
            CONF_MEASURE_DELAY,
            self.entry.data.get(
                CONF_MEASURE_DELAY,
                DEFAULT_MEASURE_DELAY,
            ),
        )

        await self.api.async_start_measurement()
        await asyncio.sleep(delay)
        await self.async_request_refresh()
