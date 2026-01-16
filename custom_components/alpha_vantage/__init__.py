"""The Alpha Vantage integration."""
import asyncio
import logging
from datetime import timedelta

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
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

PLATFORMS = ["sensor", "diagnostics"]

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
        self._last_success = True  # Track status to reduce log noise
        
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
                        # Rate limit notes are warnings
                        _LOGGER.warning("Alpha Vantage API Note: %s", data["Note"])
                    elif "Error Message" in data:
                        msg = data["Error Message"]
                        _LOGGER.error("Alpha Vantage API Error for %s: %s", symbol, msg)
                        # Detect invalid API Key to trigger re-auth flow
                        if "the apikey parameter" in msg.lower():
                             raise ConfigEntryAuthFailed(f"Invalid API Key: {msg}")
                    return None
            except Exception as err:
                if self._last_success:
                    _LOGGER.error("Error communicating with Alpha Vantage: %s", err)
                    self._last_success = False
                else:
                    _LOGGER.debug("Still failing to communicate with Alpha Vantage: %s", err)
                return None

        # Fetch symbols sequentially to respect rate limits
        final_data = {"symbols": {}}
        
        for symbol in self.symbols:
            data = await fetch_symbol_data(symbol)
            if data:
                final_data["symbols"][symbol] = data
            
            # If we have more symbols to fetch, wait a bit to avoid hitting 5 requests/min limit
            # 12 seconds would be perfect for 5/min, but let's try 1 second first 
            # as some users might have premium or the limiter might be less strict for bursts.
            # We will handle the "Note" (rate limit) in fetch_symbol_data.
            if len(self.symbols) > 1 and symbol != self.symbols[-1]:
                await asyncio.sleep(2)  # Small delay between requests

        if not final_data["symbols"]:
            if self._last_success:
                raise UpdateFailed("Failed to fetch any data from Alpha Vantage. Likely rate limited.")
            return {} # Return empty data to suppress further errors
            
        self._last_success = True # Reset on success
        return final_data
