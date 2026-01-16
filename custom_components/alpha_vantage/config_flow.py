"""Config flow for Alpha Vantage integration."""
import logging
import voluptuous as vol
import aiohttp

from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN, 
    CONF_API_KEY, 
    CONF_SYMBOLS, 
    CONF_SCAN_INTERVAL, 
    CONF_DECIMALS, 
    CONF_SHOW_SENSORS,
    API_URL, 
    DEFAULT_SCAN_INTERVAL, 
    DEFAULT_DECIMALS,
    DEFAULT_SENSORS,
    SENSOR_TYPES
)

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_KEY): str,
    vol.Required(CONF_SYMBOLS, default="AAPL"): str,
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(cv.positive_int, vol.Range(min=60)),
    vol.Optional(CONF_DECIMALS, default=DEFAULT_DECIMALS): vol.All(cv.positive_int, vol.Range(min=0)),
    vol.Optional(CONF_SHOW_SENSORS, default=DEFAULT_SENSORS): cv.multi_select(
        {k: v["name"] for k, v in SENSOR_TYPES.items()}
    ),
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Alpha Vantage."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Validate the API key
            valid = await self._test_api_key(user_input[CONF_API_KEY])
            if valid:
                return self.async_create_entry(title="Alpha Vantage", data=user_input)
            else:
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    async def async_step_reauth(self, user_input=None):
        """Handle re-authentication."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        """Handle re-authentication confirmation."""
        errors = {}
        if user_input is not None:
            valid = await self._test_api_key(user_input[CONF_API_KEY])
            if valid:
                entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
                self.hass.config_entries.async_update_entry(
                    entry, data={**entry.data, CONF_API_KEY: user_input[CONF_API_KEY]}
                )
                await self.hass.config_entries.async_reload(entry.entry_id)
                return self.async_abort(reason="reauth_successful")
            else:
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str,
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def _test_api_key(self, api_key):
        """Test if the API key is valid."""
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": "AAPL",
            "apikey": api_key
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(API_URL, params=params) as response:
                    if response.status != 200:
                        return False
                    data = await response.json()
                    # If it's a Note (rate limit) or a Global Quote, the key is valid structure-wise
                    # If it has an Error Message about API Key, it's invalid
                    if "Error Message" in data and "the apikey parameter" in data["Error Message"].lower():
                        return False
                    return True
            except Exception:
                return False

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Alpha Vantage."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_API_KEY,
                    default=self._config_entry.options.get(
                        CONF_API_KEY, 
                        self._config_entry.data.get(CONF_API_KEY)
                    ),
                ): str,
                vol.Required(
                    CONF_SYMBOLS,
                    default=self._config_entry.options.get(
                        CONF_SYMBOLS, 
                        self._config_entry.data.get(CONF_SYMBOLS, "AAPL,MSFT")
                    ),
                ): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=self._config_entry.options.get(
                        CONF_SCAN_INTERVAL, 
                        self._config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                    ),
                ): vol.All(cv.positive_int, vol.Range(min=60)),
                vol.Optional(
                    CONF_DECIMALS,
                    default=self._config_entry.options.get(
                        CONF_DECIMALS, 
                        self._config_entry.data.get(CONF_DECIMALS, DEFAULT_DECIMALS)
                    ),
                ): vol.All(cv.positive_int, vol.Range(min=0)),
                vol.Optional(
                    CONF_SHOW_SENSORS,
                    default=self._config_entry.options.get(
                        CONF_SHOW_SENSORS, 
                        self._config_entry.data.get(CONF_SHOW_SENSORS, DEFAULT_SENSORS)
                    ),
                ): cv.multi_select({k: v["name"] for k, v in SENSOR_TYPES.items()}),
            }),
        )
