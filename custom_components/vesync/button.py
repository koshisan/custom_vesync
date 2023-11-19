"""Support for VeSync button."""
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pyvesync.vesynckitchen import model_features as kitchen_model_features

from .common import VeSyncBaseEntity
from .const import BTN_TYPES, DOMAIN, VS_AIRFRYER_TYPES, VS_BUTTON, VS_DISCOVERY

_LOGGER = logging.getLogger(__name__)


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
        async_dispatcher_connect(hass, VS_DISCOVERY.format(VS_BUTTON), discover)
    )

    _setup_entities(
        hass.data[DOMAIN][config_entry.entry_id][VS_BUTTON],
        async_add_entities,
        coordinator,
    )


@callback
def _setup_entities(devices, async_add_entities, coordinator):
    """Check if device is online and add entity."""
    entities = []
    for dev in devices:
        if kitchen_model_features(dev.device_type)["module"] in VS_AIRFRYER_TYPES:

            for stype in BTN_TYPES.values():
                if (stype["mode"] == "pause") | (stype["mode"] == "resume"):
                    if (
                        kitchen_model_features(dev.device_type)["module"]
                        != "VeSyncAirFryerCAF"
                    ):
                        entities.append(
                            VeSyncairfryerButton(
                                dev,
                                coordinator,
                                stype,
                            )
                        )
                else:
                    entities.append(
                        VeSyncairfryerButton(
                            dev,
                            coordinator,
                            stype,
                        )
                    )
    async_add_entities(entities, update_before_add=True)


class VeSyncairfryerButton(VeSyncBaseEntity, ButtonEntity):
    """Base class for VeSync switch Device Representations."""

    def __init__(self, airfryer, coordinator, stype) -> None:
        """Initialize the VeSync humidifier device."""
        super().__init__(airfryer, coordinator)
        self.airfryer = airfryer
        self.stype = stype

    @property
    def unique_id(self):
        """Return unique ID for water tank lifted sensor on device."""
        return f"{super().unique_id}-" + self.stype["mode"]

    @property
    def name(self):
        """Return sensor name."""
        return self.stype["mode"]

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self.stype["icon"]

    def press(self) -> None:
        """Return True if device is on."""
        if self.stype["mode"] == "end":
            self.airfryer.end()
        elif self.stype["mode"] == "pause":
            self.airfryer.pause()
        elif self.stype["mode"] == "resume":
            self.airfryer.resume()
        elif self.stype["mode"] == "update":
            self.airfryer.update()
        else:
            if (
                kitchen_model_features(self.airfryer.device_type)["module"]
                == "VeSyncAirFryerCAF"
            ):
                self.airfryer.cookv2()

