"""Constants for VeSync Component."""

from homeassistant.const import DEVICE_CLASS_TEMPERATURE, TEMP_CELSIUS, TIME_MINUTES

DOMAIN = "vesync"
VS_DISCOVERY = "vesync_discovery_{}"
SERVICE_UPDATE_DEVS = "update_devices"


VS_BUTTON = "button"
VS_SWITCHES = "switches"
VS_FAN = "fan"
VS_FANS = "fans"
VS_LIGHTS = "lights"
VS_SENSORS = "sensors"
VS_HUMIDIFIERS = "humidifiers"
VS_NUMBERS = "numbers"
VS_BINARY_SENSORS = "binary_sensors"
VS_MANAGER = "manager"
VS_SELECT = "select"

VS_LEVELS = "levels"
VS_MODES = "modes"

VS_MODE_AUTO = "auto"
VS_MODE_HUMIDITY = "humidity"
VS_MODE_MANUAL = "manual"
VS_MODE_SLEEP = "sleep"

VS_TO_HA_ATTRIBUTES = {"humidity": "current_humidity"}

VS_FAN_TYPES = ["VeSyncAirBypass", "VeSyncAir131", "VeSyncVital"]
VS_HUMIDIFIERS_TYPES = ["VeSyncHumid200300S", "VeSyncHumid200S", "VeSyncHumid1000S"]
VS_AIRFRYER_TYPES = ["VeSyncAirFryer158", "VeSyncAirFryerCAF"]


DEV_TYPE_TO_HA = {
    "ESL100": "bulb-dimmable",
    "ESL100CW": "bulb-tunable-white",
    "ESO15-TB": "outlet",
    "ESW03-USA": "outlet",
    "ESW01-EU": "outlet",
    "ESW15-USA": "outlet",
    "wifi-switch-1.3": "outlet",
    "ESWL01": "switch",
    "ESWL03": "switch",
    "ESD16": "walldimmer",
    "ESWD16": "walldimmer",
}


BINARY_SENSOR_TYPES_AIRFRYER = {
    # unique_id,name # icon, #attribute read,
    "is_heating": [
        "is_heating",
        "preheating",
        "mdi:pot-steam-outline",
    ],
    "is_cooking": [
        "is_cooking",
        "cooking",
        "mdi:rice",
    ],
    "is_running": [
        "is_running",
        "running",
        "mdi:pause",
    ],
}

NUMBER_TYPES_AIRFRYER = {
    # unique_id,name # icon, #attribute read,
    "cook_temp": [
        "cook_temp",
        "cook temperature",
        "mdi:pot-steam-outline",
    ],
    "cook_time": [
        "cook_time",
        "cook time",
        "mdi:rice",
    ],
}

SENSOR_TYPES_AIRFRYER = {
    # unique_id ,#name ,# unit of measurement,# icon, # device class, #attribute read,
    "current_temp": [
        "current_temperature",
        "Current temperature",
        TEMP_CELSIUS,
        None,
        DEVICE_CLASS_TEMPERATURE,
        "current_temp",
    ],
    "cook_set_temp": [
        "set_temperature",
        "Set temperature",
        TEMP_CELSIUS,
        None,
        DEVICE_CLASS_TEMPERATURE,
        "cook_set_temp",
    ],
    "cook_last_time": [
        "cook_last_time",
        "Cook Remaining",
        TIME_MINUTES,
        "mdi:timer",
        TIME_MINUTES,
        "cook_last_time",
    ],
    "preheat_last_time": [
        "preheat_last_time",
        "Preheat Remaining",
        TIME_MINUTES,
        "mdi:timer",
        TIME_MINUTES,
        "preheat_last_time",
    ],
    "cook_status": [
        "cook_status",
        "Cook Status",
        None,
        "mdi:rotate-3d-variant",
        None,
        "cook_status",
    ],
    # "remaining_time": [
    #    "remaining_time",
    #    "running:",
    #    TIME_MINUTES,
    #    "mdi:timer",
    #    TIME_MINUTES,
    #    "remaining_time",
    # ],
}


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
}

BTN_TYPES = {
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