"""Constants for the Alpha Vantage integration."""

DOMAIN = "alpha_vantage"

CONF_API_KEY = "api_key"
CONF_SYMBOLS = "symbols"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_DECIMALS = "decimals"
CONF_SHOW_SENSORS = "show_sensors"

DEFAULT_SCAN_INTERVAL = 3600  # 1 hour (to stay within 25 req/day limit)
DEFAULT_DECIMALS = 2
DEFAULT_SENSORS = ["price", "change", "change_percent"]

# API Endpoints
# Alpha Vantage uses a single endpoint with different 'function' parameters
API_URL = "https://www.alphavantage.co/query"

SENSOR_TYPES = {
    "price": {
        "name": "Price",
        "json_path": ["05. price"],
        "unit": None,  # Will be set in sensor.py if needed
        "icon": "mdi:currency-usd",
        "category": "symbol",
        "device_class": "monetary",
        "state_class": "measurement",
    },
    "change": {
        "name": "Change",
        "json_path": ["09. change"],
        "unit": None,
        "icon": "mdi:trending-up",
        "category": "symbol",
        "state_class": "measurement",
    },
    "change_percent": {
        "name": "Change Percent",
        "json_path": ["10. change percent"],
        "unit": "%",
        "icon": "mdi:percent",
        "category": "symbol",
        "state_class": "measurement",
    },
    "volume": {
        "name": "Volume",
        "json_path": ["06. volume"],
        "unit": None,
        "icon": "mdi:chart-bar",
        "category": "symbol",
        "state_class": "measurement",
    },
    "high": {
        "name": "High",
        "json_path": ["03. high"],
        "unit": None,
        "icon": "mdi:arrow-up-bold",
        "category": "symbol",
        "device_class": "monetary",
        "state_class": "measurement",
    },
    "low": {
        "name": "Low",
        "json_path": ["04. low"],
        "unit": None,
        "icon": "mdi:arrow-down-bold",
        "category": "symbol",
        "device_class": "monetary",
        "state_class": "measurement",
    },
    "previous_close": {
        "name": "Previous Close",
        "json_path": ["08. previous close"],
        "unit": None,
        "icon": "mdi:history",
        "category": "symbol",
        "device_class": "monetary",
        "state_class": "measurement",
    },
}
