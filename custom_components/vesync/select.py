"""Support for VeSync select."""
import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pyvesync.vesynckitchen import model_features as kitchen_model_features


from .common import VeSyncBaseEntity
from .const import DOMAIN, SENSOR_TYPES_CAF, VS_AIRFRYER_TYPES, VS_DISCOVERY, VS_SELECT

_LOGGER = logging.getLogger(__name__)


def get_auto_generate_data_points() -> list:
    """Get Options."""
    dps = []
    for stype in SENSOR_TYPES_CAF.values():
        dps.append(stype["mode"])

    return dps


def get_values(amode, avalue) -> int:
    """Get Values."""
    bvalue = ""
    for stype in SENSOR_TYPES_CAF.values():
        if (stype["mode"]) == amode:
            bvalue = stype[avalue]
            break
    return bvalue


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switches."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    @callback
    def discover(devices):
        """Add new devices to platform."""
        _setup_entities(devices, async_add_entities, coordinator)

    config_entry.async_on_unload(
        async_dispatcher_connect(hass, VS_DISCOVERY.format(VS_SELECT), discover)
    )

    _setup_entities(
        hass.data[DOMAIN][config_entry.entry_id][VS_SELECT],
        async_add_entities,
        coordinator,
    )


@callback
def _setup_entities(devices, async_add_entities, coordinator):
    """Check if device is online and add entity."""
    entities = []
    for dev in devices:
        if kitchen_model_features(dev.device_type)["module"] in VS_AIRFRYER_TYPES:
            if kitchen_model_features(dev.device_type)["module"] == "VeSyncAirFryerCAF":
                entities.append(
                    VeSyncairfryerSelectMenu(
                        dev,
                        coordinator,
                    )
                )

    async_add_entities(entities, update_before_add=True)


class VeSyncairfryerSelectMenu(VeSyncBaseEntity, SelectEntity):
    """Base class for VeSync switch Device Representations."""

    def __init__(self, airfryer, coordinator) -> None:
        """Initialize the VeSync humidifier device."""
        super().__init__(airfryer, coordinator)
        self.airfryer = airfryer
        self._name = "KITCHEN MENU"
        self._state = self.airfryer.recipename
        self._options = get_auto_generate_data_points()

    @property
    def should_poll(self):
        """Return the polling state."""
        return True

    @property
    def name(self):
        """Return the name."""
        return self._name

    @property
    def options(self):
        """Return the options."""
        return self._options

    @property
    def current_option(self):
        """Return current option."""
        return self._state
    
    def select_option(self, option):
        """Sekect option."""
        self._state = option
        self.airfryer.set_kitchen_mode(option)
        self.airfryer.set_cook_temp(get_values(option,"cookTemp"))
        self.airfryer.set_cook_time(get_values(option,"cookSetTime"))
        self.schedule_update_ha_state(True)
