"""The Alpha Vantage integration."""
import asyncio
import logging
from datetime import timedelta

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN, 
    CONF_API_KEY, 
    CONF_SYMBOLS, 
    CONF_SCAN_INTERVAL, 
    CONF_DECIMALS, 
    API_URL, 
    DEFAULT_SCAN_INTERVAL, 
    DEFAULT_DECIMALS
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Alpha Vantage from a config entry."""
    session = async_get_clientsession(hass)
    
    # Use options if available, otherwise fallback to data
    api_key = entry.options.get(CONF_API_KEY, entry.data[CONF_API_KEY])
    symbols = entry.options.get(CONF_SYMBOLS, entry.data[CONF_SYMBOLS])
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
    decimals = entry.options.get(CONF_DECIMALS, entry.data.get(CONF_DECIMALS, DEFAULT_DECIMALS))

    coordinator = AlphaVantageDataUpdateCoordinator(
        hass,
        session,
        api_key=api_key,
        symbols=symbols,
        scan_interval=scan_interval,
        decimals=decimals,
        config_entry=entry
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Register update listener
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)

class AlphaVantageDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Alpha Vantage data."""

    def __init__(self, hass, session, api_key, symbols, scan_interval, decimals, config_entry):
        """Initialize the coordinator."""
        self.session = session
        self.api_key = api_key
        self.symbols = [s.strip().upper() for s in symbols.split(",")]
        self.decimals = decimals
        self.config_entry = config_entry
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        
        async def fetch_symbol_data(symbol):
            """Fetch data for a single symbol."""
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.api_key
            }
            try:
                async with self.session.get(API_URL, params=params, timeout=10) as response:
                    if response.status != 200:
                        _LOGGER.error("Error fetching %s: %s", symbol, response.status)
                        return None
                    data = await response.json()
                    if "Global Quote" in data:
                        return data["Global Quote"]
                    elif "Note" in data:
                        _LOGGER.warning("Alpha Vantage API Note: %s", data["Note"])
                    elif "Error Message" in data:
                        _LOGGER.error("Alpha Vantage API Error for %s: %s", symbol, data["Error Message"])
                    return None
            except Exception as err:
                _LOGGER.error("Exception fetching %s: %s", symbol, err)
                return None

        # Execute all fetches in parallel
        # Note: Alpha Vantage free tier has a limit of 5 requests per minute.
        # We might need to handle rate limiting here if many symbols are configured.
        results = await asyncio.gather(
            *[fetch_symbol_data(symbol) for symbol in self.symbols],
            return_exceptions=True
        )

        final_data = {"symbols": {}}
        
        for i, symbol in enumerate(self.symbols):
            if isinstance(results[i], dict) and results[i]:
                final_data["symbols"][symbol] = results[i]

        if not final_data["symbols"]:
            raise UpdateFailed("Failed to fetch any data from Alpha Vantage")
            
        return final_data
