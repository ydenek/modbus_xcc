import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_URL, CONF_PORT, CONF_DEVICE_ID

@config_entries.HANDLERS.register(DOMAIN)
class ModbusTepelkoFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Modbus Tepelko", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_URL): str,
            vol.Required(CONF_PORT): int,
            vol.Required(CONF_DEVICE_ID): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
