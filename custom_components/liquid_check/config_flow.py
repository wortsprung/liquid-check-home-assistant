"""Config flow for Liquid Check."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import (
    LiquidCheckApi,
    LiquidCheckConnectionError,
    LiquidCheckInvalidDataError,
)
from .const import (
    CONF_KEEP_LAST_VALUE,
    CONF_MAX_VOLUME,
    CONF_MEASURE_DELAY,
    CONF_SCAN_INTERVAL,
    CONF_TANK_NAME,
    CONF_TIMEOUT,
    CONF_USE_HTTPS,
    DEFAULT_HOST,
    DEFAULT_KEEP_LAST_VALUE,
    DEFAULT_MAX_VOLUME,
    DEFAULT_MEASURE_DELAY,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TANK_NAME,
    DEFAULT_TIMEOUT,
    DEFAULT_USE_HTTPS,
    DOMAIN,
)


class LiquidCheckConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow for Liquid Check."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the initial setup step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()

            await self.async_set_unique_id(host.lower())
            self._abort_if_unique_id_configured()

            api = LiquidCheckApi(
                session=async_get_clientsession(self.hass),
                host=host,
                port=user_input[CONF_PORT],
                use_https=user_input[CONF_USE_HTTPS],
                timeout=user_input[CONF_TIMEOUT],
            )

            try:
                await api.async_get_measurement()
            except LiquidCheckConnectionError:
                errors["base"] = "cannot_connect"
            except LiquidCheckInvalidDataError:
                errors["base"] = "invalid_data"
            except Exception:
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_NAME,
                    default=DEFAULT_NAME,
                ): str,
                vol.Required(
                    CONF_HOST,
                    default=DEFAULT_HOST,
                ): str,
                vol.Required(
                    CONF_PORT,
                    default=DEFAULT_PORT,
                ): vol.All(int, vol.Range(min=1, max=65535)),
                vol.Required(
                    CONF_USE_HTTPS,
                    default=DEFAULT_USE_HTTPS,
                ): bool,
                vol.Required(
                    CONF_TANK_NAME,
                    default=DEFAULT_TANK_NAME,
                ): str,
                vol.Required(
                    CONF_MAX_VOLUME,
                    default=DEFAULT_MAX_VOLUME,
                ): vol.All(vol.Coerce(float), vol.Range(min=1)),
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=DEFAULT_SCAN_INTERVAL,
                ): vol.All(int, vol.Range(min=5, max=720)),
                vol.Required(
                    CONF_MEASURE_DELAY,
                    default=DEFAULT_MEASURE_DELAY,
                ): vol.All(int, vol.Range(min=1, max=120)),
                vol.Required(
                    CONF_TIMEOUT,
                    default=DEFAULT_TIMEOUT,
                ): vol.All(int, vol.Range(min=1, max=60)),
                vol.Required(
                    CONF_KEEP_LAST_VALUE,
                    default=DEFAULT_KEEP_LAST_VALUE,
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> LiquidCheckOptionsFlow:
        """Return the options flow."""
        return LiquidCheckOptionsFlow()


class LiquidCheckOptionsFlow(config_entries.OptionsFlow):
    """Handle Liquid Check options."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Manage Liquid Check options."""
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input,
            )

        current = {
            **self.config_entry.data,
            **self.config_entry.options,
        }

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_PORT,
                    default=current.get(CONF_PORT, DEFAULT_PORT),
                ): vol.All(int, vol.Range(min=1, max=65535)),
                vol.Required(
                    CONF_USE_HTTPS,
                    default=current.get(
                        CONF_USE_HTTPS,
                        DEFAULT_USE_HTTPS,
                    ),
                ): bool,
                vol.Required(
                    CONF_MAX_VOLUME,
                    default=current.get(
                        CONF_MAX_VOLUME,
                        DEFAULT_MAX_VOLUME,
                    ),
                ): vol.All(vol.Coerce(float), vol.Range(min=1)),
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=current.get(
                        CONF_SCAN_INTERVAL,
                        DEFAULT_SCAN_INTERVAL,
                    ),
                ): vol.All(int, vol.Range(min=5, max=720)),
                vol.Required(
                    CONF_MEASURE_DELAY,
                    default=current.get(
                        CONF_MEASURE_DELAY,
                        DEFAULT_MEASURE_DELAY,
                    ),
                ): vol.All(int, vol.Range(min=1, max=120)),
                vol.Required(
                    CONF_TIMEOUT,
                    default=current.get(
                        CONF_TIMEOUT,
                        DEFAULT_TIMEOUT,
                    ),
                ): vol.All(int, vol.Range(min=1, max=60)),
                vol.Required(
                    CONF_KEEP_LAST_VALUE,
                    default=current.get(
                        CONF_KEEP_LAST_VALUE,
                        DEFAULT_KEEP_LAST_VALUE,
                    ),
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )
