"""Discovery class handle find all device in broker and create devices."""
import logging
from inelsmqtt.const import INELS_ASSUMED_STATE_DEVICES, INELS_COMM_TEST_DICT, INELS_DEVICE_TYPE_DICT

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

        retry = False
        for d in devs:
            if devs[d] is None: #if comes from 'connected'
                d_frags = d.split("/")
                
                dev_type = d_frags[1]
                unique_id = d_frags[2]

                if dev_type in INELS_COMM_TEST_DICT:
                    self.__mqtt.publish("inels/set/" + d, INELS_COMM_TEST_DICT[dev_type])
                    _LOGGER.info("Sending comm test to device of type %s, unique_id %s", dev_type, unique_id)
                    retry = True

        if retry:
            _LOGGER.info("Retrying discovery...")
            devs = self.__mqtt.discovery_all()

        #disregard any devices that don't respond
        sanitized_devs = []
        for k, v in devs.items():
            k_frags = k.split("/")
            dev_type = k_frags[1]
            if v is not None or INELS_DEVICE_TYPE_DICT[dev_type] in INELS_ASSUMED_STATE_DEVICES:
                sanitized_devs.append(k)
        devs = sanitized_devs

        self.__devices = [Device(self.__mqtt, "inels/status/" + item) for item in devs]
        # for item in self.__devices:
        #     if item.parent_id not in self.__coordinators:
        #         self.__coordinators.append(item.parent_id)
        #         self.__coordinators_with_devices[item.parent_id] = []

        #     self.__coordinators_with_devices[item.parent_id].append(item)

        _LOGGER.info("Discovered %s devices", len(self.__devices))

        return self.__devices
