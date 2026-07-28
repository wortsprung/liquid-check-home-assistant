"""Liquid Check integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import LiquidCheckApi
from .const import (
    CONF_HOST,
    CONF_MAX_VOLUME,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_TIMEOUT,
    CONF_USE_HTTPS,
    DEFAULT_MAX_VOLUME,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
    DEFAULT_USE_HTTPS,
    DOMAIN,
    PLATFORMS,
    SERVICE_MEASURE,
    SERVICE_REFRESH,
)
from .coordinator import LiquidCheckCoordinator


type LiquidCheckConfigEntry = ConfigEntry[LiquidCheckCoordinator]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: LiquidCheckConfigEntry,
) -> bool:
    """Set up Liquid Check from a config entry."""
    session = async_get_clientsession(hass)

    api = LiquidCheckApi(
        session=session,
        host=entry.data[CONF_HOST],
        port=entry.options.get(
            CONF_PORT,
            entry.data.get(CONF_PORT, DEFAULT_PORT),
        ),
        use_https=entry.options.get(
            CONF_USE_HTTPS,
            entry.data.get(CONF_USE_HTTPS, DEFAULT_USE_HTTPS),
        ),
        timeout=entry.options.get(
            CONF_TIMEOUT,
            entry.data.get(CONF_TIMEOUT, DEFAULT_TIMEOUT),
        ),
    )

    scan_interval = entry.options.get(
        CONF_SCAN_INTERVAL,
        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    )
    max_volume = entry.options.get(
        CONF_MAX_VOLUME,
        entry.data.get(CONF_MAX_VOLUME, DEFAULT_MAX_VOLUME),
    )

    coordinator = LiquidCheckCoordinator(
        hass=hass,
        entry=entry,
        api=api,
        update_interval=timedelta(minutes=scan_interval),
        max_volume=max_volume,
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    async def async_refresh_service(call) -> None:
        """Refresh Liquid Check data."""
        await coordinator.async_request_refresh()

    async def async_measure_service(call) -> None:
        """Start a new Liquid Check measurement."""
        await coordinator.async_measure()

    if not hass.services.has_service(DOMAIN, SERVICE_REFRESH):
        hass.services.async_register(
            DOMAIN,
            SERVICE_REFRESH,
            async_refresh_service,
        )

    if not hass.services.has_service(DOMAIN, SERVICE_MEASURE):
        hass.services.async_register(
            DOMAIN,
            SERVICE_MEASURE,
            async_measure_service,
        )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: LiquidCheckConfigEntry,
) -> bool:
    """Unload a Liquid Check config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.services.async_remove(DOMAIN, SERVICE_REFRESH)
        hass.services.async_remove(DOMAIN, SERVICE_MEASURE)

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: LiquidCheckConfigEntry,
) -> None:
    """Reload Liquid Check after options change."""
    await hass.config_entries.async_reload(entry.entry_id)
