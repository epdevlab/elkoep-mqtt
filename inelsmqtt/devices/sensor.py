"""Class handle specific platform sensor."""
from inelsmqtt import InelsMqtt
from inelsmqtt.devices import Device
from inelsmqtt.const import (
    Element,
    TEMPERATURE,
    BATTERY,
    TEMP_IN,
    TEMP_OUT,
    LIGHT_IN, 
    AIN,
    HUMIDITY,
    DEW_POINT
)

LIST_OF_FEATURES = {
    Element.RFTC_10_G.value: [TEMPERATURE, BATTERY],
    Element.RFTI_10B.value: [TEMP_IN, TEMP_OUT, BATTERY],
    
    Element.SA3_01B.value: [TEMP_IN],
    Element.DA3_22M.value: [TEMP_IN],
    Element.GTR3_50.value: [TEMP_IN, LIGHT_IN, AIN, HUMIDITY, DEW_POINT],
    Element.GSB3_90SX.value: [TEMP_IN, LIGHT_IN, AIN, HUMIDITY, DEW_POINT]
}

class Sensor(Device):
    """Carry sensor stuff

    Args:
        Device (_type_): it base class for all platforms
    """

    def __init__(
        self,
        mqtt: InelsMqtt,
        state_topic: str,
        title: str = None,
    ) -> None:
        """Initit inels switch class"""
        super().__init__(mqtt=mqtt, state_topic=state_topic, title=title)
        self._set_features(LIST_OF_FEATURES.get(self.inels_type.value))
