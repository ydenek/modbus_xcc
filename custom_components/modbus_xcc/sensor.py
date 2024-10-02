import logging
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN]["client"]
    if not client.connect():
        _LOGGER.error("Failed to connect to Modbus device")
    else:
        _LOGGER.info("Debug log: Modbus client connected")
    sensors = [
        VenkovniTeplotaSensor(client),
        AktualniVykonSensor(client)
    ]
    
    async_add_entities(sensors, True)

class VenkovniTeplotaSensor(Entity):
    def __init__(self, client):
        self._client = client
        self._state = None

    @property
    def name(self):
        return "venkovni_teplota"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        result = self._client.read_holding_registers(0x0001,1)
        if result.isError():
            _LOGGER.error("Error reading temperature from Modbus device: %s", result)
        else:
            self._state = result.registers[0] / 100.0  # škálování na 2 desetinná místa

class AktualniVykonSensor(Entity):
    def __init__(self, client):
        self._client = client
        self._state = None

    @property
    def name(self):
        return "aktualni_vykon_systemu"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        result = self._client.read_holding_registers(0x0003, 1)
        if result.isError():
            _LOGGER.error("Error reading temperature from Modbus device: %s", result)
        else:
            self._state = result.registers[0]  # jednotky v %
