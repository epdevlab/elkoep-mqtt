"""Class handle specific platform sensor."""
from inelsmqtt import InelsMqtt
from inelsmqtt.devices import Device
from inelsmqtt.const import (
    Element,
    TEMPERATURE,
    BATTERY,
    TEMP_IN,
    TEMP_OUT,
)

LIST_OF_FEATURES = {
    Element.RFTC_10_G.value: [TEMPERATURE, BATTERY],
    Element.RFTI_10B.value: [TEMP_IN, TEMP_OUT, BATTERY],
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
