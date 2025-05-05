"""Class handle base info about device."""

import json
import logging
from typing import Any, Callable, Optional, Union

from inelsmqtt import InelsMqtt
from inelsmqtt.const import (
    BUTTON,
    DEVICE_CONNECTED,
    FRAGMENT_DEVICE_TYPE,
    FRAGMENT_DOMAIN,
    FRAGMENT_SERIAL_NUMBER,
    FRAGMENT_UNIQUE_ID,
    GW_CONNECTED,
    MANUFACTURER,
    SENSOR,
    TOPIC_FRAGMENTS,
    VERSION,
)
from inelsmqtt.utils.core import (
    DUMMY_VAL,
    DeviceClassProtocol,
    DeviceTypeNotFound,
    DeviceValue,
    LastHAValue,
    ProtocolHandlerMapper,
)

_LOGGER = logging.getLogger(__name__)


class Device(object):
    """Carry basic device stuff

    Args:
        object (_type_): default object it is new style of python class coding
    """

    def __init__(
        self,
        mqtt: InelsMqtt,
        state_topic: str,
        title: Optional[str] = None,
    ) -> None:
        """Initialize instance of device

        Args:
            mqtt (InelsMqtt): instance of mqtt broker
            status_topic (str): String format of status topic
            set_topic (str): Sring format of set topic
            title (str, optional): Formal name of the device. When None
            then will be same as unique_id. Defaults to None.
        """
        fragments = state_topic.split("/")

        self.__mqtt = mqtt

        try:
            self.__device_class: type[DeviceClassProtocol] = ProtocolHandlerMapper.get_handler(
                fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]
            )
        except DeviceTypeNotFound as e:
            _LOGGER.error("Failed to get device class: %s", e)
            raise

        self.__device_type = self.__device_class.HA_TYPE
        self.__inels_type = self.__device_class.INELS_TYPE

        self.__unique_id = f"{fragments[TOPIC_FRAGMENTS[FRAGMENT_SERIAL_NUMBER]]}_{fragments[TOPIC_FRAGMENTS[FRAGMENT_UNIQUE_ID]]}"  # fragments[TOPIC_FRAGMENTS[FRAGMENT_UNIQUE_ID]]
        self.__parent_id = self.__unique_id  # fragments[TOPIC_FRAGMENTS[FRAGMENT_SERIAL_NUMBER]]
        self.__state_topic = state_topic
        self.__set_topic = None

        if self.__device_type is not SENSOR and self.__device_type is not BUTTON:
            self.__set_topic = f"{fragments[TOPIC_FRAGMENTS[FRAGMENT_DOMAIN]]}/set/{fragments[TOPIC_FRAGMENTS[FRAGMENT_SERIAL_NUMBER]]}/{fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]}/{fragments[TOPIC_FRAGMENTS[FRAGMENT_UNIQUE_ID]]}"  # noqa: E501

        self.__connected_topic = f"{fragments[TOPIC_FRAGMENTS[FRAGMENT_DOMAIN]]}/connected/{fragments[TOPIC_FRAGMENTS[FRAGMENT_SERIAL_NUMBER]]}/{fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]}/{fragments[TOPIC_FRAGMENTS[FRAGMENT_UNIQUE_ID]]}"  # noqa: E501
        self.__gw_connected_topic = f"{fragments[TOPIC_FRAGMENTS[FRAGMENT_DOMAIN]]}/connected/{fragments[TOPIC_FRAGMENTS[FRAGMENT_SERIAL_NUMBER]]}/gw"  # noqa: E501
        self.__title = title if title is not None else self.__unique_id
        self.__domain = fragments[TOPIC_FRAGMENTS[FRAGMENT_DOMAIN]]
        self.__state: Any = None
        self.__values: Optional[DeviceValue] = None

        self.__entity_callbacks: Optional[dict[tuple[str, int], Callable[[], Any]]] = None

    @property
    def unique_id(self) -> str:
        """Get unique_id of the device

        Returns:
            str: Unique ID
        """
        return self.__unique_id

    @property
    def is_subscribed(self) -> bool:
        """Is device subscribed to mqtt

        Returns:
            bool: True/False
        """
        return self.__mqtt.is_subscribed(self.__state_topic)

    @property
    def device_class(self) -> str:
        """Get device class of the device

        Returns:
            str: Device class
        """
        return self.__device_class.TYPE_ID

    def get_settable_attributes(self) -> dict:
        """
        Returns the settable attributes dictionary.
        This method is used ONLY by the IntegrationDeviceTester for testing purposes.
        """
        return getattr(self.__device_class, "SETTABLE_ATTRIBUTES", {})

    @property
    def inels_type(self) -> str:
        """Get inels type of the device

        Returns:
            str: Type
        """
        return self.__inels_type

    @property
    def device_type(self) -> str:
        """Get type of the device

        Returns:
            str: Type
        """
        return self.__device_type

    @property
    def parent_id(self) -> str:
        """Get Id of the controller (PLC, Bridge)

        Returns:
            str: Parent ID
        """
        return self.__parent_id

    @property
    def title(self) -> str:
        """Get name of the device

        Returns:
            str: Name
        """
        return self.__title

    @property
    def is_available(self) -> bool:
        """Get info about availability of device

        Returns:
            bool: True/False
        """
        gw = self.__mqtt.messages().get(self.gw_connected_topic)
        if gw is not None:
            if not GW_CONNECTED.get(gw):  # type: ignore[call-overload]
                return False

        val = self.__mqtt.messages().get(self.connected_topic)
        if isinstance(val, (bytes, bytearray)):
            val = val.decode()  # type: ignore[unreachable]

        # Temporary workaround to provide an always-online status for DT [164, 165, 166, 167, 168]
        if self.__device_class.TYPE_ID in ["164", "165", "166", "167", "168"]:
            return self.__values is not None and self.__values.ha_value is not None
        else:
            return bool(
                val is not None
                and DEVICE_CONNECTED.get(val)
                and self.__values is not None
                and self.__values.ha_value is not None
            )

    @property
    def set_topic(self) -> Union[str, None]:
        """Set topic

        Returns:
            str: string of the set topic
        """
        return self.__set_topic

    @property
    def state_topic(self) -> str:
        """State topic

        Returns:
            str: string of the status topic
        """
        return self.__state_topic

    @property
    def domain(self) -> str:
        """Domain name of the topic
           it should represent the manufacturer

        Returns:
            str: Name of the domain
        """
        return self.__domain

    @property
    def connected_topic(self) -> str:
        """Connected topic

        Returns:
            str: string of the connected topic
        """
        return self.__connected_topic

    @property
    def gw_connected_topic(self) -> str:
        """Gateway connected topic

        Returns:
            str: string of the gateway connected topic
        """
        return self.__gw_connected_topic

    @property
    def state(self) -> Any:
        """State of the device."""
        if self.__state is None:
            self.get_value()

        return self.__state

    @property
    def values(self) -> Optional[DeviceValue]:
        """Get values of inels and ha type."""
        return self.__values

    @property
    def last_values(self) -> LastHAValue:
        """Get last value of the device

        Returns:
            LastHAValue: Container for the previous Home Assistant value.
        """
        if self.__values:  # previous state exists
            return self.__values.last_value
        else:
            val = self.__mqtt.last_value(self.__state_topic)
            device_value = DeviceValue(
                self.__device_type,
                self.__inels_type,
                self.__device_class,
                inels_value=val.decode() if val is not None else None,  # type: ignore[attr-defined]
            )
            return LastHAValue(device_value.ha_value)

    @property
    def mqtt(self) -> InelsMqtt:
        """Instnace of broker."""
        return self.__mqtt

    def update_value(self, new_value: Any) -> DeviceValue:
        """Update value after broker change it."""
        return self.__get_value(new_value)

    def __get_value(self, val: Any) -> DeviceValue:
        """Get value and transform into the DeviceValue."""

        dev_value = DeviceValue(
            self.__device_type,
            self.__inels_type,
            self.__device_class,
            inels_value=(val.decode() if val is not None else None),
            last_value=LastHAValue(self.__values.ha_value) if self.__values else self.last_values,
        )
        self.__state = (
            dev_value.ha_value.copy()
            if (dev_value.ha_value is not DUMMY_VAL and dev_value.ha_value is not None)
            else DUMMY_VAL
        )
        self.__values = dev_value

        return dev_value

    def get_value(self) -> DeviceValue:
        """Get value from inels

        Returns:
            Any: DeviceValue
        """

        val = self.__mqtt.messages().get(self.state_topic)
        return self.__get_value(val)

    def set_ha_value(self, value: Any) -> bool:
        """Set HA value. Will automaticaly convert HA value
        into the inels value format.

        Args:
            value (Any): Object value belonging to HA device
        Returns:
            true/false if publishing is successfull or not
        """
        dev = DeviceValue(
            self.__device_type,
            self.__inels_type,
            self.__device_class,
            ha_value=value,
            last_value=LastHAValue(self.__values.ha_value if self.__values else None),
        )

        # This is a workaround to the last value before turn off since ramp increments are built into mqtt events
        if hasattr(value, 'light_coa_toa'):
            _values = self.__values
            for i in range(len(_values.ha_value.light_coa_toa)):
                _values.ha_value.light_coa_toa[i].brightness_before_off = value.light_coa_toa[i].brightness_before_off
            self.__values = _values

        ret = False
        if self.__set_topic is not None:
            ret = self.__mqtt.publish(self.__set_topic, dev.inels_set_value)

        return ret

    def info(self) -> "DeviceInfo":
        """Device info."""
        return DeviceInfo(self)

    def info_serialized(self) -> str:
        """Device info in json format string

        Returns:
            str: JSON string format
        """
        info = {
            "name": self.__title,
            "device_type": self.__device_type,
            "id": self.__unique_id,
            "via_device": self.__parent_id,
        }

        json_serialized = json.dumps(info)
        _LOGGER.info("Device: %s", json_serialized)

        return json_serialized

    def add_ha_callback(self, key: str, index: int, fnc: Callable[[], Any]) -> None:
        t: tuple[str, int] = (key, index)
        if self.__entity_callbacks is None:
            self.__entity_callbacks = dict()
        self.__entity_callbacks[t] = fnc

    def ha_diff(self, last_val: Any, curr_val: Any) -> None:
        if self.__entity_callbacks is None:
            return

        if last_val is DUMMY_VAL or curr_val is DUMMY_VAL:
            return

        for k, curr_value in curr_val.__dict__.items():
            if k.startswith("_"):
                continue

            last_value = last_val.__dict__.get(k)
            if isinstance(curr_value, list):
                for i, (curr_item, last_item) in enumerate(zip(curr_value, last_value, strict=True)):
                    if curr_item != last_item:
                        self.__entity_callbacks.get((k, i), lambda: None)()  # type: ignore [call-arg]
            elif curr_value != last_value:
                self.__entity_callbacks.get((k, -1), lambda: None)()  # type: ignore [call-arg]

    def complete_callback(self) -> None:
        if self.__entity_callbacks:
            for v in tuple(self.__entity_callbacks.values()):
                v()

    def callback(self, availability_update: bool) -> None:
        """Update value in device and call the callbacks of the respective entities."""
        self.get_value()

        if availability_update:  # recalculate state for all the entities as they became unavailable/available
            self.complete_callback()
        elif self.__values and self.last_values:
            self.ha_diff(  # differential availability
                last_val=self.last_values.ha_value,
                curr_val=self.__values.ha_value,
            )


class DeviceInfo(object):
    """Device info class."""

    def __init__(self, device: Device) -> None:
        """Create object of the class

        Args:
            device (Device): device object
        """
        self.__device = device

    @property
    def manufacturer(self) -> str:
        """Manufacturer property."""
        return MANUFACTURER

    @property
    def sw_version(self) -> str:
        """Version of software."""
        return VERSION

    @property
    def model_number(self) -> str:
        """Modle of the device."""
        return self.__device.inels_type

    @property
    def serial_number(self) -> str:
        """Serial number of the device."""
        return self.__device.unique_id
