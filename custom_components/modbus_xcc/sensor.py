import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN]["client"]
    device_id = hass.data[DOMAIN]["device_id"]

    if not client.connect():
        _LOGGER.error("Failed to connect to Modbus device")
    else:
        _LOGGER.info("Debug log: Modbus client connected")

    # Získání registru zařízení (nyní synchronně bez await)
    device_registry = async_get_device_registry(hass)

    # Vytvoření zařízení
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, device_id)},
        manufacturer="Your Manufacturer",  # Výrobce zařízení
        model="Your Model",  # Model zařízení
        name="Modbus Device",
        sw_version="1.0",  # Verze software zařízení
        configuration_url=f"http://192.168.7.17"
    )

    # Vytvoření a registrace senzorů
    sensors = [
        VenkovniTeplotaSensor(client, device_id),
        AktualniVykonSensor(client, device_id)
    ]
    
    async_add_entities(sensors, True)

class VenkovniTeplotaSensor(Entity):
    def __init__(self, client, device_id):
        self._client = client
        self._state = None
        self._device_id = device_id

    @property
    def name(self):
        return "venkovni_teplota"

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
        }

    async def async_update(self):
        result = self._client.read_holding_registers(0x0001, 1)
        if result.isError():
            _LOGGER.error("Error reading temperature from Modbus device: %s", result)
        else:
            self._state = result.registers[0] / 100.0  # škálování na 2 desetinná místa

class AktualniVykonSensor(Entity):
    def __init__(self, client, device_id):
        self._client = client
        self._state = None
        self._device_id = device_id

    @property
    def name(self):
        return "aktualni_vykon_systemu"

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
        }

    async def async_update(self):
        result = self._client.read_holding_registers(0x0003, 1)
        if result.isError():
            _LOGGER.error("Error reading power from Modbus device: %s", result)
        else:
            self._state = result.registers[0]  # jednotky v %
