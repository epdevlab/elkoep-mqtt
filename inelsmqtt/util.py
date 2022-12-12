"""Utility classes."""
import logging

from operator import itemgetter
from typing import Any, Dict

from inelsmqtt.mqtt_client import GetMessageType

from .const import (
    Platform,
    Element,
    Archetype,
)

from .const import (
    SENSOR_RFTC_10_G_LOW_BATTERY,
    ANALOG_REGULATOR_SET_BYTES,
    BATTERY,
    DEVICE_TYPE_10_DATA,
    DEVICE_TYPE_12_DATA,
    TEMPERATURE,
    CLIMATE_TYPE_09_DATA,
    CURRENT_TEMP,
    DEVICE_TYPE_05_DATA,
    DEVICE_TYPE_05_HEX_VALUES,
    BUTTON_TYPE_19_DATA,
    BUTTON_DEVICE_AMOUNT,
    BUTTON_NUMBER,
    DEVICE_TYPE_07_DATA,
    REQUIRED_TEMP,
    SHUTTER_SET,
    SHUTTER_STATE_LIST,
    SHUTTER_STATES,
    SWITCH_SET,
    SWITCH_STATE,
    OPEN_IN_PERCENTAGE,
    STATE,
    IDENTITY,
    SWITCH_WITH_TEMP_SET,
    TEMP_OUT,

    RELAY_DATA,
    TWOCHANNELDIMMER_DATA,
    THERMOSTAT_DATA,
    BUTTONARRAY_DATA,

    RELAY_OVERFLOW,
    TEMP_IN,
    DIM_OUT_1,
    DIM_OUT_2,
    PLUS_MINUS_BUTTONS,
    LIGHT_IN,
    AIN,
    HUMIDITY,
    DEW_POINT,

    RELAY_SET,

    THERMOSTAT_SET_BACKLIT_DISPLAY,
    THERMOSTAT_SET_BACKLIT_BUTTONS,

    BUTTONARRAY_SET_DISABLED,
    BUTTONARRAY_SET_BACKLIT,
)

ConfigType = Dict[str, str]
_LOGGER = logging.getLogger(__name__)


def new_object(**kwargs):
    """Create new anonymous object."""
    return type("Object", (), kwargs)


class DeviceValue(object):
    """Device value interpretation object."""

    def __init__(
        self,
        device_type: Platform,
        inels_type: str,
        device_archetype: str,
        inels_value: str = None,
        ha_value: Any = None,
        last_value: Any = None,
    ) -> None:
        """initializing device info."""
        self.__inels_status_value = inels_value
        self.__inels_set_value: Any = None
        self.__ha_value = ha_value
        self.__device_type = device_type
        self.__inels_type = inels_type
        self.__device_archetype = device_archetype
        self.__last_value = last_value

        if self.__ha_value is None:
            self.__find_ha_value()

        if self.__inels_status_value is None:
            self.__find_inels_value()

    def __find_ha_value(self) -> None:
        """Find and create device value object."""

        # ha values are for home assistant to observe the state
        # inels set values are for enforcing commands
        # inels status values are what comes from the broker

        if self.__device_archetype == Archetype.RF.value:
            device_type = self.__device_type[0]
            if device_type is Platform.SWITCH:  # outlet switch
                if self.__inels_type is Element.RFSTI_11B:
                    state = int(  # defines state of relay
                        self.__trim_inels_status_values(DEVICE_TYPE_07_DATA, STATE, ""), 16
                    )

                    temp = (  # defines measured temperature (temp out)
                        int(
                            self.__trim_inels_status_values(
                                DEVICE_TYPE_07_DATA, TEMP_OUT, ""
                            ),
                            16,
                        )
                        / 100
                    )

                    self.__ha_value = new_object(on=(state == 1), temperature=temp)
                    # simplified the command to just on/off
                    self.__inels_set_value = SWITCH_WITH_TEMP_SET[self.__ha_value.on]
                else:
                    self.__ha_value = new_object(on=SWITCH_STATE[self.__inels_status_value])
                    self.__inels_set_value = SWITCH_SET[self.__ha_value.on]
            elif device_type is Platform.SENSOR:  # temperature sensor
                if self.__inels_type is Element.RFTI_10B:
                    hex_temp_in = self.__trim_inels_status_values(
                        DEVICE_TYPE_10_DATA, TEMP_IN, ""
                    )
                    hex_temp_out = self.__trim_inels_status_values(
                        DEVICE_TYPE_10_DATA, TEMP_OUT, ""
                    )
                    hex_battery = self.__trim_inels_status_values(
                        DEVICE_TYPE_10_DATA, BATTERY, ""
                    )
                    
                    temp_in = int(hex_temp_in, 16) / 100
                    temp_out = int(hex_temp_out, 16) / 100
                    battery_level = 100 if int(hex_battery, 16) == 0 else 0
                    
                    # interpretation of the values is done elsewhere.
                    # No output.
                    self.__ha_value = new_object(
                        temp_in=temp_in,
                        temp_out=temp_out,
                        battery=battery_level,
                    )
                elif self.__inels_type is Element.RFTC_10_G:
                    hex_temp = self.__trim_inels_status_values(
                        DEVICE_TYPE_12_DATA, TEMPERATURE, ""
                    )
                    hex_battery = self.__trim_inels_status_values(
                        DEVICE_TYPE_12_DATA, BATTERY, ""
                    )

                    temperature = int(hex_temp, 16) * 0.5
                    battery_level = (
                        0 if hex_battery == SENSOR_RFTC_10_G_LOW_BATTERY else 100
                    )

                    self.__ha_value = new_object(
                        temperature=temperature,
                        battery=battery_level,
                    )
                else:
                    self.__ha_value = self.__inels_status_value
            elif device_type is Platform.LIGHT:  # dimmer
                if self.__inels_type is Element.RFDAC_71B:
                    # value in percentage to present in HA
                    self.__ha_value = DEVICE_TYPE_05_HEX_VALUES[self.__inels_status_value]

                    # gets the hex values directly
                    trimmed_data = self.__trim_inels_status_values(
                        DEVICE_TYPE_05_DATA, Element.RFDAC_71B, " "
                    )

                    # simplified view of dimmer (sets brightness level)
                    self.__inels_set_value = (  # "01 ?? ??"" sets this value to internal state
                        f"{ANALOG_REGULATOR_SET_BYTES[Element.RFDAC_71B]} {trimmed_data}"
                    )
                else:
                    self.__ha_value = self.__inels_status_value
            elif device_type is Platform.COVER:  # Shutters
                ha_val = SHUTTER_STATES.get(self.__inels_status_value)

                # if the state is not obtained, grab last one (not sure why it wouldn't)
                self.__ha_value = ha_val if ha_val is not None else self.__last_value
                # give the new instruction (ex. 03 00 00 00)
                self.__inels_set_value = SHUTTER_SET[self.__ha_value]
            elif device_type is Platform.CLIMATE:  # thermovalve
                if self.__inels_type is Element.RFATV_2:
                    # fetches all the status values and compacts them into a new object
                    temp_current_hex = self.__trim_inels_status_values(
                        CLIMATE_TYPE_09_DATA, CURRENT_TEMP, ""
                    )
                    temp_current = int(temp_current_hex, 16) * 0.5
                    temp_required_hex = self.__trim_inels_status_values(
                        CLIMATE_TYPE_09_DATA, REQUIRED_TEMP, ""
                    )
                    temp_required = int(temp_required_hex, 16) * 0.5
                    battery_hex = self.__trim_inels_status_values(
                        CLIMATE_TYPE_09_DATA, BATTERY, ""
                    )
                    open_to_hex = self.__trim_inels_status_values(
                        CLIMATE_TYPE_09_DATA, OPEN_IN_PERCENTAGE, ""
                    )
                    open_to_percentage = int(open_to_hex, 16) * 0.5
                    batter = int(battery_hex, 16)
                    self.__ha_value = new_object(
                        battery=batter,
                        current=temp_current,
                        required=temp_required,
                        open_in_percentage=open_to_percentage,
                    )
                else:
                    self.__ha_value = self.__inels_status_value
            elif device_type is Platform.BUTTON:
                if self.__inels_type is Element.RFGB_40:
                    state = self.__trim_inels_status_values(BUTTON_TYPE_19_DATA, STATE, "")
                    state_hex_str = f"0x{state}"  # 0xSTATE
                    # interpret the value and write it in binary
                    state_bin_str = f"{int(state_hex_str, 16):0>8b}"

                    # read which button was last pressed
                    identity = self.__trim_inels_status_values(
                        BUTTON_TYPE_19_DATA, IDENTITY, ""
                    )

                    self.__ha_value = new_object(
                        number=BUTTON_NUMBER.get(identity),
                        battery=100 if state_bin_str[4] == "0" else 0,  # checking low battery state
                        pressing=state_bin_str[3] == "1",
                        changed=state_bin_str[2] == "1",
                        # reports the number of buttons
                        amount=BUTTON_DEVICE_AMOUNT.get(self.__inels_type),
                    )
        else: # BUS
            if self.__inels_type is Element.SA3_01B: # Switch
                state = int(self.__trim_inels_status_values(RELAY_DATA, STATE, ""), 16)
                temp = self.__trim_inels_status_values(RELAY_DATA, TEMP_IN, "")
                relay_overflow = int(self.__trim_inels_status_values(RELAY_DATA, RELAY_OVERFLOW, ""),16)
                self.__ha_value = new_object(
                    on=(state == 1),
                    temp_in=temp,
                    # may not be important, but could cause problems if ignored
                    relay_overflow=(relay_overflow == 1)
                )
                self.__inels_set_value = RELAY_SET[self.__ha_value.on]
            elif self.__inels_type is Element.DA3_22M: # Two channel dimmer
                temp = self.__trim_inels_status_values(TWOCHANNELDIMMER_DATA, TEMP_IN, "")

                state = self.__trim_inels_status_values(
                    TWOCHANNELDIMMER_DATA, Element.DA3_22M, "")
                state_hex_str = f"0x{state}"
                state_bin_str = f"{int(state_hex_str, 16):0>8b}"

                out1 = int(
                    self.__trim_inels_status_values(
                        TWOCHANNELDIMMER_DATA, DIM_OUT_1, ""
                    ), 16
                )

                out2 = int(
                    self.__trim_inels_status_values(
                        TWOCHANNELDIMMER_DATA, DIM_OUT_2, ""
                    ), 16
                )
                
                out = [
                    out1 if out1 <= 100 else 100,
                    out2 if out2 <= 100 else 100,
                ]
                self.__ha_value = new_object(
                    #May not be that interesting for HA
                    sw1=state_bin_str[0] == "0",
                    sw2=state_bin_str[1] == "0",

                    in1=state_bin_str[2] == "0",
                    in2=state_bin_str[3] == "0",

                    ovt_alert_1=state_bin_str[4] == "0",
                    ovt_alert_2=state_bin_str[5] == "0",

                    ovlo_alert_1=state_bin_str[6] == "0",
                    ovlo_alert_2=state_bin_str[7] == "0",

                    # This might be important
                    temp=temp,
                    
                    #generalization for multiple channel dimmers
                    out=out, # array
                    channel_number=2,
                )
                
                #_LOGGER.info("Logging dimmer ha value")
                #_LOGGER.info("out1: %d out2: %d", self.__ha_value.out[0], self.__ha_value.out[1])
                
                set_val = "00\n00\n00\n00\n"
                for i in range(self.__ha_value.channel_number):
                    set_val +=  f"{self.__ha_value.out[i]:02X}" + "\n"
                self.__inels_set_value = set_val
            elif self.__inels_type is Element.GTR3_50: # Thermostat
                digital_inputs = self.__trim_inels_status_values(THERMOSTAT_DATA, Element.GTR3_50.value, "")
                digital_inputs_hex_str = f"0x{digital_inputs}"
                digital_inputs_bin_str = f"{int(digital_inputs_hex_str, 16):0>8b}"

                temp = self.__trim_inels_status_values(THERMOSTAT_DATA, TEMP_IN, "")

                plusminus = self.__trim_inels_status_values(
                    THERMOSTAT_DATA, PLUS_MINUS_BUTTONS, "")
                plusminus = f"0x{plusminus}"
                plusminus = f"{int(plusminus, 16):0>8b}"

                #light_in = int(self.__trim_inels_status_values(
                #    THERMOSTAT_DATA, LIGHT_IN, ""), 16)/100
                light_in = self.__trim_inels_status_values(THERMOSTAT_DATA, LIGHT_IN, "")

                #ain = int(self.__trim_inels_status_values(
                #    THERMOSTAT_DATA, AIN, ""), 16)/100
                ain = self.__trim_inels_status_values(THERMOSTAT_DATA, AIN, "")

                #humidity = (int(self.__trim_inels_status_values(
                #    THERMOSTAT_DATA, HUMIDITY, ""), 16)/100)
                
                humidity = self.__trim_inels_status_values(THERMOSTAT_DATA, HUMIDITY, "")


                #dewpoint = (int(self.__trim_inels_status_values(
                #    THERMOSTAT_DATA, DEW_POINT, ""), 16)/100)
                dewpoint = self.__trim_inels_status_values(THERMOSTAT_DATA, DEW_POINT, "")


                self.ha_value = new_object(
                    # May not be important to notify HA of this
                    # digital inputs
                    din1=digital_inputs_bin_str[0] == "0",
                    din2=digital_inputs_bin_str[1] == "0",
                    sw1=digital_inputs_bin_str[2] == "0",
                    sw2=digital_inputs_bin_str[3] == "0",
                    sw3=digital_inputs_bin_str[4] == "0",
                    sw4=digital_inputs_bin_str[5] == "0",
                    sw5=digital_inputs_bin_str[6] == "0",
                    # plus minus
                    plus=plusminus[0] == "0",  # plus button
                    minus=plusminus[1] == "0",  # minus button
                    
                    # Actually important
                    # temperature
                    temp=temp,

                    light_in=light_in,

                    ain=ain,

                    humidity=humidity,

                    dewpoint=dewpoint,

                    # my addition
                    # backlit
                    backlit=False,
                )
            elif self.__inels_type is Element.GSB3_90SX: # Button array
                digital_inputs = self.__trim_inels_status_values(
                    BUTTONARRAY_DATA, Element.GSB3_90SX.value, "")
                digital_inputs = f"0x{digital_inputs}"
                digital_inputs = f"{int(digital_inputs, 16):0>8b}"

                temp = self.__trim_inels_status_values(
                    BUTTONARRAY_DATA, TEMP_IN, "")

                light_in = self.__trim_inels_status_values(
                    BUTTONARRAY_DATA, LIGHT_IN, "")

                ain = self.__trim_inels_status_values(
                    BUTTONARRAY_DATA, AIN, "")

                humidity = self.__trim_inels_status_values(
                    BUTTONARRAY_DATA, HUMIDITY, "")

                dewpoint = self.__trim_inels_status_values(
                    BUTTONARRAY_DATA, DEW_POINT, "")

                #TODO make output

                self.ha_value = new_object(
                    # may not be needed as it is overkill for HA
                    # digital inputs
                    sw1=digital_inputs[0] == "0",
                    sw2=digital_inputs[1] == "0",
                    sw3=digital_inputs[2] == "0",
                    sw4=digital_inputs[3] == "0",
                    sw5=digital_inputs[4] == "0",
                    sw6=digital_inputs[5] == "0",
                    sw7=digital_inputs[6] == "0",
                    sw8=digital_inputs[7] == "0",
                    sw9=digital_inputs[8] == "0",

                    dn1=digital_inputs[9] == "0",
                    dn2=digital_inputs[10] == "0",
                    proxi=digital_inputs[11] == "0",

                    # Actually important:
                    # temperature
                    temp=temp,

                    # light in
                    light_in=light_in,

                    # AIN
                    ain=ain,

                    # humidity
                    humidity=humidity,

                    # dewpoint
                    dewpoint=dewpoint,

                    # my own additions
                    # disabled
                    disabled=False,
                    # backlit
                    backlit=False,
                )
                # TODO make output
            else:
                self.__ha_value = self.__inels_status_value
                
    def __trim_inels_status_values(
        self, selector: "dict[str, Any]", fragment: str, jointer: str
    ) -> str:
        """Trim inels status from broker into the pure string."""
        data = self.__inels_status_value.split("\n")[:-1]

        selected = itemgetter(*selector[fragment])(data)
        return jointer.join(selected)

    # TODO investigate this part
    # essentially forms a set value from the ha value
    
    def __find_inels_value(self) -> None:
        """Find inels mqtt value for specific device."""
        if self.__device_archetype == Archetype.RF.value:
            device_type = self.__device_type[0]

            if device_type is Platform.SWITCH:
                if self.__inels_type == Element.RFSTI_11B:
                    self.__inels_set_value = SWITCH_WITH_TEMP_SET.get(self.__ha_value.on)
                else:
                    # just a shortcut for setting it
                    # basically set the status from the ha value
                    self.__inels_set_value = SWITCH_SET.get(self.__ha_value.on)
            elif device_type is Platform.LIGHT:
                if self.__inels_type is Element.RFDAC_71B:
                    self.__inels_status_value = self.__find_keys_by_value(
                        DEVICE_TYPE_05_HEX_VALUES,  # str -> int
                        round(self.__ha_value, -1),
                        self.__last_value,
                    )
                    trimmed_data = self.__trim_inels_status_values(
                        DEVICE_TYPE_05_DATA, Element.RFDAC_71B, " "
                    )
                    self.__inels_set_value = (  # 01 00 00
                        f"{ANALOG_REGULATOR_SET_BYTES[Element.RFDAC_71B]} {trimmed_data}"
                    )
                    self.__ha_value = DEVICE_TYPE_05_HEX_VALUES[self.__inels_status_value]
            elif device_type is Platform.COVER:
                if self.__inels_type is Element.RFJA_12:
                    self.__inels_status_value = self.__find_keys_by_value(
                        SHUTTER_STATES,  # str -> str
                        self.__ha_value,
                        self.__last_value
                    )
                    self.__inels_set_value = SHUTTER_SET.get(self.__ha_value)
                    # special behavior. We need to find right HA state for the cover
                    prev_val = SHUTTER_STATES.get(self.__inels_status_value)
                    ha_val = (
                        self.__ha_value
                        if self.__ha_value in SHUTTER_STATE_LIST
                        else prev_val
                    )
                    self.__ha_value = ha_val
            elif device_type is Platform.CLIMATE:
                if self.__inels_type is Element.RFATV_2:
                    required_temp = int(round(self.__ha_value.required * 2, 0))
                    self.__inels_set_value = f"00 {required_temp:x} 00".upper()
            elif device_type is Platform.BUTTON:
                self.__ha_value = ha_val
        else:
            if self.__inels_type is Element.SA3_01B:
                self.__inels_set_value = RELAY_SET.get(self.__ha_value.on)
            elif self.__inels_type is Element.DA3_22M:
                # correct the values
                out1 = round(self.__ha_value.out[0], -1)
                out1 = out1 if out1 < 100 else 100

                out2 = round(self.__ha_value.out[1], -1)
                out2 = out2 if out2 < 100 else 100

                out1_str = f"{out1:02X}" + "\n"
                out2_str = f"{out2:02X}" + "\n"

                # EX: 00\n00\n00\n00\n64\n64\n # 100%/100%
                self.__inels_set_value = "".join(["00\n" * 4, out1_str, out2_str])
                #TODO fix __inels_status_value through the rounding
            elif self.__inels_type is Element.GTR3_50:
                # basically depending on the context of the functioning color the buttons
                backlit_display = THERMOSTAT_SET_BACKLIT_DISPLAY[self.__ha_value.backlit]
                backlit_buttons = THERMOSTAT_SET_BACKLIT_BUTTONS[self.__ha_value.backlit]
                self.__inels_set_value = "".join([
                    "00\n"*3, backlit_display, "00\n"*7, backlit_buttons, "00\n" * 3])
            elif self.__inels_type is Element.GSB3_90SX:
                disabled = BUTTONARRAY_SET_DISABLED[self.__ha_value.disabled]
                backlit = BUTTONARRAY_SET_BACKLIT[self.__ha_value.backlit]

                self.__inels_set_value = "".join(["00\n" * 36, disabled, backlit])
            else:
                self.__ha_value = ha_val #TODO is this right?

    def __find_keys_by_value(self, array: dict, value, last_value) -> Any:
        """Return key from dict by value

        Args:
            array (dict): dictionary where should I have to search
            value Any: by this value I'm goning to find key
        Returns:
            Any: value of the dict key
        """
        keys = list(array.keys())
        vals = list(array.values())
        try:
            index = vals.index(value)
            return keys[index]
        except ValueError as err:
            index = vals.index(last_value)
            _LOGGER.warning(
                "Value %s is not in list of %s. Stack %s", value, array, err
            )

        return keys[index]

    @property
    def ha_value(self) -> Any:
        """Converted value from inels mqtt broker into
           the HA format

        Returns:
            Any: object to corespond to HA device
        """
        return self.__ha_value

    @property
    def inels_status_value(self) -> str:
        """Raw inels value from mqtt broker

        Returns:
            str: quated string from mqtt broker
        """
        return self.__inels_status_value

    @property
    def inels_set_value(self) -> str:
        """Raw inels value for mqtt broker

        Returns:
            str: this is string format value for mqtt broker
        """
        return self.__inels_set_value


def get_value(status: GetMessageType, platform: str) -> Any:
    """Get value from pyload message."""
    if platform == Platform.SWITCH:
        return SWITCH_STATE[status]

    return None


def get_state_topic(cfg: ConfigType) -> str:
    """Get state topic."""
    return cfg["DDD"]


def get_set_topic(cfg: ConfigType) -> str:
    """Get set topic."""
    return cfg["OOO"]


def get_name(cfg: ConfigType) -> str:
    """Get name of the entity."""
    return cfg["Name"]
