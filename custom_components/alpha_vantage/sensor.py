"""Sensor platform for Alpha Vantage integration."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES, CONF_SHOW_SENSORS, DEFAULT_SENSORS

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Alpha Vantage sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    symbols = coordinator.symbols
    # Get enabled sensors from options or fallback to default
    enabled_sensors = entry.options.get(CONF_SHOW_SENSORS, entry.data.get(CONF_SHOW_SENSORS, DEFAULT_SENSORS))
    
    entities = []
    
    # Add symbol-based sensors
    for symbol in symbols:
        for sensor_type in enabled_sensors:
            if sensor_type in SENSOR_TYPES and SENSOR_TYPES[sensor_type]["category"] == "symbol":
                entities.append(AlphaVantageSensor(coordinator, symbol, sensor_type))
    
    async_add_entities(entities)

class AlphaVantageSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Alpha Vantage sensor."""

    def __init__(self, coordinator, symbol, sensor_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._symbol = symbol.upper()
        self._sensor_type = sensor_type
        self._sensor_info = SENSOR_TYPES[sensor_type]
        
        self._attr_name = f"{self._symbol} {self._sensor_info['name']}"
        self._attr_unique_id = f"{DOMAIN}_{self._symbol}_{sensor_type}"
        self._attr_translation_key = sensor_type
            
        self._entry_id = coordinator.config_entry.entry_id
        
        # Set attributes from sensor_info
        self._attr_icon = self._sensor_info.get("icon")
        self._attr_device_class = self._sensor_info.get("device_class")
        self._attr_state_class = self._sensor_info.get("state_class")
        self._attr_native_unit_of_measurement = self._sensor_info.get("unit")

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name="Alpha Vantage",
            manufacturer="Alpha Vantage",
            entry_type="service",
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        data = self.coordinator.data.get('symbols', {}).get(self._symbol)
        
        if data:
            value = data
            for key in self._sensor_info["json_path"]:
                if isinstance(value, dict):
                    value = value.get(key)
                else:
                    return None
                    
                if value is None:
                    return None
            
            # Formatting
            if isinstance(value, str) and value.endswith('%'):
                value = value.replace('%', '')
                
            try:
                num_value = float(value)
                return round(num_value, self.coordinator.decimals)
            except (ValueError, TypeError):
                return value
            
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data.get('symbols', {}).get(self._symbol)
        if data:
            return {
                "last_refreshed": data.get('07. latest trading day'),
                "symbol": self._symbol,
            }
        return None
