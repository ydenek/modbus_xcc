from pymodbus.client import ModbusTcpClient
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_URL, CONF_PORT, CONF_DEVICE_ID

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Připojení k Modbus zařízení
    url = entry.data[CONF_URL]
    port = entry.data[CONF_PORT]
    client = ModbusTcpClient(url, port=port)
    
    hass.data[DOMAIN] = {
        "client": client,
        "device_id": entry.data[CONF_DEVICE_ID]
    }

    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "sensor"))

    return True
