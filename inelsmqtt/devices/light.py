"""Class handle specific platform light."""
from inelsmqtt import InelsMqtt
from inelsmqtt.devices import Device
from inelsmqtt.const import Element, BRIGHTNESS

LIST_OF_FEATURES = {
    Element.RFDAC_71B.value: [BRIGHTNESS],
}

class Light(Device):
    """Carry light stuff

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

    def set_ha_value(self, value: bool) -> bool:
        """Convert set value to the proper light object."""
        # new object passing into the device set func Device value object
        return super().set_ha_value(value)
