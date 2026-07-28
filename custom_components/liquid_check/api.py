"""Local API client for Liquid Check."""

from __future__ import annotations

import asyncio
from typing import Any

from aiohttp import ClientError, ClientSession


class LiquidCheckApiError(Exception):
    """Base exception for Liquid Check API errors."""


class LiquidCheckConnectionError(LiquidCheckApiError):
    """Raised when the device cannot be reached."""


class LiquidCheckInvalidDataError(LiquidCheckApiError):
    """Raised when the device response contains no valid measurement."""


class LiquidCheckApi:
    """Communicate with a Liquid Check device."""

    def __init__(
        self,
        session: ClientSession,
        host: str,
        port: int = 80,
        use_https: bool = False,
        timeout: int = 10,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._host = host.strip().rstrip("/")
        self._port = port
        self._scheme = "https" if use_https else "http"
        self._timeout = timeout

    @property
    def base_url(self) -> str:
        """Return the device base URL."""
        return f"{self._scheme}://{self._host}:{self._port}"

    async def async_get_measurement(self) -> dict[str, float]:
        """Read the current measurement from infos.json."""
        url = f"{self.base_url}/infos.json"

        try:
            async with asyncio.timeout(self._timeout):
                response = await self._session.get(url)
                response.raise_for_status()
                data: dict[str, Any] = await response.json(
                    content_type=None
                )
        except (TimeoutError, ClientError, ValueError) as err:
            raise LiquidCheckConnectionError(
                f"Liquid Check konnte nicht abgefragt werden: {err}"
            ) from err

        measure = data.get("payload", {}).get("measure", {})
        level = measure.get("level")
        content = measure.get("content")

        if level is None or content is None:
            raise LiquidCheckInvalidDataError(
                "Die Antwort enthält weder einen gültigen "
                "Füllstand noch einen Inhalt."
            )

        try:
            return {
                "level": float(level),
                "content": float(content),
            }
        except (TypeError, ValueError) as err:
            raise LiquidCheckInvalidDataError(
                "Die Messwerte sind nicht numerisch."
            ) from err

    async def async_start_measurement(self) -> None:
        """Start a new physical measurement."""
        url = f"{self.base_url}/command"
        payload = {
            "header": {
                "namespace": "Device.Control",
                "name": "StartMeasure",
                "messageId": "1",
                "payloadVersion": "1",
            },
            "payload": None,
        }

        try:
            async with asyncio.timeout(self._timeout):
                response = await self._session.post(
                    url,
                    json=payload,
                    headers={
                        "Content-Type": "application/json; charset=utf-8"
                    },
                )
                response.raise_for_status()
        except (TimeoutError, ClientError) as err:
            raise LiquidCheckConnectionError(
                f"Messung konnte nicht gestartet werden: {err}"
            ) from err
