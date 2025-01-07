from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, Any, List

from inelsmqtt.utils.common import SettableAttribute

if TYPE_CHECKING:
    from inelsmqtt.utils.core import DeviceValue

from inelsmqtt.const import (
    AIN,
    BATTERY,
    BLUE,
    BUTTON,
    BUTTON_NUMBER,
    CLIMATE,
    COVER,
    CURRENT_TEMP,
    GREEN,
    HUMIDITY,
    IDENTITY,
    LIGHT,
    OPEN_IN_PERCENTAGE,
    OUT,
    POSITION,
    RED,
    RELAY,
    REQUIRED_TEMP,
    RF_2_BUTTON_CONTROLLER,
    RF_CONTROLLER,
    RF_DETECTOR,
    RF_DIMMER,
    RF_DIMMER_RGB,
    RF_FLOOD_DETECTOR,
    RF_LIGHT_BULB,
    RF_MOTION_DETECTOR,
    RF_SHUTTER_UNIT,
    RF_SHUTTERS,
    RF_SINGLE_DIMMER,
    RF_SINGLE_SWITCH,
    RF_SWITCHING_UNIT,
    RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR,
    RF_TEMPERATURE_HUMIDITY_SENSOR,
    RF_TEMPERATURE_INPUT,
    RF_THERMOSTAT,
    RF_WIRELESS_THERMOVALVE,
    SENSOR,
    SHUTTER,
    STATE,
    SWITCH,
    TEMP_IN,
    TEMP_OUT,
    WHITE,
    Climate_modes,
    Shutter_state,
)
from inelsmqtt.utils.common import (
    DataDict,
    Formatter,
    RGBLight,
    Shutter,
    Shutter_pos,
    SimpleLight,
    SimpleRelay,
    WarmLight,
    new_object,
    trim_inels_status_values,
    twos_comp_1B,
)


class CommTest:
    @classmethod
    def COMM_TEST(cls) -> str:
        """
        This default implementation returns an empty string, indicating that the device does not support a communication test.
        Subclasses should override this method to provide specific functionality.
        """
        return ""

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        return ""


class DT_01(CommTest):
    class Command(IntEnum):
        ON = 0x01
        OFF = 0x02
        COMM_TEST = 0x08

    INELS_TYPE = RF_SINGLE_SWITCH
    HA_TYPE = SWITCH
    TYPE_ID = "01"

    DATA: DataDict = {RELAY: 1}

    # NOTE: This dictionary is used ONLY for testing purposes.
    SETTABLE_ATTRIBUTES = {"is_on": SettableAttribute("simple_relay.0.is_on", bool, [True, False])}

    @classmethod
    def COMM_TEST(cls) -> str:
        return cls.create_command_payload(cls.Command.COMM_TEST)

    @staticmethod
    def create_command_payload(command: int) -> str:
        return Formatter.format_data([command, 0])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        simple_relay: list[SimpleRelay] = []
        simple_relay.append(
            SimpleRelay(
                is_on=int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, RELAY, ""), 16) != 0
            )
        )
        return new_object(
            simple_relay=simple_relay,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        cmd = cls.Command.ON if device_value.ha_value.simple_relay[0].is_on else cls.Command.OFF
        return cls.create_command_payload(cmd)


class DT_02(CommTest):
    class Command(IntEnum):
        ON = 0x01
        OFF = 0x02
        IMPULSE = 0x03
        DELAYED_OFF = 0x04
        DELAYED_ON = 0x05
        SET_DELAYED_OFF = 0x06
        SET_DELAYED_ON = 0x07
        COMM_TEST = 0x08

    INELS_TYPE = RF_SWITCHING_UNIT
    HA_TYPE = SWITCH
    TYPE_ID = "02"

    DATA: DataDict = {RELAY: 1}
    TIME_HIGH_BYTE = 0
    TIME_LOW_BYTE = 0

    SETTABLE_ATTRIBUTES = {"is_on": SettableAttribute("simple_relay.0.is_on", bool, [True, False])}

    @classmethod
    def COMM_TEST(cls) -> str:
        return cls.create_command_payload(cls.Command.COMM_TEST, cls.TIME_HIGH_BYTE, cls.TIME_LOW_BYTE)

    @staticmethod
    def create_command_payload(command: int, time_high_byte: int = 0, time_low_byte: int = 0) -> str:
        return Formatter.format_data([command, time_high_byte, time_low_byte])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        """Create a HA value object for a switch."""
        simple_relay: list[SimpleRelay] = []
        simple_relay.append(
            SimpleRelay(
                is_on=int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, RELAY, ""), 16) != 0
            )
        )
        return new_object(
            simple_relay=simple_relay,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        """Generate command string to turn the relay on or off."""
        cmd = cls.Command.ON if device_value.ha_value.simple_relay[0].is_on else cls.Command.OFF
        return cls.create_command_payload(cmd)


class DT_03(CommTest):
    class Command(IntEnum):
        OPEN = 0x01
        CLOSE = 0x02
        START_UP = 0x03
        STOP_UP = 0x04
        START_DOWN = 0x05
        STOP_DOWN = 0x06
        SET_UP_TIME = 0x07
        SET_DOWN_TIME = 0x08
        COMM_TEST = 0x09

    INELS_TYPE = RF_SHUTTERS
    HA_TYPE = COVER
    TYPE_ID = "03"

    DATA: DataDict = {SHUTTER: [1]}
    TIME_HIGH_BYTE = 0
    TIME_LOW_BYTE = 0

    SHUTTER_STATE_SET = {
        Shutter_state.Open: Command.OPEN,
        Shutter_state.Closed: Command.CLOSE,
        Shutter_state.Stop_up: Command.STOP_UP,
        Shutter_state.Stop_down: Command.STOP_DOWN,
    }

    SETTABLE_ATTRIBUTES = {
        "state": SettableAttribute(
            "shutters.0.state",
            Shutter_state,
            [Shutter_state.Open, Shutter_state.Closed, Shutter_state.Stop_up, Shutter_state.Stop_down],
        ),
    }

    @classmethod
    def COMM_TEST(cls) -> str:
        return cls.create_command_payload(cls.Command.COMM_TEST, cls.TIME_HIGH_BYTE, cls.TIME_LOW_BYTE)

    @staticmethod
    def create_command_payload(command: int, time_high_byte: int = 0, time_low_byte: int = 0) -> str:
        return Formatter.format_data([command, time_high_byte, time_low_byte])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        shutter_val = Shutter_state(
            int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, SHUTTER, ""), 16)
        )

        # So as to continue driving it down if it aisn't closed
        # and continue opening it if it isn't open
        if shutter_val not in [Shutter_state.Open, Shutter_state.Closed]:
            shutter_val = device_value.last_value.ha_value.shutters[0].state

        shutters: List[Shutter] = []
        shutters.append(Shutter(state=shutter_val, is_closed=shutter_val == Shutter_state.Closed))
        return new_object(
            shutters=shutters,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        cmd = cls.SHUTTER_STATE_SET[device_value.ha_value.shutters[0].state]
        return cls.create_command_payload(cmd)


class DT_04(CommTest):
    class Command(IntEnum):
        BRIGHTNESS = 0x01
        COMM_TEST = 0x07

    INELS_TYPE = RF_SINGLE_DIMMER
    HA_TYPE = LIGHT
    TYPE_ID = "04"

    DATA: DataDict = {RF_DIMMER: [0, 1]}

    SETTABLE_ATTRIBUTES = {
        "brightness": SettableAttribute("simple_light.0.brightness", int, list(range(0, 101, 10))),
    }

    @classmethod
    def COMM_TEST(cls) -> str:
        return cls.create_command_payload(cls.Command.COMM_TEST)

    @staticmethod
    def create_command_payload(command: int, brt_high_byte: int = 0, brt_low_byte: int = 0) -> str:
        return Formatter.format_data([command, brt_high_byte, brt_low_byte])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        brightness = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, RF_DIMMER, ""), 16)
        brightness = int((((0xFFFF - brightness) - 10000) / 1000) * 5)
        brightness = round(brightness, -1)

        simple_light = []
        simple_light.append(SimpleLight(brightness=brightness))
        return new_object(simple_light=simple_light)

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        out = round(device_value.ha_value.simple_light[0].brightness, -1)
        out = out if out < 100 else 100

        word = 0xFFFF - ((int(out / 5) * 1000) + 10000)
        brt_high_byte = word >> 8
        brt_low_byte = word & 0xFF
        return cls.create_command_payload(cls.Command.BRIGHTNESS, brt_high_byte, brt_low_byte)


class DT_05(CommTest):
    class Command(IntEnum):
        BRIGHTNESS = 0x01
        DELAYED_ON = 0x02
        DELAYED_OFF = 0x03
        SET_DELAYED_ON = 0x05
        SET_DELAYED_OFF = 0x06
        COMM_TEST = 0x07

    INELS_TYPE = RF_DIMMER
    HA_TYPE = LIGHT
    TYPE_ID = "05"

    DATA: DataDict = {RF_DIMMER: [0, 1]}

    SETTABLE_ATTRIBUTES = {
        "brightness": SettableAttribute("simple_light.0.brightness", int, list(range(0, 101, 10))),
    }

    @classmethod
    def COMM_TEST(cls) -> str:
        return cls.create_command_payload(cls.Command.COMM_TEST)

    @staticmethod
    def create_command_payload(command: int, high_byte: int = 0, low_byte: int = 0) -> str:
        return Formatter.format_data([command, high_byte, low_byte])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        """Create a HA value object for a dimmer."""
        brightness = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, RF_DIMMER, ""), 16)
        brightness = int((((0xFFFF - brightness) - 10000) / 1000) * 5)
        brightness = round(brightness, -1)

        simple_light: List[SimpleLight] = []
        simple_light.append(SimpleLight(brightness=brightness))
        return new_object(simple_light=simple_light)

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        """Generate command string to set the brightness of a dimmer."""
        out = round(device_value.ha_value.simple_light[0].brightness, -1)
        out = out if out < 100 else 100

        word = 0xFFFF - ((int(out / 5) * 1000) + 10000)
        high_byte = word >> 8
        low_byte = word & 0xFF
        return cls.create_command_payload(cls.Command.BRIGHTNESS, high_byte, low_byte)


class DT_06(CommTest):
    class Command(IntEnum):
        RGBA = 0x01
        COMM_TEST = 0x07

    INELS_TYPE = RF_DIMMER_RGB
    HA_TYPE = LIGHT
    TYPE_ID = "06"

    DATA: DataDict = {RED: [1], GREEN: [2], BLUE: [3], OUT: [4]}

    SETTABLE_ATTRIBUTES = {
        "red": SettableAttribute("rgb.0.r", int, list(range(0, 256))),
        "green": SettableAttribute("rgb.0.g", int, list(range(0, 256))),
        "blue": SettableAttribute("rgb.0.b", int, list(range(0, 256))),
        "brightness": SettableAttribute("rgb.0.brightness", int, list(range(0, 256))),
    }

    @classmethod
    def COMM_TEST(cls) -> str:
        return cls.create_command_payload(cls.Command.COMM_TEST, 0, 0, 0, 0)

    @staticmethod
    def create_command_payload(command: int, red: int, green: int, blue: int, brightness: int) -> str:
        return Formatter.format_data([command, red, green, blue, brightness, 0])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        """Create a HA value object for a RGB."""
        red = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, RED, ""), 16)
        green = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, GREEN, ""), 16)
        blue = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, BLUE, ""), 16)
        brightness = int(
            int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, OUT, ""), 16) * 100.0 / 255.0
        )

        rgb = []
        rgb.append(
            RGBLight(
                r=red,
                g=green,
                b=blue,
                brightness=brightness,
            )
        )
        return new_object(rgb=rgb)

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        """Generate command string to set the RGB and brightness values."""
        cmd = cls.Command.RGBA
        rgb = device_value.ha_value.rgb[0]
        scaled_brightness = int(rgb.brightness * 2.55)
        return cls.create_command_payload(cmd, rgb.r, rgb.g, rgb.b, scaled_brightness)


class DT_07(CommTest):
    class Command(IntEnum):
        ON = 0x01
        OFF = 0x02
        COMM_TEST = 0x08

    INELS_TYPE = RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR
    HA_TYPE = SWITCH
    TYPE_ID = "07"

    DATA: DataDict = {RELAY: [1], TEMP_OUT: [3, 2]}
    RESERVED_BYTE = 0

    STATE_SET = {
        True: Command.ON,
        False: Command.OFF,
    }

    SETTABLE_ATTRIBUTES = {
        "is_on": SettableAttribute("simple_relay.0.is_on", bool, [True, False]),
    }

    @classmethod
    def COMM_TEST(cls) -> str:
        return cls.create_command_payload(cls.Command.COMM_TEST)

    @staticmethod
    def create_command_payload(command: int) -> str:
        return Formatter.format_data([command, DT_07.RESERVED_BYTE])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        simple_relay: list[SimpleRelay] = []
        simple_relay.append(
            SimpleRelay(
                is_on=int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, RELAY, ""), 16) != 0
            )
        )
        temp = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_OUT, "")

        return new_object(
            simple_relay=simple_relay,
            temp_out=temp,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        command = cls.STATE_SET[device_value.ha_value.simple_relay[0].is_on]
        return cls.create_command_payload(command)


class DT_09(CommTest):
    INELS_TYPE = RF_WIRELESS_THERMOVALVE
    HA_TYPE = CLIMATE
    TYPE_ID = "09"

    DATA: DataDict = {
        OPEN_IN_PERCENTAGE: [0],
        CURRENT_TEMP: [1],
        BATTERY: [2],
        REQUIRED_TEMP: [3],
    }

    SETTABLE_ATTRIBUTES = {
        "required_temp": SettableAttribute("thermovalve.required", float, [x / 2 for x in range(0, 129)]),
    }

    @staticmethod
    def create_command_payload(temp_required: int) -> str:
        return Formatter.format_data([0, temp_required, 0])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        # fetches all the status values and compacts them into a new object
        temp_current_hex = trim_inels_status_values(device_value.inels_status_value, cls.DATA, CURRENT_TEMP, "")
        temp_current = twos_comp_1B(int(temp_current_hex, 16)) * 0.5
        temp_required_hex = trim_inels_status_values(device_value.inels_status_value, cls.DATA, REQUIRED_TEMP, "")
        temp_required = twos_comp_1B(int(temp_required_hex, 16)) * 0.5
        battery = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, BATTERY, ""), 16)
        open_to_hex = trim_inels_status_values(device_value.inels_status_value, cls.DATA, OPEN_IN_PERCENTAGE, "")
        open_to_percentage = int(open_to_hex, 16) * 0.5

        climate_mode = Climate_modes.Off
        if temp_current < temp_required:
            climate_mode = Climate_modes.Heat

        return new_object(
            low_battery=(battery != 0),
            thermovalve=new_object(
                current=temp_current,
                required=temp_required,
                climate_mode=climate_mode,
                open_in_percentage=open_to_percentage,
            ),
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        temp_required = int(round(device_value.ha_value.thermovalve.required * 2, 0))
        return cls.create_command_payload(temp_required)


class DT_10(CommTest):
    INELS_TYPE = RF_TEMPERATURE_INPUT
    HA_TYPE = SENSOR
    TYPE_ID = "10"

    DATA: DataDict = {BATTERY: [0], TEMP_IN: [2, 1], TEMP_OUT: [4, 3]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        battery = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, BATTERY, ""), 16)
        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        temp_out = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_OUT, "")

        return new_object(
            low_battery=(battery != 0),
            temp_in=temp_in,
            temp_out=temp_out,
        )


class DT_12(CommTest):
    INELS_TYPE = RF_THERMOSTAT
    HA_TYPE = SENSOR
    TYPE_ID = "12"

    DATA: DataDict = {TEMP_IN: [0], BATTERY: [2]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        temp_in = (
            twos_comp_1B(int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, ""), 16))
            * 0.5
        )
        battery = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, BATTERY, ""), 16)

        return new_object(
            low_battery=(battery == 0x81),
            temp_in=temp_in,
        )


class DT_13(CommTest):
    class Command(IntEnum):
        BRIGHTNESS = 0x0F
        COMM_TEST = 0x07

    INELS_TYPE = RF_LIGHT_BULB
    HA_TYPE = LIGHT
    TYPE_ID = "13"

    DATA: DataDict = {OUT: [4], WHITE: [5]}

    SETTABLE_ATTRIBUTES = {
        "brightness": SettableAttribute("warm_light.0.brightness", int, list(range(0, 101))),
        "relative_ct": SettableAttribute("warm_light.0.relative_ct", int, list(range(0, 101))),
    }

    @classmethod
    def COMM_TEST(cls) -> str:
        return cls.create_command_payload(cls.Command.COMM_TEST)

    @staticmethod
    def create_command_payload(command: int, brightness: int = 0, relative_ct: int = 0) -> str:
        return Formatter.format_data([command, 0, 0, 0, brightness, relative_ct])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        warm_light = []
        warm_light.append(
            WarmLight(
                brightness=round(
                    int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, OUT, ""), 16)
                    * 100.0
                    / 255.0
                ),
                relative_ct=round(
                    int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, WHITE, ""), 16)
                    * 100.0
                    / 255.0
                ),
            ),
        )

        return new_object(warm_light=warm_light)

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        brightness = round(device_value.ha_value.warm_light[0].brightness * 2.55)
        relative_ct = round(device_value.ha_value.warm_light[0].relative_ct * 2.55)
        return cls.create_command_payload(cls.Command.BRIGHTNESS, brightness, relative_ct)


class DT_15(CommTest):
    INELS_TYPE = RF_FLOOD_DETECTOR
    HA_TYPE = SENSOR
    TYPE_ID = "15"

    DATA: DataDict = {STATE: [0], AIN: [2, 1]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        state = trim_inels_status_values(device_value.inels_status_value, cls.DATA, STATE, "")
        state = f"0x{state}"
        state = f"{int(state, 16):0>8b}"

        ain = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, AIN, ""), 16) / 100

        low_battery = state[7] == "1"
        flooded = state[0] == "1"
        ains = []
        ains.append(ain)

        return new_object(
            low_battery=low_battery,
            flooded=flooded,
            ains=ains,
        )


class DT_16(CommTest):
    INELS_TYPE = RF_DETECTOR
    HA_TYPE = SENSOR
    TYPE_ID = "16"

    DATA: DataDict = {STATE: [0]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        state = trim_inels_status_values(device_value.inels_status_value, cls.DATA, STATE, "")
        state = f"0x{state}"
        state = f"{int(state, 16):0>8b}"

        low_battery = state[4] == "1"
        detected = state[3] == "1"
        tamper = state[1] == "1"

        return new_object(
            low_battery=low_battery,
            detected=detected,
            tamper=tamper,
        )


class DT_17(CommTest):
    INELS_TYPE = RF_MOTION_DETECTOR
    HA_TYPE = SENSOR
    TYPE_ID = "17"

    DATA: DataDict = {STATE: [0]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        state = trim_inels_status_values(device_value.inels_status_value, cls.DATA, STATE, "")
        state = f"0x{state}"
        state = f"{int(state, 16):0>8b}"

        low_battery = state[4] == "1"
        motion = state[3] == "1"
        tamper = state[1] == "1"

        return new_object(
            low_battery=low_battery,
            motion=motion,
            tamper=tamper,
        )


class DT_18(CommTest):
    INELS_TYPE = RF_2_BUTTON_CONTROLLER
    HA_TYPE = BUTTON
    TYPE_ID = "18"

    DATA: DataDict = {STATE: [0], IDENTITY: [1]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        state = trim_inels_status_values(device_value.inels_status_value, cls.DATA, STATE, "")
        state = f"0x{state}"
        state = f"{int(state, 16):0>8b}"

        identity = trim_inels_status_values(device_value.inels_status_value, cls.DATA, IDENTITY, "")

        low_battery = state[4] == "1"
        pressed = state[3] == "1"
        if device_value.last_value is None:
            btn = [False, False]
        else:
            btn = device_value.last_value.ha_value.btn

        if identity in BUTTON_NUMBER:
            number = BUTTON_NUMBER[identity]
            if number <= 2:
                btn[number - 1] = pressed

        return new_object(
            low_battery=low_battery,
            btn=btn,
        )


class DT_19(CommTest):
    INELS_TYPE = RF_CONTROLLER
    HA_TYPE = BUTTON
    TYPE_ID = "19"

    DATA: DataDict = {STATE: [0], IDENTITY: [1]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        state = trim_inels_status_values(device_value.inels_status_value, cls.DATA, STATE, "")
        state_hex_str = f"0x{state}"
        # interpret the value and write it in binary
        state_bin_str = f"{int(state_hex_str, 16):0>8b}"

        # read which button was last pressed
        identity = trim_inels_status_values(device_value.inels_status_value, cls.DATA, IDENTITY, "")

        low_battery = state_bin_str[4] == "1"
        pressed = state_bin_str[3] == "1"
        if device_value.last_value is None:
            btn = [
                False,
                False,
                False,
                False,
            ]
        else:
            btn = device_value.last_value.ha_value.btn

        if identity in BUTTON_NUMBER:
            number = BUTTON_NUMBER[identity]
            if number <= 4:
                btn[number - 1] = pressed

        return new_object(low_battery=low_battery, btn=btn)


class DT_21(CommTest):
    class Command(IntEnum):
        OPEN = 0x01
        CLOSE = 0x02
        START_UP = 0x03
        STOP_UP = 0x04
        START_DOWN = 0x05
        STOP_DOWN = 0x06
        SET_UP_TIME = 0x07
        SET_DOWN_TIME = 0x08
        COMM_TEST = 0x09
        POSITION = 0x0A

    INELS_TYPE = RF_SHUTTER_UNIT
    HA_TYPE = COVER
    TYPE_ID = "21"

    DATA: DataDict = {SHUTTER: [1], POSITION: [2]}
    HIGH_BYTE = 0
    LOW_BYTE = 0

    SHUTTER_STATE_SET = {
        Shutter_state.Open: Command.OPEN,
        Shutter_state.Closed: Command.CLOSE,
        Shutter_state.Stop_up: Command.STOP_UP,
        Shutter_state.Stop_down: Command.STOP_DOWN,
    }

    SETTABLE_ATTRIBUTES = {
        "state": SettableAttribute(
            "shutters_with_pos.0.state",
            Shutter_state,
            [Shutter_state.Open, Shutter_state.Closed, Shutter_state.Stop_up, Shutter_state.Stop_down],
        ),
        "position": SettableAttribute("shutters_with_pos.0.position", int, list(range(0, 101))),
    }

    @classmethod
    def COMM_TEST(cls) -> str:
        return cls.create_command_payload(cls.Command.COMM_TEST, cls.HIGH_BYTE, cls.LOW_BYTE)

    @staticmethod
    def create_command_payload(command: int, high_byte: int = 0, low_byte: int = 0) -> str:
        return Formatter.format_data([command, high_byte, low_byte])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        shutters_with_pos = []

        position = 100 - int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, POSITION, ""), 16)

        shutter_val = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, SHUTTER, ""))
        shutter_val = ((shutter_val >> 1) & 1) | (shutter_val & 1) << 1  # swap bit 0 with bit 1

        if shutter_val == Shutter_state.Closed and position != 0:
            shutter_val = Shutter_state.Open

        if (device_value.last_value is not None) and (shutter_val not in [Shutter_state.Open, Shutter_state.Closed]):
            shutter_val = device_value.last_value.ha_value.shutters_with_pos[0].state

        shutters_with_pos.append(
            Shutter_pos(
                state=Shutter_state(shutter_val),
                is_closed=shutter_val == Shutter_state.Closed,
                position=position,
                set_pos=False,
            )
        )

        return new_object(
            shutters_with_pos=shutters_with_pos,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        if device_value.ha_value.shutters_with_pos[0].set_pos:
            position = 100 - round(device_value.ha_value.shutters_with_pos[0].position)
            return cls.create_command_payload(cls.Command.POSITION, 0, position)
        else:
            cmd = cls.SHUTTER_STATE_SET[device_value.ha_value.shutters_with_pos[0].state]
            return cls.create_command_payload(cmd)


class DT_30(CommTest):
    INELS_TYPE = RF_TEMPERATURE_HUMIDITY_SENSOR
    HA_TYPE = SENSOR
    TYPE_ID = "30"

    DATA: DataDict = {BATTERY: [0], TEMP_IN: [2, 1], HUMIDITY: [3]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        battery = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, BATTERY, ""), 16)
        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        humidity = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, HUMIDITY, ""), 16)

        return new_object(
            low_battery=(battery != 0),
            temp_in=temp_in,
            humidity=humidity,
        )
