"""Class handle specific platform switch."""
from inelsmqtt.devices import Device
from inelsmqtt import InelsMqtt
from inelsmqtt.util import new_object
from inelsmqtt.const import Element, TEMPERATURE

LIST_OF_FEATURES = {
    Element.RFSTI_11B.value: [TEMPERATURE],
}


class Switch(Device):
    """Carry switch stuff

    Args:
        Device (_type_): base class for all platforms
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
        """Convert set value to the proper switch object."""
        # basic property is on
        kwargs = {"on": value}

        # other properties will be created from features
        if self.features is not None:
            for feature in self.features:
                kwargs[feature] = self.state.__dict__.get(feature)


        # ALL THIS DOES IS ADD turn "on" either True or False, and keeps the same properties 
        # new object passing into the device set func Device value object
        return super().set_ha_value(new_object(**kwargs))