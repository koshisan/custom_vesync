"""VeSync integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pyvesync.vesync import VeSync

from .common import async_process_devices
from .const import (
    DOMAIN,
    SERVICE_UPDATE_DEVS,
    VS_BINARY_SENSORS,
    VS_BUTTON,
    VS_DISCOVERY,
    VS_FANS,
    VS_HUMIDIFIERS,
    VS_LIGHTS,
    VS_MANAGER,
    VS_NUMBERS,
    VS_SENSORS,
    VS_SWITCHES,
)

PLATFORMS: dict[Platform, str] = {
    Platform.SWITCH: VS_SWITCHES,
    Platform.FAN: VS_FANS,
    Platform.LIGHT: VS_LIGHTS,
    Platform.SENSOR: VS_SENSORS,
    Platform.HUMIDIFIER: VS_HUMIDIFIERS,
    Platform.NUMBER: VS_NUMBERS,
    Platform.BINARY_SENSOR: VS_BINARY_SENSORS,
    Platform.BUTTON: VS_BUTTON,
}

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.removed(DOMAIN, raise_if_present=False)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up VeSync as config entry."""
    username = config_entry.data[CONF_USERNAME]
    password = config_entry.data[CONF_PASSWORD]
    time_zone = str(hass.config.time_zone)

    manager = VeSync(username, password, time_zone)
    login = await hass.async_add_executor_job(manager.login)
    if not login:
        _LOGGER.error("Unable to login to the VeSync server")
        return False

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = {VS_MANAGER: manager}

    # Coordinator
    async def async_update_data():
        try:
            await hass.async_add_executor_job(manager.update)
        except Exception as err:
            raise UpdateFailed(f"Update failed: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="vesync",
        update_method=async_update_data,
        update_interval=timedelta(seconds=30),
    )
    await coordinator.async_refresh()
    hass.data[DOMAIN][config_entry.entry_id]["coordinator"] = coordinator

    # Devices erfassen
    device_dict = await async_process_devices(hass, manager)

    platforms_to_setup: list[Platform] = []
    for platform, bucket in PLATFORMS.items():
        hass.data[DOMAIN][config_entry.entry_id][bucket] = []
        if device_dict.get(bucket):
            hass.data[DOMAIN][config_entry.entry_id][bucket].extend(device_dict[bucket])
            platforms_to_setup.append(platform)

    # Neue API: gesammelt und awaited
    if platforms_to_setup:
        await hass.config_entries.async_forward_entry_setups(config_entry, platforms_to_setup)

    # Service: neue Geräte später hinzufügen
    async def async_new_device_discovery(_: ServiceCall) -> None:
        """Discover if new devices should be added."""
        manager_local = hass.data[DOMAIN][config_entry.entry_id][VS_MANAGER]
        dev_dict = await async_process_devices(hass, manager_local)

        async def _add_new_devices(platform: Platform) -> None:
            bucket = PLATFORMS[platform]
            old_devices = hass.data[DOMAIN][config_entry.entry_id][bucket]
            new_devices = list(set(dev_dict.get(bucket, [])) - set(old_devices))
            if not new_devices:
                return

            if old_devices:
                # Plattform aktiv → Entities via Dispatcher hinzufügen
                old_devices.extend(new_devices)
                async_dispatcher_send(hass, VS_DISCOVERY.format(bucket), new_devices)
            else:
                # Plattform noch nicht aktiv → vormerken & Plattform laden
                old_devices.extend(new_devices)
                await hass.config_entries.async_forward_entry_setups(config_entry, [platform])

        for p in PLATFORMS.keys():
            await _add_new_devices(p)

    hass.services.async_register(DOMAIN, SERVICE_UPDATE_DEVS, async_new_device_discovery)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, list(PLATFORMS.keys()))
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
