"""Support for VeSync button."""
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pyvesync.vesynckitchen import model_features as kitchen_model_features

from .common import VeSyncBaseEntity
from .const import DOMAIN, VS_AIRFRYER_TYPES, VS_BUTTON, VS_DISCOVERY

_LOGGER = logging.getLogger(__name__)


SENSOR_TYPES_CAF = {
    "Chicken": {
        "cookSetTime": 1200,
        "cookTemp": 200,
        "mode": "Chicken",
        "shakeTime": 0,
        "tempUnit": "c",
        "allowModified": True,
        "icon": "mdi:food-drumstick",
        "recipeId": 2,
    },
    "Steak": {
        "cookSetTime": 480,
        "cookTemp": 205,
        "mode": "Steak",
        "shakeTime": 0,
        "tempUnit": "c",
        "allowModified": True,
        "icon": "mdi:food-steak",
        "recipeId": 1,
    },
    "Seafood": {
        "cookSetTime": 480,
        "cookTemp": 190,
        "mode": "Seafood",
        "shakeTime": 0,
        "tempUnit": "c",
        "allowModified": True,
        "icon": "mdi:fish",
        "recipeId": 3,
    },
    "Veggies": {
        "cookSetTime": 360,
        "cookTemp": 195,
        "mode": "Veggies",
        "shakeTime": 0,
        "tempUnit": "c",
        "allowModified": True,
        "icon": "mdi:carrot",
        "recipeId": 15,
    },
    "French fries": {
        "cookSetTime": 1200,
        "cookTemp": 195,
        "mode": "French fries",
        "shakeTime": 0,
        "tempUnit": "c",
        "allowModified": True,
        "icon": "mdi:french-fries",
        "recipeId": 6,
    },
    "Frozen": {
        "cookSetTime": 720,
        "cookTemp": 200,
        "mode": "Frozen",
        "shakeTime": 0,
        "tempUnit": "c",
        "allowModified": True,
        "icon": "mdi:snowflake",
        "recipeId": 5,
    },
    "AirFry": {
        "cookSetTime": 600,
        "cookTemp": 180,
        "mode": "AirFry",
        "shakeTime": 0,
        "tempUnit": "c",
        "allowModified": True,
        "icon": "mdi:fan",
        "recipeId": 14,
    },
    "Reheat": {
        "cookSetTime": 300,
        "cookTemp": 175,
        "mode": "Reheat",
        "shakeTime": 0,
        "tempUnit": "c",
        "allowModified": True,
        "icon": "",
        "recipeId": 16,
    },
    "Roast": {
        "cookSetTime": 600,
        "cookTemp": 205,
        "mode": "Roast",
        "shakeTime": 0,
        "tempUnit": "c",
        "allowModified": True,
        "icon": "",
        "recipeId": 13,
    },
    "Bake": {
        "cookSetTime": 1200,
        "cookTemp": 160,
        "mode": "Bake",
        "shakeTime": 0,
        "tempUnit": "c",
        "allowModified": True,
        "icon": "mdi:baguette",
        "recipeId": 9,
    },
    "Broil": {
        "cookSetTime": 600,
        "cookTemp": 205,
        "mode": "Broil",
        "shakeTime": 0,
        "tempUnit": "c",
        "allowModified": True,
        "icon": "",
        "recipeId": 17,
    },
    "end": {
        "mode": "end",
        "name": "End cooking or preheating",
        "icon": "mdi:stop",
    },
    "update": {
        "mode": "update",
        "name": "Force Update",
        "icon": "mdi:update",
    },
    "startCook": {
        "mode": "startCook",
        "name": "Start Cook",
        "icon": "mdi:play",
    },
}

SENSOR_TYPES_CS158 = {
    # unique_id,name # icon,
    "end": {
        "mode": "end",
        "name": "End cooking or preheating",
        "icon": "mdi:stop",
    },
    "pause": {
        "mode": "pause",
        "name": "Pause air fryer when in cooking or heating",
        "icon": "mdi:pause",
    },
    "resume": {
        "mode": "resume",
        "name": "Resume air fryer when in cookStop or preheatStop",
        "icon": "mdi:play",
    },
    "update": {
        "mode": "update",
        "name": "Force Update",
        "icon": "mdi:update",
    },
    "startCook": {
        "mode": "startCook",
        "name": "Start Cook",
        "icon": "mdi:play",
    },
}


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
            if kitchen_model_features(dev.device_type)["module"] == "VeSyncAirFryerCAF":
                for stype in SENSOR_TYPES_CAF.values():
                    entities.append(
                        VeSyncairfryerButton(
                            dev,
                            coordinator,
                            stype,
                        )
                    )
            else:
                for stype in SENSOR_TYPES_CS158.values():
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
                self.airfryer.cookv2(
                    self.stype["cookTemp"],
                    self.stype["cookSetTime"],
                    self.stype["mode"],
                )
