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
        "unit": "$",
        "icon": "mdi:cash",
        "category": "symbol"
    },
    "change": {
        "name": "Change",
        "json_path": ["09. change"],
        "unit": "$",
        "icon": "mdi:chart-line-variant",
        "category": "symbol"
    },
    "change_percent": {
        "name": "Change Percent",
        "json_path": ["10. change percent"],
        "unit": "%",
        "icon": "mdi:chart-line",
        "category": "symbol"
    },
    "volume": {
        "name": "Volume",
        "json_path": ["06. volume"],
        "unit": None,
        "icon": "mdi:chart-bar",
        "category": "symbol"
    },
    "high": {
        "name": "Day High",
        "json_path": ["03. high"],
        "unit": "$",
        "icon": "mdi:arrow-up-bold",
        "category": "symbol"
    },
    "low": {
        "name": "Day Low",
        "json_path": ["04. low"],
        "unit": "$",
        "icon": "mdi:arrow-down-bold",
        "category": "symbol"
    },
    "previous_close": {
        "name": "Previous Close",
        "json_path": ["08. previous close"],
        "unit": "$",
        "icon": "mdi:history",
        "category": "symbol"
    },
}
