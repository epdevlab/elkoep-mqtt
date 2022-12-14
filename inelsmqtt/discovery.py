"""Discovery class handle find all device in broker and create devices."""
import logging

from inelsmqtt import InelsMqtt
from inelsmqtt.devices import Device


_LOGGER = logging.getLogger(__name__)


class InelsDiscovery(object):
    """Handling discovery mqtt topics from broker."""

    def __init__(self, mqtt: InelsMqtt) -> None:
        """Initialize inels mqtt discovery"""
        self.__mqtt = mqtt
        self.__devices: list[Device] = []
        self.__coordinators: list[str] = []
        self.__coordinators_with_devices: dict[str, list[Device]] = {}

    @property
    def coordinators(self) -> list[str]:
        """Coordinators list

        Returns:
            _type_: list of coordinator serial numbers
        """
        return self.__coordinators

    @property
    def devices(self) -> list[Device]:
        """List of devices

        Returns:
            list[Device]: all devices handled with discovery object
        """
        return self.__devices

    def discovery(self) -> dict[str, list[Device]]:
        """Discover and create device list

        Returns:
            list[Device]: List of Device object
        """
        devs = self.__mqtt.discovery_all()
        self.__devices = [Device(self.__mqtt, item) for item in devs]

        for item in self.__devices:
            if item.parent_id not in self.__coordinators:
                self.__coordinators.append(item.parent_id)
                self.__coordinators_with_devices[item.parent_id] = []

            self.__coordinators_with_devices[item.parent_id].append(item)

        _LOGGER.info("Discovered %s devices", len(self.__devices))

        return self.__devices
