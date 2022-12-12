"""Class handle generic feature setting."""

from inelsmqtt import InelsMqtt
from inelsmqtt.devices import Device
from inelsmqtt.const import Element, BRIGHTNESS, TEMP_IN, LIGHT_IN, AIN, HUMIDITY, DEW_POINT
from inelsmqtt.util import new_object



LIST_OF_FEATURES = {
    Element.SA3_01B.value: [TEMP_IN],
    Element.DA3_22M.value: [BRIGHTNESS, TEMP_IN],
    Element.GTR3_50.value: [TEMP_IN, LIGHT_IN, AIN, HUMIDITY, DEW_POINT],
    Element.GSB3_90SX.value: [TEMP_IN, LIGHT_IN, AIN, HUMIDITY, DEW_POINT]
}

class BusDevice(Device):
    """Bus device with features

    Args:
        Device (_type_): base class for all platforms
    """
    
    def __init__(
        self,
        mqtt: InelsMqtt,
        state_topic: str,
        title: str = None,
    ) -> None:
        """Init bus device class"""
        super().__init__(mqtt=mqtt, state_topic=state_topic, title=title)
        self._set_features(LIST_OF_FEATURES.get(self.inels_type.value))
        
    def set_ha_value(self, value: bool) -> bool:
        """Convert set value to the proper object."""

        #switch
        if self.inels_type is Element.SA3_01B:
            kwargs = {"on": value}

            if self.features is not None:
                for feature in self.features:
                    kwargs[feature] = self.state.__dict__.get(feature)

            return super().set_ha_value(new_object(**kwargs))
        #light -> might need changes to support multiple channels
        elif self.inels_type is Element.DA3_22M:
            return super().set_ha_value(value)
        else:
            pass