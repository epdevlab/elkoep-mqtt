"""Discovery class handle find all device in broker and create devices."""

import logging

from inelsmqtt import InelsMqtt
from inelsmqtt.const import GATEWAY
from inelsmqtt.devices import Device
from inelsmqtt.utils.core import INELS_ASSUMED_STATE_DEVICES, ProtocolHandlerMapper

_LOGGER = logging.getLogger(__name__)


class InelsDiscovery(object):
    """Handling discovery mqtt topics from broker."""

    def __init__(self, mqtt: InelsMqtt) -> None:
        """Initialize inels mqtt discovery"""
        self.__mqtt = mqtt
        self.__devices: list[Device] = []

    @property
    def devices(self) -> list[Device]:
        """List of devices

        Returns:
            list[Device]: all devices handled with discovery object
        """
        return self.__devices

    def discovery(self) -> list[Device]:
        """Discover and create device list

        Returns:
            list[Device]: List of Device object
        """
        devs = self.__mqtt.discovery_all()

        gateways_topics = []

        retry = False
        for d in devs:
            if devs[d] is None:  # if comes from 'connected'
                d_frags = d.split("/")

                dev_type = d_frags[1]
                unique_id = d_frags[2]

                handler = ProtocolHandlerMapper.get_handler(dev_type)
                command = getattr(handler, "COMM_TEST", lambda: None)()
                if command:
                    self.__mqtt.publish("inels/set/" + d, command)
                    _LOGGER.info("Sending comm test to device of type %s, unique_id %s", dev_type, unique_id)
                    retry = True
            elif devs[d] == GATEWAY:
                gateways_topics.append(d)

        if retry:
            _LOGGER.info("Retrying discovery...")
            devs = self.__mqtt.discovery_all()

        # Remove gateways from devs
        devs = {k: v for k, v in devs.items() if k not in gateways_topics}

        # disregard any devices that don't respond
        sanitized_devs: list[str] = []
        for k, v in devs.items():
            k_frags = k.split("/")
            dev_type = k_frags[1]
            if v is not None or ProtocolHandlerMapper.get_handler(dev_type) in INELS_ASSUMED_STATE_DEVICES:
                sanitized_devs.append(k)

        self.__devices = [Device(self.__mqtt, "inels/status/" + item) for item in sanitized_devs]

        connected_topics = [device.connected_topic for device in self.__devices]
        state_topic = [device.state_topic for device in self.__devices]
        all_topics = connected_topics + state_topic + gateways_topics

        # Subscribe to all topics with QoS 0
        self.__mqtt.subscribe(all_topics, qos=0)

        _LOGGER.info("Discovered %s devices", len(self.__devices))
        _LOGGER.info("Discovered %s gateways", len(gateways_topics))

        return self.__devices
