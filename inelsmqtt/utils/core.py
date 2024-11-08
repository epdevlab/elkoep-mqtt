"""Utility classes."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, List, Optional, Protocol

from inelsmqtt.protocols import cu3, elanrf

_LOGGER = logging.getLogger(__name__)

# To prevent the value as being none,
# if anything goes wrong when calculating the value,
# we give an empty object that will simply not match with any keywords
# it is filtered out in set_val
DUMMY_VAL = object()

# Devices that support having no state topic at setup time
INELS_ASSUMED_STATE_DEVICES: List[type[DeviceClassProtocol]] = [
    elanrf.DT_18,
    elanrf.DT_19,
]


class DeviceTypeNotFound(Exception):
    """Raised when a device type is not found in the ProtocolHandlerMapper."""

    pass


class DeviceClassProtocol(Protocol):
    """
    Protocol defining the interface for device classes.
    This is used for static type checking.
    """

    INELS_TYPE: str
    HA_TYPE: str
    TYPE_ID: str

    @classmethod
    def create_ha_value_object(cls, device_value: Any) -> Any: ...

    @classmethod
    def create_inels_set_value(cls, device_value: Any) -> str: ...


class ProtocolHandlerMapper:
    DEVICE_TYPE_MAP: dict[str, type[DeviceClassProtocol]] = {
        "01": elanrf.DT_01,
        "02": elanrf.DT_02,
        "03": elanrf.DT_03,
        "04": elanrf.DT_04,
        "05": elanrf.DT_05,
        "06": elanrf.DT_06,
        "07": elanrf.DT_07,
        "09": elanrf.DT_09,
        "10": elanrf.DT_10,
        "12": elanrf.DT_12,
        "13": elanrf.DT_13,
        "15": elanrf.DT_15,
        "16": elanrf.DT_16,
        "17": elanrf.DT_17,
        "18": elanrf.DT_18,
        "19": elanrf.DT_19,
        "21": elanrf.DT_21,
        "30": elanrf.DT_30,
        "100": cu3.DT_100,
        "101": cu3.DT_101,
        "102": cu3.DT_102,
        "103": cu3.DT_103,
        "104": cu3.DT_104,
        "105": cu3.DT_105,
        "106": cu3.DT_106,
        "107": cu3.DT_107,
        "108": cu3.DT_108,
        "109": cu3.DT_109,
        "111": cu3.DT_111,
        "112": cu3.DT_112,
        "114": cu3.DT_114,
        "115": cu3.DT_115,
        "116": cu3.DT_116,
        "117": cu3.DT_117,
        "120": cu3.DT_120,
        "121": cu3.DT_121,
        "122": cu3.DT_122,
        "123": cu3.DT_123,
        "124": cu3.DT_124,
        "125": cu3.DT_125,
        "128": cu3.DT_128,
        "129": cu3.DT_129,
        "136": cu3.DT_136,
        "137": cu3.DT_137,
        "138": cu3.DT_138,
        "139": cu3.DT_139,
        "140": cu3.DT_140,
        "141": cu3.DT_141,
        "143": cu3.DT_143,
        "144": cu3.DT_144,
        "146": cu3.DT_146,
        "147": cu3.DT_147,
        "148": cu3.DT_148,
        "150": cu3.DT_150,
        "151": cu3.DT_151,
        "153": cu3.DT_153,
        "156": cu3.DT_156,
        "157": cu3.DT_157,
        "158": cu3.DT_158,
        "159": cu3.DT_159,
        "160": cu3.DT_160,
        "163": cu3.DT_163,
        "164": cu3.DT_164,
        "165": cu3.DT_165,
        "166": cu3.DT_166,
        "167": cu3.DT_167,
        "168": cu3.DT_168,
        "169": cu3.DT_169,
        "170": cu3.DT_170,
        "171": cu3.DT_171,
        "172": cu3.DT_172,
        "174": cu3.DT_174,
        "175": cu3.DT_175,
        "176": cu3.DT_176,
        "177": cu3.DT_177,
        "178": cu3.DT_178,
        "179": cu3.DT_179,
        "180": cu3.DT_180,
        "bits": cu3.DT_BITS,
        "integers": cu3.DT_INTEGERS,
    }

    @staticmethod
    def get_handler(device_type: str) -> type[DeviceClassProtocol]:
        """
        Retrieve the handler based on the device type code.

        Args:
            device_type (str): The code that identifies the device type.

        Returns:
            type[DeviceClassProtocol]: The handler associated with the device type code.

        Raises:
            DeviceTypeNotFound: If the device type is not found in the DEVICE_TYPE_MAP.
        """
        handler = ProtocolHandlerMapper.DEVICE_TYPE_MAP.get(device_type)
        if handler is None:
            raise DeviceTypeNotFound(f"Unknown device type: {device_type}")
        return handler


@dataclass
class LastHAValue:
    """Store the last known ha_value without creating reference chains."""

    ha_value: Any


class DeviceValue:
    """Device value interpretation object."""

    def __init__(
        self,
        device_type: str,
        inels_type: str,
        device_class: type[DeviceClassProtocol],
        inels_value: Optional[str] = None,
        ha_value: Any = None,
        last_value: Any = None,
    ) -> None:
        self.device_type = device_type
        self.inels_type = inels_type
        self.device_class = device_class
        self.__inels_status_value = inels_value
        self.__inels_set_value: str = ""
        self.__ha_value = ha_value
        self.__last_value = last_value

        if self.__ha_value is None:
            self.__update_ha_value()

        if self.__inels_set_value == "":
            self.__update_inels_value()

    def __update_ha_value(self) -> None:
        try:
            if self.__inels_status_value is None:
                _LOGGER.info("inels_status_value was 'None' for %s", self.inels_type)
                self.__ha_value = None
            else:
                self.__ha_value = self.device_class.create_ha_value_object(self)
        except Exception as e:
            status_value = self.inels_status_value.replace("\n", " ") if self.inels_status_value else "None"
            _LOGGER.error(
                "Failed to update HA value for %s, status value was '%s': %s",
                self.device_class.TYPE_ID,
                status_value,
                str(e),
            )
            self.__ha_value = DUMMY_VAL

    def __update_inels_value(self) -> None:
        try:
            if self.__ha_value is not DUMMY_VAL:
                if self.__ha_value is None:
                    self.__inels_set_value = getattr(self.device_class, "COMM_TEST", lambda: "")()
                else:
                    self.__inels_set_value = self.device_class.create_inels_set_value(self)
        except Exception as e:
            status_value = self.inels_status_value.replace("\n", " ") if self.inels_status_value else "None"
            _LOGGER.error(
                "Error making 'set' value for device of type '%s', status value was '%s': %s",
                self.device_class.TYPE_ID,
                status_value,
                str(e),
            )
            raise

    @property
    def ha_value(self) -> Any:
        """Converted value from inels mqtt broker into
           the HA format

        Returns:
            Any: object to corespond to HA device
        """
        return self.__ha_value

    @property
    def inels_set_value(self) -> str:
        """Raw inels value for mqtt broker

        Returns:
            str: this is string format value for mqtt broker
        """
        return self.__inels_set_value

    @property
    def inels_status_value(self) -> str:
        """Raw inels value from mqtt broker

        Returns:
            str: quated string from mqtt broker
        """
        return self.__inels_status_value or ""

    @property
    def last_value(self) -> Any:
        """Get the last known value."""
        return self.__last_value
