"""Diagnostics support for Alpha Vantage."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.diagnostics import redact_datafield

from .const import DOMAIN, CONF_API_KEY

TO_REDACT = {CONF_API_KEY}

async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    diagnostics_data = {
        "entry": redact_datafield(entry.as_dict(), TO_REDACT),
        "data": coordinator.data,
    }

    return diagnostics_data
