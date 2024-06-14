"""Utility classes."""
from __future__ import annotations
from dataclasses import dataclass
import logging
import json
import re

from operator import itemgetter
from typing import Any, Dict, Optional, Tuple

from .const import (
    ADC3_60M_DATA,
    ANALOG_REGULATOR_SET_BYTES,
    BATTERY,
    BLUE,
    CARD_DATA,
    CARD_ID,
    DAC3_04_DATA,
    DALI_DMX_UNIT,
    DALI_DMX_UNIT_2,
    DALI_DMX_UNIT_DATA,
    DCDA_33M_DATA,
    DEVICE_TYPE_02_COMM_TEST,
    DEVICE_TYPE_06_DATA,
    DEVICE_TYPE_09_DATA,
    COVER,
    CURRENT_TEMP,
    DEVICE_TYPE_02_DATA,
    DEVICE_TYPE_03_COMM_TEST,
    DEVICE_TYPE_03_DATA,
    DEVICE_TYPE_05_COMM_TEST,
    DEVICE_TYPE_05_DATA,
    DEVICE_TYPE_05_HEX_VALUES,
    DEVICE_TYPE_13_COMM_TEST,
    DEVICE_TYPE_13_DATA,
    DEVICE_TYPE_15_DATA,
    DEVICE_TYPE_16_DATA,
    DEVICE_TYPE_19_DATA,
    BUTTON_DEVICE_AMOUNT,
    BUTTON_NUMBER,
    DEVICE_TYPE_07_DATA,
    DEVICE_TYPE_10_DATA,
    DEVICE_TYPE_12_DATA,
    DEVICE_TYPE_21_DATA,
    DEVICE_TYPE_29_DATA,
    GLASS_CONTROLLER_DATA,
    GREEN,
    IOU3_108M_DATA,
    JA3_018M,
    JA3_018M_DATA,
    JA3_014M,
    JA3_014M_DATA,
    POSITION,
    RED,
    REQUIRED_TEMP,
    RF_2_BUTTON_CONTROLLER,
    RF_DETECTOR,
    RF_DIMMER_RGB,
    RF_FLOOD_DETECTOR,
    RF_LIGHT_BULB,
    RF_MOTION_DETECTOR,
    RF_SHUTTER_STATE_SET,
    RF_DIMMER,
    LIGHT,
    RF_SHUTTER_UNIT,
    RF_SINGLE_DIMMER,
    RF_SINGLE_SWITCH,
    RF_SWITCHING_UNIT,
    RF_TEMPERATURE_HUMIDITY_SENSOR,
    RF_THERMOSTAT,
    SENSOR,
    RF_SHUTTERS,
    RF_WIRELESS_THERMOVALVE,
    RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR,
    SHUTTER_SET,
    SHUTTER_STATE_LIST,
    SHUTTER_STATES,
    SIMPLE_SHUTTER_STATE_SET,
    SWITCH,
    SWITCH_SET,
    SWITCH_STATE,
    RF_TEMPERATURE_INPUT,
    CLIMATE,
    OPEN_IN_PERCENTAGE,
    RF_CONTROLLER,
    BUTTON,
    STATE,
    IDENTITY,
    SWITCH_WITH_TEMP_SET,
    TEMP_OUT,
    CRITICAL_MAX_TEMP,
    REQUIRED_HEAT_TEMP,
    MAX_TEMP,
    CRITICAL_MIN_TEMP,
    REQUIRED_COOL_TEMP,
    TEMP_CORRECTION,
    PUBLIC_HOLIDAY,
    CONTROL_MODE,
    VIRT_CONTR,

    SA3_01B,
    DA3_22M,
    GRT3_50,
    GSB3_90SX,
    SA3_04M,
    SA3_012M,
    SA3_014M,
    IM3_80B,
    IM3_140M,
    WHITE,
    WSB3_20H,
    GSB3_60SX,
    IDRT3_1,
    ADC3_60M,
    DA3_66M,
    DAC3_04B,
    DAC3_04M,
    DCDA_33M,
    DMD3_1,
    FA3_612M,
    GBP3_60,
    GCH3_31,
    GCR3_11,
    GDB3_10,
    GSB3_20SX,
    GSB3_40SX,
    GSP3_100,
    IM3_20B,
    IM3_40B,
    IOU3_108M,
    SA3_02B,
    SA3_02M,
    SA3_06M,
    SA3_022M,
    TI3_10B,
    TI3_40B,
    TI3_60M,
    WSB3_20,
    WSB3_20H,
    WSB3_40,
    WSB3_40H,
    RC3_610DALI,
    #VIRT_CONTR,
    VIRT_HEAT_REG,
    VIRT_COOL_REG,

    SA3_01B_DATA,
    DA3_22M_DATA,
    GRT3_50_DATA,
    GSB3_90SX_DATA,
    SA3_04M_DATA,
    SA3_012M_DATA,
    SA3_014M_DATA,
    IM3_80B_DATA,
    IM3_140M_DATA,
    DEVICE_TYPE_124_DATA,
    IDRT3_1_DATA,
    DEVICE_TYPE_166_DATA,
    VIRT_REG_DATA,
    DA3_66M_DATA,
    SA3_02B_DATA,
    SA3_02M_DATA,
    SA3_04M_DATA,
    SA3_06M_DATA,
    SA3_022M_DATA,
    IM3_240B_DATA,
    WSB3_240_DATA,
    WSB3_240HUM_DATA,
    DMD3_1_DATA,
    GSB3_DATA,
    RC3_610DALI_DATA,
    FA3_612M_DATA,

    RELAY,
    RELAY_OVERFLOW,
    TEMP_IN,
    DIM_OUT_1,
    DIM_OUT_2,
    PLUS_MINUS_BUTTONS,
    LIGHT_IN,
    AIN,
    HUMIDITY,
    DEW_POINT,
    SW,
    DIN,
    OUT,
    IN,
    ALERT,
    SHUTTER,
    VALVE,
    AOUT,
    DALI,

    RELAY_SET,

    BUTTONARRAY_SET_DISABLED,
    BUTTONARRAY_SET_BACKLIT,

    IM3_AMOUNTS,
    WSB3_AMOUNTS,
    GSB3_AMOUNTS,

    INELS_DEVICE_TYPE_DATA_STRUCT_DATA,

    DEVICE_TYPE_07_COMM_TEST,
    Shutter_state,
    Climate_action,
    Climate_modes,

    BITS,
    INTEGERS,
    NUMBER,
)

#bit
@dataclass
class Bit():
    is_on: bool
    addr: str

#number
@dataclass
class Number():
    value: int
    addr: str

#relay
@dataclass
class SimpleRelay():
    """Create simple relay"""
    is_on: bool

    # def toggle(self) -> bool:
    #     """Return the opposite of the current state without changing it."""
    #     # f"{(2 - (device_value.ha_value.simple_relay[0].is_on * 1)):02X}\n00\n00\n"
    #     mqtt_data = {
    #         True: 1,
    #         False: 2
    #     }
    #     return mqtt_data[not self.is_on]

@dataclass
class Relay(SimpleRelay):
    """Create relay with overflow detection."""
    overflow: bool

#shutters
@dataclass
class Shutter():
    """Create a simple shutter."""
    state: Shutter_state
    is_closed: Optional[bool]

@dataclass
class Shutter_pos(Shutter):
    """Create a shutter with position."""
    position: int
    set_pos: bool

#lights
@dataclass
class SimpleLight():
    brightness: int

@dataclass
class LightCoaToa(SimpleLight):
    toa: bool
    coa: bool

@dataclass
class RGBLight(SimpleLight):
    r: int
    g: int
    b: int

@dataclass
class AOUTLight(SimpleLight):
    aout_coa: bool

@dataclass
class WarmLight(SimpleLight):
    relative_ct: int

@dataclass
class DALILight(SimpleLight):
    alert_dali_communication: bool
    alert_dali_power: bool

ConfigType = Dict[str, str]
_LOGGER = logging.getLogger(__name__)

# To prevent the value as being none,
# if anything goes wrong when calculating the value,
# we give an empty object that will simply not match with any keywords
# it is filtered out in set_val
dummy_val = object()

def new_object(**kwargs):
    """Create new anonymous object."""
    return type("Object", (), kwargs)

def break_into_bytes(line: str):
    if len(line)%2 == 0:
        return [line[i:i+2] for i in range(0, len(line), 2)]
    return []

def xparse_formated_json(data):
    regex = r"state\":\{(.*)\}\}"
    match = re.search(regex, data)
    addr_val_list = []
    if match != None:
        states = match.group(1)
        addr_value_pair_list = states.split(',')
        for item in addr_value_pair_list:
            addr, val = item.split(':')
            addr_val_list.append(
                (addr, int(val))
            )
    return addr_val_list

def parse_formated_json(data):
    addr_val_list = []
    data = json.loads(data)
    for addr, val in data['state'].items():
        addr_val_list.append(
            (addr, val)
        )
    return addr_val_list


@dataclass
class Bit:
    is_on: bool
    addr: str

@dataclass
class Number:
    value: int
    addr: str

# ... (other dataclasses)

class HAValueHandler:
    @staticmethod
    def update_ha_value(device_value: DeviceValue) -> None:
        """Update the HA value based on the device's status."""
        pass

class InelsValueHandler:
    @staticmethod
    def update_inels_value(device_value: DeviceValue) -> None:
        """Update the Inels command value based on the desired HA state."""
        pass

class SwitchHAHandler(HAValueHandler):
    @staticmethod
    def update_ha_value(device_value: DeviceValue) -> None:
        if device_value.inels_type == RF_SINGLE_SWITCH:
            SwitchHAHandler.__handle_rf_single_switch(device_value)
        elif device_value.inels_type == RF_SWITCHING_UNIT:
            SwitchHAHandler.__handle_rf_switching_unit(device_value)
        elif device_value.inels_type == RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR:
            SwitchHAHandler.__handle_rf_switching_unit_with_external_temperature_sensor(device_value)
        elif device_value.inels_type == SA3_01B:
            SwitchHAHandler.__handle_sa3_01b(device_value)
        elif device_value.inels_type == SA3_02B:
            SwitchHAHandler.__handle_sa3_02b(device_value)
        elif device_value.inels_type == SA3_02M:
            SwitchHAHandler.__handle_sa3_02m(device_value)
        elif device_value.inels_type == SA3_04M:
            SwitchHAHandler.__handle_sa3_04m(device_value)
        elif device_value.inels_type == SA3_06M:
            SwitchHAHandler.__handle_sa3_06m(device_value)
        elif device_value.inels_type == SA3_012M:
            SwitchHAHandler.__handle_sa3_012m(device_value)
        elif device_value.inels_type == SA3_014M:
            SwitchHAHandler.__handle_sa3_014m(device_value)
        elif device_value.inels_type == SA3_022M:
            SwitchHAHandler.__handle_sa3_022m(device_value)
        elif device_value.inels_type == IOU3_108M:
            SwitchHAHandler.__handle_iou3_108m(device_value)
        elif device_value.inels_type == RC3_610DALI:
            SwitchHAHandler.__handle_rc3_610dali(device_value)
        elif device_value.inels_type == FA3_612M:
            SwitchHAHandler.__handle_fa3_612m(device_value)
        elif device_value.inels_type in [GCR3_11, GCH3_31]:
            SwitchHAHandler.__handle_gcr3_11_gch3_31(device_value)
        elif device_value.inels_type == BITS:
            SwitchHAHandler.__handle_bits(device_value)
        else:
            _LOGGER.warning(f"Unsupported inels_type: {device_value.inels_type}")

    @staticmethod
    def __handle_rf_single_switch(device_value: DeviceValue) -> None:
        if device_value.inels_status_value is None:
            _LOGGER.info("inels_status_value was 'None' for %s", RF_SINGLE_SWITCH)
            device_value.inels_set_value = DEVICE_TYPE_07_COMM_TEST
            device_value.ha_value = None
        else:
            simple_relay: list[SimpleRelay] = []
            simple_relay.append(
                SimpleRelay(
                    is_on=int(device_value.trim_inels_status_values(DEVICE_TYPE_02_DATA, RELAY, ""), 16) != 0
                )
            )

            device_value.ha_value = new_object(
                simple_relay=simple_relay,
            )

            device_value.inels_set_value = f"{(2 - (device_value.ha_value.simple_relay[0].is_on)):02X}\n00\n"

    @staticmethod
    def __handle_rf_switching_unit(device_value: DeviceValue) -> None:
        if device_value.inels_status_value is None:
            _LOGGER.info("inels_status_value was 'None' for %s", RF_SWITCHING_UNIT)
            device_value.inels_set_value = DEVICE_TYPE_02_COMM_TEST
            device_value.ha_value = None
        else:
            simple_relay: list[SimpleRelay] = []
            simple_relay.append(
                SimpleRelay(
                    is_on=int(device_value.trim_inels_status_values(DEVICE_TYPE_02_DATA, RELAY, ""), 16) != 0
                )
            )

            device_value.ha_value = new_object(
                simple_relay=simple_relay,
            )

            device_value.inels_set_value = f"{(2 - (device_value.ha_value.simple_relay[0].is_on * 1)):02X}\n00\n00\n"

    @staticmethod
    def __handle_rf_switching_unit_with_external_temperature_sensor(device_value: DeviceValue) -> None:
        if device_value.inels_status_value is None:
            _LOGGER.info("inels_status_value was 'None' for %s", RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR)
            device_value.inels_set_value = DEVICE_TYPE_07_COMM_TEST
            device_value.ha_value = None
        else:
            simple_relay: list[SimpleRelay] = []
            simple_relay.append(
                SimpleRelay(
                    is_on=int(device_value.trim_inels_status_values(DEVICE_TYPE_07_DATA, RELAY, ""), 16) != 0
                )
            )
            temp = device_value.trim_inels_status_values(DEVICE_TYPE_07_DATA, TEMP_OUT, "")

            device_value.ha_value = new_object(
                simple_relay=simple_relay,
                temp_out=temp,
            )
            device_value.inels_set_value = SWITCH_WITH_TEMP_SET[device_value.ha_value.simple_relay[0].is_on]

    @staticmethod
    def __handle_sa3_01b(device_value: DeviceValue) -> None:
        re = []
        re.append(int(device_value.trim_inels_status_values(SA3_01B_DATA, RELAY, ""), 16) & 1 != 0)

        temp = device_value.trim_inels_status_values(SA3_01B_DATA, TEMP_IN, "")

        relay_overflow = []
        relay_overflow.append(int(device_value.trim_inels_status_values(SA3_01B_DATA, RELAY_OVERFLOW, ""),16) == 1)

        relay: list[Relay] = []
        for i in range(len(re)):
            relay.append(
                Relay(
                    is_on=re[i],
                    overflow=relay_overflow[i],
                )
            )

        device_value.ha_value = new_object(
            #re=re,
            temp_in=temp,
            #relay_overflow=relay_overflow

            relay=relay
        )
        device_value.inels_set_value = RELAY_SET[device_value.ha_value.relay[0].is_on]

    @staticmethod
    def __handle_sa3_02b(device_value: DeviceValue) -> None:
        simple_relay: list[SimpleRelay] = []
        for relay in device_value.trim_inels_status_bytes(SA3_02B_DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

        temp_in = device_value.trim_inels_status_values(SA3_02B_DATA, TEMP_IN, "")
        device_value.ha_value = new_object(
            simple_relay=simple_relay,
            temp_in=temp_in,
        )

        set_val = ""
        for r in simple_relay:
            set_val += "07\n" if r.is_on else "06\n"
        device_value.inels_set_value=set_val

    @staticmethod
    def __handle_sa3_02m(device_value: DeviceValue) -> None:
        simple_relay: list[SimpleRelay] = []
        for relay in device_value.trim_inels_status_bytes(SA3_02M_DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

        digital_inputs = device_value.trim_inels_status_values(
            SA3_02M_DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"
        sw = []
        for i in range(2):
            sw.append(digital_inputs[7 - i] == "1")

        device_value.ha_value = new_object(
            simple_relay=simple_relay,
            sw=sw,
        )

        set_val = ""
        for r in simple_relay:
            set_val += "07\n" if r else "06\n"
        device_value.inels_set_value=set_val

    @staticmethod
    def __handle_sa3_04m(device_value: DeviceValue) -> None:
        simple_relay: list[SimpleRelay] = []
        for relay in device_value.trim_inels_status_bytes(SA3_04M_DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

        digital_inputs = device_value.trim_inels_status_values(
            SA3_04M_DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"
        sw = []
        for i in range(4):
            sw.append(digital_inputs[7 - i] == "1")

        device_value.ha_value = new_object(
            simple_relay=simple_relay,
            sw=sw,
        )

        set_val = ""
        for r in simple_relay:
            set_val += "07\n" if r.is_on else "06\n"
        device_value.inels_set_value=set_val

    @staticmethod
    def __handle_sa3_06m(device_value: DeviceValue) -> None:
        simple_relay: list[SimpleRelay] = []
        for relay in device_value.trim_inels_status_bytes(SA3_06M_DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

        digital_inputs = device_value.trim_inels_status_values(
            SA3_06M_DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"
        sw = []
        for i in range(6):
            sw.append(digital_inputs[7 - i] == "1")

        device_value.ha_value = new_object(
            simple_relay=simple_relay,
            sw=sw,
        )

        set_val = ""
        for r in simple_relay:
            set_val += "07\n" if r.is_on else "06\n"
        device_value.inels_set_value=set_val

    @staticmethod
    def __handle_sa3_012m(device_value: DeviceValue) -> None:
        simple_relay: list[SimpleRelay] = []
        for relay in device_value.trim_inels_status_bytes(SA3_012M_DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

        digital_inputs = device_value.trim_inels_status_values(
            SA3_012M_DATA, SA3_012M, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"

        sw=[]
        for i in range(8):
            sw.append(digital_inputs[7 - i] == "1")
        for i in range(4):
            sw.append(digital_inputs[15 - i] == "1")

        device_value.ha_value = new_object(
            simple_relay=simple_relay,
            sw=sw,
        )
        set_val = ""
        for r in simple_relay:
            set_val += "07\n" if r.is_on else "06\n"
        device_value.inels_set_value=set_val

    @staticmethod
    def __handle_sa3_014m(device_value: DeviceValue) -> None:
        simple_relay: list[SimpleRelay] = []
        for relay in device_value.trim_inels_status_bytes(SA3_014M_DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

        digital_inputs = device_value.trim_inels_status_values(
            SA3_014M_DATA, SA3_014M, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"

        sw = []
        for i in range(8):
            sw.append(digital_inputs[7 - i] == "1")
        for i in range(6):
            sw.append(digital_inputs[13 - i] == "1")

        device_value.ha_value = new_object(
            simple_relay=simple_relay,
            sw=sw,
        )
        set_val = ""
        for r in simple_relay:
            set_val += "07\n" if r.is_on else "06\n"
        device_value.inels_set_value = set_val

    @staticmethod
    def __handle_sa3_022m(device_value: DeviceValue) -> None:
        re=[]
        for relay in device_value.trim_inels_status_bytes(SA3_022M_DATA, RELAY):
            re.append((int(relay, 16) & 1) != 0)

        overflows=[]
        alerts = device_value.trim_inels_status_values(
            SA3_022M_DATA, RELAY_OVERFLOW, ""
        )
        alerts = f"0x{alerts}"
        alerts = f"{int(alerts, 16):0>16b}"
        for i in range(8): #0-7
            overflows.append(alerts[7-i] == "1")
        for i in range(8): #8-15
            overflows.append(alerts[15-i] == "1")

        digital_inputs = device_value.trim_inels_status_values(
            SA3_012M_DATA, SA3_012M, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"

        sw=[]
        for i in range(8):
            sw.append(digital_inputs[7 - i] == "1")
        for i in range(8):
            sw.append(digital_inputs[15 - i] == "1")

        relay: list[Relay] = []
        for i in range(len(re)):
            relay.append(
                Relay(
                    is_on=re[i],
                    overflow=overflows[i]
                )
            )

        shutter=[]
        for s in device_value.trim_inels_status_bytes(SA3_022M_DATA, SHUTTER):
            shutter.append((int(s, 16) & 1) != 0)

        simple_shutters = []
        shutters = list(zip(shutter[::2], shutter[1::2]))
        for s in shutters:
            if s[0]:
                state = Shutter_state.Open
            elif s[1]:
                state = Shutter_state.Closed
            else:
                state = Shutter_state.Stop_down
            simple_shutters.append(
                Shutter(
                    state=state,
                    is_closed=None
                )
            )

        valve=[]
        for v in device_value.trim_inels_status_bytes(SA3_022M_DATA, VALVE):
            valve.append((int(v, 16) & 1) != 0)

        device_value.ha_value = new_object(
            relay=relay,
            shutter_motors=shutter,
            simple_shutters=simple_shutters,
            valve=valve,
            sw=sw,
        )

        set_val = ""
        for r in device_value.ha_value.relay:
            set_val += RELAY_SET[r.is_on]
        # for s in self.ha_value.shutter_motors:
        #     set_val += RELAY_SET[s]
        for s in device_value.ha_value.simple_shutters:
            set_val += SIMPLE_SHUTTER_STATE_SET[s.state]
        for v in device_value.ha_value.valve:
            set_val += RELAY_SET[v]

        device_value.inels_set_value = set_val

    @staticmethod
    def __handle_iou3_108m(device_value: DeviceValue) -> None:
        re=[]
        for relay in device_value.trim_inels_status_bytes(IOU3_108M_DATA, RELAY):
            re.append((int(relay, 16) & 1) != 0)

        temps = device_value.trim_inels_status_values(IOU3_108M_DATA, TEMP_IN)
        temps = [temps[0:4], temps[4:8]]

        digital_inputs = device_value.trim_inels_status_values(
            IOU3_108M_DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        din = []
        for i in range(8):
            din.append(digital_inputs[7-i] == '1')

        digital_inputs = device_value.trim_inels_status_values(
            IOU3_108M_DATA, RELAY_OVERFLOW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        relay_overflow = []
        for i in range(8):
            relay_overflow.append(digital_inputs[7-1] == '1')

        relay: list[Relay] = []
        for i in range(8):
            relay.append(
                Relay(
                    is_on=re[i],
                    overflow=relay_overflow[i],
                )
            )

        device_value.ha_value = new_object(
            relay=relay,
            #re=re,
            temps=temps,
            din=din,
            #relay_overflow=relay_overflow,
        )

    @staticmethod
    def __handle_rc3_610dali(device_value: DeviceValue) -> None:
        #aout
        aout_brightness=[]
        for a in device_value.trim_inels_status_bytes(RC3_610DALI_DATA, AOUT):
            aout_brightness.append(int(a, 16))

        #relays
        re=[]
        for relay in device_value.trim_inels_status_bytes(RC3_610DALI_DATA, RELAY):
            re.append((int(relay, 16) & 1) != 0)

        #temperatures
        temps = []
        temp_bytes = device_value.trim_inels_status_bytes(
            RC3_610DALI_DATA,
            TEMP_IN,
        )
        for i in range(int(len(temp_bytes)/2)):
            temps.append(temp_bytes[2*i] + temp_bytes[2*i+1])

        #digital inputs
        din=[]
        digital_inputs = device_value.trim_inels_status_values(
            RC3_610DALI_DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        for i in range(6):
            din.append(digital_inputs[7-i] == "1")

        relay_overflow=[]
        overflows = device_value.trim_inels_status_values(
            RC3_610DALI_DATA, RELAY_OVERFLOW, "")
        overflows = f"0x{overflows}"
        overflows = f"{int(overflows, 16):0>8b}"
        for i in range(len(re)):
            relay_overflow.append(overflows[7-i] == "1")

        relay: list[Relay] = []
        for i in range(len(re)):
            relay.append(
                Relay(
                    is_on=re[i],
                    overflow=relay_overflow[i],
                )
            )

        sync_error = []
        aout_coa = []
        alerts = device_value.trim_inels_status_values(
            RC3_610DALI_DATA, ALERT, "")
        alerts = f"0x{alerts}"
        alerts = f"{int(alerts, 16):0>8b}"

        for i in range(4):
            sync_error.append(alerts[7-i] == "1")
        for i in range(4, 6):
            aout_coa.append(alerts[7-i] == "1")


        aout=[]
        for i in range(2):
            aout.append(
                AOUTLight(
                    brightness=aout_brightness[i],
                    aout_coa=aout_coa[i]
                )
            )

        alert_dali_power = alerts[1] == "1"
        alert_dali_communication = alerts[0] == "1"

        dali_raw = device_value.trim_inels_status_bytes(
            RC3_610DALI_DATA, DALI)
        dali = []
        for d in dali_raw:
            dali.append(
                DALILight(
                    brightness=int(d, 16),
                    alert_dali_communication=alert_dali_communication,
                    alert_dali_power=alert_dali_power,
                )
            )

        device_value.ha_value = new_object(
            relay=relay,
            temps=temps,
            din=din,
            aout=aout,
            dali=dali,
        )

    @staticmethod
    def __handle_fa3_612m(device_value: DeviceValue) -> None:
        inputs = device_value.trim_inels_status_values(FA3_612M_DATA, FA3_612M, "")
        inputs = f"0x{inputs}"
        inputs = f"{int(inputs, 16):0>24b}"

        din = []
        for i in range(3):
            din.append(inputs[7-i] == "1")

        aout_coa = []
        for i in range(4, 8):
            aout_coa.append(inputs[7 - i] == "1")

        sw = []
        for i in range(8):
            sw.append(inputs[15-i] == "1")

        roa = []
        for i in range(3):
            roa.append(inputs[23 - i] == "1")

        sw.append(inputs[23 - 3] == "1")

        overflows = device_value.trim_inels_status_values(FA3_612M_DATA, RELAY_OVERFLOW, "")
        overflows = f"0x{overflows}"
        overflows = f"{int(overflows, 16):0>8b}"

        #relay_overflow = []
        #for i in range(8):
        #    relay_overflow.append(overflows[7-i] == "1")

        i=0
        aout=[]
        for a in device_value.trim_inels_status_bytes(FA3_612M_DATA, AOUT):
            aout.append(
                AOUTLight(
                    brightness=int(a, 16),
                    aout_coa=aout_coa[i],
                )
            )
            i = i + 1

        re=[]
        for relay in device_value.trim_inels_status_bytes(FA3_612M_DATA, RELAY):
            re.append((int(relay, 16) & 1) != 0)

        valves = [[re[0], re[1]], [re[2], re[3]]]
        fan_speed = 0
        if re[6]: #speed 3
            fan_speed = 3
        elif re[5]: #speed 2
            fan_speed = 2
        elif re[4]: #speed 1
            fan_speed = 1

        heating_out = re[7]

        ains=[]
        ain_bytes = device_value.trim_inels_status_bytes(
            FA3_612M_DATA,
            AIN,
        )
        for i in range(int(len(ain_bytes)/4)):
            ains.append(ain_bytes[4*i] + ain_bytes[4*i+1] + ain_bytes[4*i+2] + ain_bytes[4*i+3])

        last_status_val=device_value.inels_status_value

        device_value.ha_value = new_object(
            din=din,
            sw=sw,
            aout=aout,
            valves=valves,
            fan_speed=fan_speed,
            heating_out=heating_out,
            ains=ains,
            last_status_val=last_status_val,
        )

    @staticmethod
    def __handle_gcr3_11_gch3_31(device_value: DeviceValue) -> None:
        state = device_value.trim_inels_status_values(CARD_DATA, STATE, "")
        state = f"0x{state}"
        state = f"{int(state, 16):0>16b}"

        simple_relay: list[SimpleRelay] = []
        simple_relay.append(SimpleRelay(is_on=state[5] == "1"))

        card_present = (state[4] == "1")

        card_id = device_value.trim_inels_status_values(CARD_DATA, CARD_ID, "")
        card_id_int = int(card_id, 16)
        #if card removed before
        if card_id_int == 0 and device_value.last_value is not None:
            card_id = device_value.last_value.card_id

        interface = [
            state[0] == "1",
            state[12] == "1",
            state[10] == "1"
        ]

        light_in = device_value.trim_inels_status_values(CARD_DATA, LIGHT_IN, "")

        temp_in = device_value.trim_inels_status_values(CARD_DATA, TEMP_IN, "")
        device_value.ha_value = new_object(
            simple_relay=simple_relay,
            interface=interface,
            temp_in=temp_in,
            card_present=card_present,
            card_id=card_id,
        )

    @staticmethod
    def __handle_bits(device_value: DeviceValue) -> None:
        bit: list[Bit] = []
        for addr, val in parse_formated_json(device_value.inels_status_value):
            bit.append(
                Bit(
                    is_on=val, addr=addr
                )
            )

        device_value.ha_value = new_object(
            bit=bit,
        )

        set_val = {}
        for bit in device_value.ha_value.bit:
            set_val[bit.addr] = bit.is_on

        device_value.inels_set_value = json.dumps({"cmd": set_val})


class NumberHAHandler(HAValueHandler):
    @staticmethod
    def update_ha_value(device_value: DeviceValue) -> None:
        if device_value.inels_type == NUMBER:
            NumberHAHandler.__handle_number(device_value)
        else:
            _LOGGER.warning(f"Unsupported inels_type: {device_value.inels_type}")

    @staticmethod
    def __handle_number(device_value: DeviceValue) -> None:
        number: list[Number] = []
        for addr, val in parse_formated_json(device_value.inels_status_value):
            number.append(
                Number(
                    value=val, addr=addr
                )
            )

        device_value.ha_value = new_object(
            number=number,
        )

        set_val = {}
        for number in device_value.ha_value.number:
            set_val[number.addr] = number.value

        device_value.inels_set_value = json.dumps({"cmd": set_val})

class SensorHAHandler(HAValueHandler):
    @staticmethod
    def update_ha_value(device_value: DeviceValue) -> None:
        if device_value.inels_type == RF_TEMPERATURE_INPUT:
            SensorHAHandler.__handle_rf_temperature_input(device_value)
        elif device_value.inels_type == RF_THERMOSTAT:
            SensorHAHandler.__handle_rf_thermostat(device_value)
        elif device_value.inels_type == RF_FLOOD_DETECTOR:
            SensorHAHandler.__handle_rf_flood_detector(device_value)
        elif device_value.inels_type == RF_DETECTOR:
            SensorHAHandler.__handle_rf_detector(device_value)
        elif device_value.inels_type == RF_MOTION_DETECTOR:
            SensorHAHandler.__handle_rf_motion_detector(device_value)
        elif device_value.inels_type == RF_TEMPERATURE_HUMIDITY_SENSOR:
            SensorHAHandler.__handle_rf_temperature_humidity_sensor(device_value)
        elif device_value.inels_type == GRT3_50:
            SensorHAHandler.__handle_grt3_50(device_value)
        elif device_value.inels_type == WSB3_20 or device_value.inels_type == WSB3_40:
            SensorHAHandler.__handle_wsb3_20_40(device_value)
        elif device_value.inels_type == WSB3_20H or device_value.inels_type == WSB3_40H:
            SensorHAHandler.__handle_wsb3_20h_40h(device_value)
        elif device_value.inels_type == IM3_20B or device_value.inels_type == IM3_40B:
            SensorHAHandler.__handle_im3_20b_40b(device_value)
        elif device_value.inels_type == IM3_80B:
            SensorHAHandler.__handle_im3_80b(device_value)
        elif device_value.inels_type == IM3_140M:
            SensorHAHandler.__handle_im3_140m(device_value)
        elif device_value.inels_type == DMD3_1:
            SensorHAHandler.__handle_dmd3_1(device_value)
        elif device_value.inels_type == ADC3_60M:
            SensorHAHandler.__handle_adc3_60m(device_value)
        elif device_value.inels_type == TI3_10B or device_value.inels_type == TI3_40B or device_value.inels_type == TI3_60M:
            SensorHAHandler.__handle_ti3_series(device_value)
        elif device_value.inels_type == IDRT3_1:
            SensorHAHandler.__handle_idrt3_1(device_value)
        else:
            _LOGGER.warning(f"Unsupported inels_type: {device_value.inels_type}")

    @staticmethod
    def __handle_rf_temperature_input(device_value: DeviceValue) -> None:
        battery = int(device_value.trim_inels_status_values(DEVICE_TYPE_10_DATA, BATTERY, ""), 16)
        temp_in = device_value.trim_inels_status_values(DEVICE_TYPE_10_DATA, TEMP_IN, "")
        temp_out = device_value.trim_inels_status_values(DEVICE_TYPE_10_DATA, TEMP_OUT, "")

        device_value.ha_value = new_object(
            low_battery=(battery!=0),
            temp_in=temp_in,
            temp_out=temp_out,
        )

    @staticmethod
    def __handle_rf_thermostat(device_value: DeviceValue) -> None:
        temp_in = int(device_value.trim_inels_status_values(DEVICE_TYPE_12_DATA, TEMP_IN, ""), 16) * 0.5
        battery = int(device_value.trim_inels_status_values(DEVICE_TYPE_12_DATA, BATTERY, ""), 16)
        # has 2 values, 0x80 and 0x81 on which 0x81 means low battery

        device_value.ha_value = new_object(
            low_battery=(battery == 0x81),
            temp_in=temp_in,
        )

    @staticmethod
    def __handle_rf_flood_detector(device_value: DeviceValue) -> None:
        state = device_value.trim_inels_status_values(DEVICE_TYPE_15_DATA, STATE, "")
        state = f"0x{state}"
        state = f"{int(state, 16):0>8b}"

        ain = int(device_value.trim_inels_status_values(DEVICE_TYPE_15_DATA, AIN, ""), 16) /100

        low_battery=state[7] == "1"
        flooded=state[0] == "1"
        ains=[]
        ains.append(ain)
        device_value.ha_value = new_object(
            low_battery=low_battery,
            flooded=flooded,
            ains=ains,
        )

    @staticmethod
    def __handle_rf_detector(device_value: DeviceValue) -> None:
        state = device_value.trim_inels_status_values(
            DEVICE_TYPE_16_DATA, STATE, "")
        state = f"0x{state}"
        state = f"{int(state, 16):0>8b}"


        low_battery=state[4] == "1"
        detected=state[3] == "1"
        tamper=state[1]=="1"

        device_value.ha_value = new_object(
            low_battery=low_battery,
            detected=detected,
            tamper=tamper,
        )

    @staticmethod
    def __handle_rf_motion_detector(device_value: DeviceValue) -> None:
        state = device_value.trim_inels_status_values(
            DEVICE_TYPE_16_DATA, STATE, "")
        state = f"0x{state}"
        state = f"{int(state, 16):0>8b}"

        low_battery=state[4] == "1"
        motion=state[3] == "1"
        tamper=state[1]=="1"

        device_value.ha_value = new_object(
            low_battery=low_battery,
            motion=motion,
            tamper=tamper,
        )

    @staticmethod
    def __handle_rf_temperature_humidity_sensor(device_value: DeviceValue) -> None:
        battery = int(device_value.trim_inels_status_values(DEVICE_TYPE_29_DATA, BATTERY, ""), 16)
        temp_in = device_value.trim_inels_status_values(DEVICE_TYPE_29_DATA, TEMP_IN, "")
        humidity = int(device_value.trim_inels_status_values(DEVICE_TYPE_29_DATA, HUMIDITY, ""), 16)

        device_value.ha_value = new_object(
            low_battery=(battery!=0),
            temp_in=temp_in,
            humidity=humidity,
        )

    @staticmethod
    def __handle_grt3_50(device_value: DeviceValue) -> None:
        digital_inputs = device_value.trim_inels_status_values(
            GRT3_50_DATA, GRT3_50, "")
        digital_inputs_hex_str = f"0x{digital_inputs}"
        digital_inputs_bin_str = f"{int(digital_inputs_hex_str, 16):0>8b}"

        plusminus = device_value.trim_inels_status_values(
            GRT3_50_DATA, PLUS_MINUS_BUTTONS, "")
        plusminus = f"0x{plusminus}"
        plusminus = f"{int(plusminus, 16):0>8b}"

        temp_in = device_value.trim_inels_status_values(GRT3_50_DATA, TEMP_IN, "")

        light_in = device_value.trim_inels_status_values(GRT3_50_DATA, LIGHT_IN, "")

        ain = device_value.trim_inels_status_values(GRT3_50_DATA, AIN, "")

        humidity = device_value.trim_inels_status_values(GRT3_50_DATA, HUMIDITY, "")

        dewpoint = device_value.trim_inels_status_values(GRT3_50_DATA, DEW_POINT, "")


        device_value.ha_value = new_object(
            # digital inputs
            din=[# 2
                digital_inputs_bin_str[7] == "1", #0 -> 7, reverse endianness
                digital_inputs_bin_str[6] == "1",
            ],
            interface=[# 5
                digital_inputs_bin_str[5] == "1",
                digital_inputs_bin_str[4] == "1",
                digital_inputs_bin_str[3] == "1",
                digital_inputs_bin_str[2] == "1",
                digital_inputs_bin_str[1] == "1", #6
                plusminus[7] == "1", # plus
                plusminus[6] == "1", # minus
            ],

            temp_in=temp_in,

            light_in=light_in,

            ain=ain,

            humidity=humidity,

            dewpoint=dewpoint,

            # backlit
            backlit=False,
        )

    @staticmethod
    def __handle_wsb3_20_40(device_value: DeviceValue) -> None:
        switches = device_value.trim_inels_status_values(
            WSB3_240_DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = device_value.trim_inels_status_values(
            WSB3_240_DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        interface=[] #up/down buttons
        for i in range(WSB3_AMOUNTS[device_value.inels_type]):
            interface.append(switches[7 - i] == "1")

        din=[]
        for i in range(2):
            din.append(digital_inputs[7 - i] == "1")

        temp_in=device_value.trim_inels_status_values(
            WSB3_240_DATA, TEMP_IN, ""
        )
        ain=device_value.trim_inels_status_values(
            WSB3_240_DATA, AIN, ""
        )

        device_value.ha_value = new_object(
            interface=interface,
            din=din,
            temp_in=temp_in,
            ain=ain,
        )

    @staticmethod
    def __handle_wsb3_20h_40h(device_value: DeviceValue) -> None:
        switches = device_value.trim_inels_status_values(
            WSB3_240HUM_DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"


        digital_inputs = device_value.trim_inels_status_values(
            WSB3_240HUM_DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"
        interface=[] #up/down buttons
        din=[]
        for i in range(WSB3_AMOUNTS[device_value.inels_type]):
            interface.append(switches[7 - i] == "1")
        for i in range(2):
            din.append(digital_inputs[7 - i] == "1")

        temp_in = device_value.trim_inels_status_values(WSB3_240HUM_DATA, TEMP_IN, "")

        ain = device_value.trim_inels_status_values(WSB3_240HUM_DATA, AIN, "")

        humidity = device_value.trim_inels_status_values(WSB3_240HUM_DATA, HUMIDITY, "")

        dewpoint = device_value.trim_inels_status_values(WSB3_240HUM_DATA, DEW_POINT, "")

        device_value.ha_value = new_object(
            interface=interface,
            din=din,
            temp_in=temp_in,
            ain=ain,
            humidity=humidity,
            dewpoint=dewpoint,
        )

    @staticmethod
    def __handle_im3_20b_40b(device_value: DeviceValue) -> None:
        binary_input = []
        inputs = device_value.trim_inels_status_values(IM3_240B_DATA, IN, "")
        inputs = f"0x{inputs}"
        inputs = f"{int(inputs, 16):0>8b}"
        for i in range(IM3_AMOUNTS[device_value.inels_type]):
            binary_input.append(int(inputs[7-2*i-1] + inputs[7-2*i], 2))

        temp = device_value.trim_inels_status_values(IM3_240B_DATA, TEMP_IN, "")
        device_value.ha_value = new_object(
            input=binary_input,
            temp_in=temp,
        )

    @staticmethod
    def __handle_im3_80b(device_value: DeviceValue) -> None:
        binary_input = []
        binary_input2 = []
        inputs = device_value.trim_inels_status_values(IM3_80B_DATA, IN, "")
        inputs = f"0x{inputs}"
        inputs = f"{int(inputs, 16):0>16b}"
        for i in range(4):
            binary_input.append(int(inputs[7-2*i-1] + inputs[7-2*i], 2))
            binary_input2.append(int(inputs[15-2*i-1] + inputs[15-2*i], 2))
        binary_input.extend(binary_input2)

        temp = device_value.trim_inels_status_values(IM3_80B_DATA, TEMP_IN, "")
        device_value.ha_value = new_object(
            input=binary_input,
            temp=temp,
        )

    @staticmethod
    def __handle_im3_140m(device_value: DeviceValue) -> None:
        binary_input = []
        binary_input2 = []
        binary_input3 = []
        inputs = device_value.trim_inels_status_values(IM3_140M_DATA, IN, "")
        inputs = f"0x{inputs}"
        inputs = f"{int(inputs, 16):0>32b}"

        for i in range(4):
            binary_input.append(int(inputs[7-2*i-1] + inputs[7-2*i], 2))
            binary_input2.append(int(inputs[15-2*i-1] + inputs[15-2*i], 2))
            binary_input3.append(int(inputs[23-2*i-1] + inputs[23-2*i], 2))
        binary_input.extend(binary_input2)
        binary_input.extend(binary_input3)

        for i in range(2):
            binary_input.append(int(inputs[31-2*i-1] + inputs[31-2*i], 2))

        device_value.ha_value = new_object(
            input=binary_input
        )

    @staticmethod
    def __handle_dmd3_1(device_value: DeviceValue) -> None:
        light_in = device_value.trim_inels_status_values(DMD3_1_DATA, LIGHT_IN, "")
        temp_in = device_value.trim_inels_status_values(DMD3_1_DATA, TEMP_IN, "")
        humidity = device_value.trim_inels_status_values(DMD3_1_DATA, HUMIDITY, "")
        motion = device_value.trim_inels_status_values(
            DMD3_1_DATA, DMD3_1, "")
        motion = f"0x{motion}"
        motion = f"{int(motion, 16):0>8b}"

        motion=motion[7] == "1"

        device_value.ha_value = new_object(
            light_in=light_in,
            temp_in=temp_in,
            humidity=humidity,
            motion=motion,
        )

    @staticmethod
    def __handle_adc3_60m(device_value: DeviceValue) -> None:
        ains=[]
        ain_bytes = device_value.trim_inels_status_bytes(
            ADC3_60M_DATA, AIN,
        )
        for i in range(int(len(ain_bytes)/4)):
            ains.append(ain_bytes[4*i] + ain_bytes[4*i+1] + ain_bytes[4*i+2] + ain_bytes[4*i+3])

        device_value.ha_value = new_object(
            ains=ains,
        )

    @staticmethod
    def __handle_ti3_series(device_value: DeviceValue) -> None:
        temps = []
        temp_bytes = device_value.trim_inels_status_bytes(
            INELS_DEVICE_TYPE_DATA_STRUCT_DATA[device_value.inels_type],
            TEMP_IN,
        )

        for i in range(int(len(temp_bytes)/2)):
            temps.append(temp_bytes[2*i] + temp_bytes[2*i+1])

        device_value.ha_value = new_object(
            temps=temps
        )

    @staticmethod
    def __handle_idrt3_1(device_value: DeviceValue) -> None:
        inputs = device_value.trim_inels_status_values(IDRT3_1_DATA, SW, "")
        inputs = f"0x{inputs}"
        inputs = f"{int(inputs, 16):0>8b}"

        interface = []
        din = []
        for i in range(2):
            din.append(inputs[7-i]=="1")
            interface.append(inputs[5-i]=="1")

        temp_in = device_value.trim_inels_status_values(IDRT3_1_DATA, TEMP_IN, "")
        temp_out = device_value.trim_inels_status_values(IDRT3_1_DATA, TEMP_OUT, "")

        device_value.ha_value = new_object(
            interface=interface,
            din=din,
            temp_in=temp_in,
            temp_out=temp_out,
        )

class LightHAHandler(HAValueHandler):
    @staticmethod
    def update_ha_value(device_value: DeviceValue) -> None:
        if device_value.inels_type in [RF_SINGLE_DIMMER, RF_DIMMER]:
            LightHAHandler.__handle_rf_dimmer(device_value)
        elif device_value.inels_type == RF_DIMMER_RGB:
            LightHAHandler.__handle_rf_dimmer_rgb(device_value)
        elif device_value.inels_type == RF_LIGHT_BULB:
            LightHAHandler.__handle_rf_light_bulb(device_value)
        elif device_value.inels_type == DA3_22M:
            LightHAHandler.__handle_da3_22m(device_value)
        elif device_value.inels_type == DAC3_04B:
            LightHAHandler.__handle_dac3_04b(device_value)
        elif device_value.inels_type == DAC3_04M:
            LightHAHandler.__handle_dac3_04m(device_value)
        elif device_value.inels_type == DCDA_33M:
            LightHAHandler.__handle_dcda_33m(device_value)
        elif device_value.inels_type == DA3_66M:
            LightHAHandler.__handle_da3_66m(device_value)
        elif device_value.inels_type == DALI_DMX_UNIT:
            LightHAHandler.__handle_dali_dmx_unit(device_value)
        elif device_value.inels_type == DALI_DMX_UNIT_2:
            LightHAHandler.__handle_dali_dmx_unit_2(device_value)
        else:
            _LOGGER.warning(f"Unsupported inels_type: {device_value.inels_type}")

    @staticmethod
    def __handle_rf_dimmer(device_value: DeviceValue) -> None:
        if device_value.inels_status_value is None:
            _LOGGER.info("inels_status_value was None for RFDAC")
            device_value.inels_set_value = DEVICE_TYPE_05_COMM_TEST
            device_value.ha_value = None
        else:
            brightness = int(device_value.trim_inels_status_values(DEVICE_TYPE_05_DATA, RF_DIMMER, ""), 16)
            brightness = int((((0xFFFF - brightness) - 10000)/1000)*5)
            brightness = round(brightness, -1)

            simple_light = []
            simple_light.append(
                SimpleLight(brightness=brightness)
            )
            device_value.ha_value = new_object(simple_light=simple_light)

    @staticmethod
    def __handle_rf_dimmer_rgb(device_value: DeviceValue) -> None:
        if device_value.inels_status_value is None:
            _LOGGER.info("inels_status_value was None for %s", RF_DIMMER_RGB)
            device_value.inels_set_value = DEVICE_TYPE_13_COMM_TEST
            device_value.ha_value = None
        else:
            red = int(device_value.trim_inels_status_values(DEVICE_TYPE_06_DATA, RED, ""), 16)
            green = int(device_value.trim_inels_status_values(DEVICE_TYPE_06_DATA, GREEN, ""), 16)
            blue = int(device_value.trim_inels_status_values(DEVICE_TYPE_06_DATA, BLUE, ""), 16)
            brightness = int(int(device_value.trim_inels_status_values(DEVICE_TYPE_06_DATA, OUT, ""), 16)* 100.0/255.0)

            rgb=[]
            rgb.append(
                RGBLight(
                    r=red,
                    g=green,
                    b=blue,
                    brightness=brightness,
                )
            )

            device_value.ha_value=new_object(
                rgb=rgb
            )

    @staticmethod
    def __handle_rf_light_bulb(device_value: DeviceValue) -> None:
        if device_value.inels_status_value is None:
            _LOGGER.info("inels_status_value was None for %s", RF_LIGHT_BULB)
            device_value.inels_set_value = DEVICE_TYPE_13_COMM_TEST
            device_value.ha_value = None
        else:
            warm_light = []
            warm_light.append(
                WarmLight(
                        brightness=round(
                            int(device_value.trim_inels_status_values(DEVICE_TYPE_13_DATA, OUT, ""), 16) * 100.0/255.0
                        ),
                        relative_ct=round(
                            int(device_value.trim_inels_status_values(DEVICE_TYPE_13_DATA, WHITE, ""), 16) * 100.0/255.0
                        )
                    ),
                )

            device_value.ha_value=new_object(warm_light=warm_light)

    @staticmethod
    def __handle_da3_22m(device_value: DeviceValue) -> None:
        temp = device_value.trim_inels_status_values(DA3_22M_DATA, TEMP_IN, "")

        state = device_value.trim_inels_status_values(
            DA3_22M_DATA, DA3_22M, "")
        state_hex_str = f"0x{state}"
        state_bin_str = f"{int(state_hex_str, 16):0>8b}"

        toa=[ # thermal overload alarm
            state_bin_str[3] == "1",
            state_bin_str[2] == "1",
        ]
        coa=[ # current overload alrm
            state_bin_str[1] == "1", #6
            state_bin_str[0] == "1", #7
        ]

        out1 = int(
            device_value.trim_inels_status_values(
                DA3_22M_DATA, DIM_OUT_1, ""
            ), 16
        )

        out2 = int(
            device_value.trim_inels_status_values(
                DA3_22M_DATA, DIM_OUT_2, ""
            ), 16
        )
        out1 = out1 if out1 <= 100 else 100
        out2 = out2 if out2 <= 100 else 100
        out = [out1, out2]

        light_coa_toa = []
        for i in range(2):
            light_coa_toa.append(
                LightCoaToa(
                    brightness=out[i],
                    toa=toa[i],
                    coa=coa[i],
                )
            )

        device_value.ha_value = new_object(
            #May not be that interesting for HA
            sw=[
                state_bin_str[7] == "1", #0
                state_bin_str[6] == "1", #1
            ],
            din=[
                state_bin_str[5] == "1",
                state_bin_str[4] == "1"
            ],

            temp_in=temp,
            light_coa_toa=light_coa_toa,
        )

        set_val = "00\n00\n00\n00\n"
        for i in range(len(device_value.ha_value.light_coa_toa)):
            set_val +=  f"{device_value.ha_value.light_coa_toa[i].brightness:02X}\n"
        device_value.inels_set_value = set_val

    @staticmethod
    def __handle_dac3_04b(device_value: DeviceValue) -> None:
        temp_out = device_value.trim_inels_status_values(DAC3_04_DATA, TEMP_OUT, "")

        aout_alert = int(device_value.trim_inels_status_values(DAC3_04_DATA, ALERT, ""), 16) != 0

        aout_str = device_value.trim_inels_status_bytes(DAC3_04_DATA, OUT)
        aout = []
        for d in aout_str:
            d = int(d, 16)
            d = d if d <= 100 else 100
            aout.append(
                AOUTLight(
                    brightness=d,
                    aout_coa=aout_alert,
                )
            )

        device_value.ha_value = new_object(
            temp_out=temp_out,
            aout=aout,
        )

        set_val = "00\n" * 4
        for d in aout:
            set_val += f"{d.brightness:02X}\n"

    @staticmethod
    def __handle_dac3_04m(device_value: DeviceValue) -> None:
        temp_out = device_value.trim_inels_status_values(DAC3_04_DATA, TEMP_OUT, "")

        aout_alert = device_value.trim_inels_status_values(DAC3_04_DATA, ALERT, "")
        aout_coa=[]
        for i in range(4):
            aout_coa.append(aout_alert[6-i] == "1") #skip first bit

        aout_str = device_value.trim_inels_status_bytes(DAC3_04_DATA, OUT)
        aout_val = []
        for d in aout_str:
            d = int(d, 16)
            d = d if d <= 100 else 100
            aout_val.append(d)

        aout=[]
        for i in range(4):
            aout.append(
                AOUTLight(
                    brightness=aout_val[i],
                    aout_coa=aout_coa[i],
                )
            )

        device_value.ha_value = new_object(
            temp_out=temp_out,
            aout=aout,
        )

        set_val = "00\n" * 4
        for d in aout:
            set_val += f"{d.brightness:02X}\n"

    @staticmethod
    def __handle_dcda_33m(device_value: DeviceValue) -> None:
        digital_inputs = device_value.trim_inels_status_values(DCDA_33M_DATA, ALERT, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        sw = []
        coa = []
        for i in range(3):
            sw.append(digital_inputs[7-i] == "1")
            coa.append(digital_inputs[4-i] == "1")

        coa.append(False) #only 3 alerts, so I fake the last one

        aout_val=[]
        aouts = device_value.trim_inels_status_bytes(DCDA_33M_DATA, OUT)
        for i in range(len(aouts)):
            brightness = int(i, 16)
            brightness = brightness if brightness > 100 else 100
            aout_val.append(brightness)

        aout=[]
        for i in range(4):
            aout.append(AOUTLight(
                    brightness=aout_val[i],
                    aout_coa=coa[i],
                )
            )


        device_value.ha_value = new_object(
            sw=sw,
            aout=aout,
        )

        set_val = "00\n"*4
        for i in range(4):
            aout_val = aout[i].brightness
            set_val += f"{aout_val:02X}\n"
        device_value.inels_set_value = set_val

    @staticmethod
    def __handle_da3_66m(device_value: DeviceValue) -> None:
        state = device_value.trim_inels_status_values(
            DA3_66M_DATA, ALERT, ""
        )
        state = f"0x{state}"
        state = f"{int(state, 16):0>16b}"

        toa = []
        coa = []
        for i in range (4):
            toa.append(state[7-2*i]=="1")
            coa.append(state [7-2*i-1] == "1")
        for i in range(2):
            toa.append(state[15-2*i]== "1")
            coa.append(state[15-2*i-1] == "1")

        switches = device_value.trim_inels_status_values(
            DA3_66M_DATA, SW, ""
        )
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = device_value.trim_inels_status_values(
            DA3_66M_DATA, DIN, ""
        )
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        sw = []
        din = []
        for i in range(6):
            sw.append(switches[7-i] == "1")
            din.append(digital_inputs[7-i] == "1")

        out = []
        outs = device_value.trim_inels_status_bytes(
            DA3_66M_DATA, OUT
        )

        for o in outs:
            out.append(int(o, 16))

        light_coa_toa=[]
        for i in range(6):
            light_coa_toa.append(
                LightCoaToa(
                    brightness=out[i],
                    toa=toa[i],
                    coa=coa[i],
                )
            )

        device_value.ha_value = new_object(
            sw=sw,
            din=din,
            light_coa_toa=light_coa_toa,
        )

        set_val = "00\n"*4
        for i in range(4):
            set_val += f"{device_value.ha_value.light_coa_toa[i].brightness:02X}\n"
        set_val += "00\n"*4
        for i in range(4, 6):
            set_val += f"{device_value.ha_value.light_coa_toa[i].brightness:02X}\n"
        set_val += "00\n"*12
        device_value.inels_set_value = set_val

    @staticmethod
    def __handle_dali_dmx_unit(device_value: DeviceValue) -> None:
        outs = device_value.trim_inels_status_bytes(DALI_DMX_UNIT_DATA, OUT)
        simple_light = []
        for o in outs:
            o = int(o, 16)
            o = o if o < 100 else 100
            simple_light.append(
                SimpleLight(
                    brightness=o,
                )
            )

        device_value.ha_value = new_object(
            simple_light=simple_light,
        )

    @staticmethod
    def __handle_dali_dmx_unit_2(device_value: DeviceValue) -> None:
        outs = device_value.trim_inels_status_bytes(DALI_DMX_UNIT_DATA, OUT)
        warm_light = []
        lights = list(zip(outs[::2], outs[1::2]))

        for l in lights:
            b = min(int(l[0], 16), 100)
            w = min(int(l[1], 16), 100)
            warm_light.append(
                WarmLight(
                    brightness=b,
                    relative_ct=w,
                )
            )

        device_value.ha_value = new_object(
            warm_light=warm_light,
        )

class CoverHAHandler(HAValueHandler):
    @staticmethod
    def update_ha_value(device_value: DeviceValue) -> None:
        if device_value.inels_type == RF_SHUTTERS:
            CoverHAHandler.__handle_rf_shutters(device_value)
        elif device_value.inels_type == RF_SHUTTER_UNIT:
            CoverHAHandler.__handle_rf_shutter_unit(device_value)
        elif device_value.inels_type == JA3_018M:
            CoverHAHandler.__handle_ja3_018m(device_value)
        elif device_value.inels_type == JA3_014M:
            CoverHAHandler.__handle_ja3_014m(device_value)
        else:
            _LOGGER.warning(f"Unsupported inels_type: {device_value.inels_type}")

    @staticmethod
    def __handle_rf_shutters(device_value: DeviceValue) -> None:
        if device_value.inels_status_value is None:
            _LOGGER.info("inels_status_value was 'None' for %s", RF_SHUTTERS)
            device_value.inels_set_value = DEVICE_TYPE_03_COMM_TEST
            device_value.ha_value = None
        else:
            # shutters True -> closed, False -> open
            shutters = []
            shutter_val = int(device_value.trim_inels_status_values(DEVICE_TYPE_03_DATA, SHUTTER, ""), 16)

            # So as to continue driving it down if it aisn't closed
            # and continue opening it if it isn't open
            if shutter_val not in [Shutter_state.Open, Shutter_state.Closed]:
                shutter_val = device_value.last_value.shutters[0].state
            shutters.append(
                Shutter(
                    state=shutter_val,
                    is_closed=(shutter_val is Shutter_state.Closed)
                )
            )

            device_value.ha_value = new_object(
                shutters=shutters,
            )

            device_value.inels_set_value = f"{RF_SHUTTER_STATE_SET[shutters[0].state]}\n00\n00\n"


    @staticmethod
    def __handle_rf_shutter_unit(device_value: DeviceValue) -> None:
        if device_value.inels_status_value is None:
            _LOGGER.info("inels_status_value was 'None' for %s", RF_SHUTTER_UNIT)
            device_value.inels_set_value = DEVICE_TYPE_03_COMM_TEST
            device_value.ha_value = None
        else:
            shutters_with_pos = []

            position = 100 - int(device_value.trim_inels_status_values(DEVICE_TYPE_21_DATA, POSITION, ""), 16)

            shutter_val = int(device_value.trim_inels_status_values(DEVICE_TYPE_21_DATA, SHUTTER, ""))
            shutter_val = ((shutter_val >> 1) & 1) | (shutter_val & 1) << 1 #swap bit 0 with bit 1

            if shutter_val == Shutter_state.Closed and position != 0:
                shutter_val = Shutter_state.Open

            if (device_value.last_value is not None) and (shutter_val not in [Shutter_state.Open, Shutter_state.Closed]):
                shutter_val = device_value.last_value.shutters[0].state


            shutters_with_pos.append(
                Shutter_pos(
                    state=shutter_val,
                    is_closed=shutter_val == Shutter_state.Closed,
                    position=position,
                    set_pos=False,
                )
            )

            device_value.ha_value = new_object(
                shutters_with_pos=shutters_with_pos,
            )
            device_value.inels_set_value = f"{RF_SHUTTER_STATE_SET[shutters_with_pos[0].state]}\n00\n00\n"

    @staticmethod
    def __handle_ja3_018m(device_value: DeviceValue) -> None:
        shutter_relays=[]
        for r in device_value.trim_inels_status_bytes(JA3_018M_DATA, SHUTTER):
            shutter_relays.append((int(r, 16) & 1) != 0)

        simple_shutters = []
        shutters = list(zip(shutter_relays[::2], shutter_relays[1::2]))
        for s in shutters:
            if s[0]:
                state = Shutter_state.Open
            elif s[1]:
                state = Shutter_state.Closed
            else:
                state = Shutter_state.Stop_down
            simple_shutters.append(
                Shutter(
                    state=state,
                    is_closed=None
                )
            )

        interface=[]
        digital_inputs = device_value.trim_inels_status_values(
            JA3_018M_DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"

        for i in range(8):
            interface.append(digital_inputs[7-i] == "1")
        for i in range(8):
            interface.append(digital_inputs[15-i] == "1")

        alerts = device_value.trim_inels_status_values(
            JA3_018M_DATA, ALERT, "")
        alerts = f"0x{alerts}"
        alerts = f"{int(alerts, 16):0>8b}"

        for i in range(2):
            interface.append(alerts[7-i] == "1")

        alert_power = alerts[4]=="1"
        alert_comm = [
            alerts[3]=="1",
            alerts[2]=="1",
            alerts[1]=="1"
        ]

        overflows = device_value.trim_inels_status_values(
            JA3_018M_DATA, RELAY_OVERFLOW, "")
        overflows = f"0x{overflows}"
        overflows = f"{int(overflows, 16):0>8b}"

        #TODO add overflows and alerts to the shutters
        relay_overflow=[]
        for i in range(8):
            relay_overflow.append(overflows[7-i] == "1")

        relay_overflow.append(alerts[0]=="1")

        #I'll register them as an interface and replace the names to SW 1 up/down, etc...

        device_value.ha_value=new_object(
            simple_shutters=simple_shutters,
            interface=interface,

        )

        device_value.inels_set_value = f"{''.join([SIMPLE_SHUTTER_STATE_SET[x.state] for x in simple_shutters])}"

    @staticmethod
    def __handle_ja3_014m(device_value: DeviceValue) -> None:
        shutter_relays = []
        for r in device_value.trim_inels_status_bytes(JA3_014M_DATA, SHUTTER):
            shutter_relays.append((int(r, 16) & 1) != 0)

        simple_shutters = []
        shutters = list(zip(shutter_relays[::2], shutter_relays[1::2]))

        for s in shutters:
            if s[0]:
                state = Shutter_state.Open
            elif s[1]:
                state = Shutter_state.Closed
            else:
                state = Shutter_state.Stop_down
            simple_shutters.append(
                Shutter(
                    state=state,
                    is_closed=None
                )
            )

        interface = []
        digital_inputs = device_value.trim_inels_status_values(
            JA3_014M_DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"

        for i in range(8):
            interface.append(digital_inputs[7 - i] == "1")
        for i in range(6):
            interface.append(digital_inputs[13 - i] == "1")

        alerts = device_value.trim_inels_status_values(
            JA3_014M_DATA, ALERT, "")
        alerts = f"0x{alerts}"
        alerts = f"{int(alerts, 16):0>8b}"

        for i in range(7):
            interface.append(alerts[6 - i] == "1")

        # alert_power = alerts[4] == "1"
        # alert_comm = [
        #     alerts[3] == "1",
        #     alerts[2] == "1",
        #     alerts[1] == "1"
        # ]

        overflows = device_value.trim_inels_status_values(
            JA3_014M_DATA, RELAY_OVERFLOW, "")
        overflows = f"0x{overflows}"
        overflows = f"{int(overflows, 16):0>16b}"

        # TODO add overflows and alerts to the shutters
        relay_overflow = []
        for i in range(8):
            interface.append(overflows[7 - i] == "1")
        for i in range(6):
            interface.append(overflows[13 - i] == "1")

        # relay_overflow.append(alerts[0] == "1")

        # I'll register them as an interface and replace the names to SW 1 up/down, etc...

        device_value.ha_value = new_object(
            simple_shutters=simple_shutters,
            interface=interface,

        )

        device_value.inels_set_value = f"{''.join([SIMPLE_SHUTTER_STATE_SET[x.state] for x in simple_shutters])}"

class ClimateHAHandler(HAValueHandler):
    @staticmethod
    def update_ha_value(device_value: DeviceValue) -> None:
        if device_value.inels_type == RF_WIRELESS_THERMOVALVE:
            ClimateHAHandler.__handle_rf_wireless_thermovalve(device_value)
        elif device_value.inels_type == VIRT_CONTR:
            ClimateHAHandler.__handle_virt_contr(device_value)
        elif device_value.inels_type == VIRT_HEAT_REG:
            ClimateHAHandler.__handle_virt_heat_reg(device_value)
        elif device_value.inels_type == VIRT_COOL_REG:
            ClimateHAHandler.__handle_virt_cool_reg(device_value)
        else:
            _LOGGER.warning(f"Unsupported inels_type: {device_value.inels_type}")

    @staticmethod
    def __handle_rf_wireless_thermovalve(device_value: DeviceValue) -> None:
        # fetches all the status values and compacts them into a new object
        temp_current_hex = device_value.trim_inels_status_values(
            DEVICE_TYPE_09_DATA, CURRENT_TEMP, ""
        )
        temp_current = int(temp_current_hex, 16) * 0.5
        temp_required_hex = device_value.trim_inels_status_values(
            DEVICE_TYPE_09_DATA, REQUIRED_TEMP, ""
        )
        temp_required = int(temp_required_hex, 16) * 0.5
        battery = int(device_value.trim_inels_status_values(
            DEVICE_TYPE_09_DATA, BATTERY, ""
        ), 16)
        open_to_hex = device_value.trim_inels_status_values(
            DEVICE_TYPE_09_DATA, OPEN_IN_PERCENTAGE, ""
        )
        open_to_percentage = int(open_to_hex, 16) * 0.5

        climate_mode = Climate_modes.Off
        if temp_current < temp_required:
            climate_mode = Climate_modes.Heat

        device_value.ha_value = new_object(
            low_battery=(battery!=0),
            thermovalve=new_object(
                current=temp_current,
                required=temp_required,
                climate_mode=climate_mode,
                open_in_percentage=open_to_percentage,
            )
        )

    @staticmethod
    def __handle_virt_contr(device_value: DeviceValue) -> None:
        temp_current = int(device_value.trim_inels_status_values(
            DEVICE_TYPE_166_DATA, CURRENT_TEMP, ""
        ), 16)
        if temp_current == 0x7FFFFFFB:
            temp_current = 0
        else:
            temp_current /= 100
        temp_critical_max = int(device_value.trim_inels_status_values( #check if 0x7F FF FF FB -> make it 50
            DEVICE_TYPE_166_DATA, CRITICAL_MAX_TEMP, ""
        ), 16) / 100
        temp_required_heat = int(device_value.trim_inels_status_values(
            DEVICE_TYPE_166_DATA, REQUIRED_HEAT_TEMP, ""
        ), 16)
        if temp_required_heat == 0x7FFFFFFB:
            temp_required_heat = 0
        else:
            temp_required_heat /= 100
        temp_critical_min = int(device_value.trim_inels_status_values( #check if 0x7F FF FF FB -> make it -50
            DEVICE_TYPE_166_DATA, CRITICAL_MIN_TEMP, ""
        ), 16) / 100
        temp_required_cool = int(device_value.trim_inels_status_values(
            DEVICE_TYPE_166_DATA, REQUIRED_COOL_TEMP, ""
        ), 16)
        if temp_required_cool == 0x7FFFFFFB:
            temp_required_cool = 0
        else:
            temp_required_cool /= 100
        temp_correction = int(device_value.trim_inels_status_values(
            DEVICE_TYPE_166_DATA, TEMP_CORRECTION, ""
        ), 16) / 100
        holiday_mode = int(device_value.trim_inels_status_values(
            DEVICE_TYPE_166_DATA, PUBLIC_HOLIDAY, ""
        ), 16)
        control_mode = int(device_value.trim_inels_status_values(
            DEVICE_TYPE_166_DATA, CONTROL_MODE, ""
        ))
        #0 -> user control [ONLY IMPLEMENT THIS ONE FOR NOW]
        #   Has presets (Schedule, Fav1-4 and manual temp)
        #1 -> 2 temp
        #2 -> single temp

        binary_vals = device_value.trim_inels_status_values(
            DEVICE_TYPE_166_DATA, VIRT_CONTR, ""
        )
        binary_vals = f"0x{binary_vals}"
        binary_vals = f"{int(binary_vals, 16):0>8b}"

        controller_on = binary_vals[7] == "1" #if controller is on
        schedule_mode = binary_vals[6] == "1" # schedule or a set temperature
        heating_enabled = binary_vals[5] == "1" #if heating is connected
        cooling_enabled = binary_vals[4] == "1" #if cooling is connected
        vacation = binary_vals[3] == "1"
        regulator_disabled = binary_vals[2] == "1" #window detection is on (?)

        climate_mode = Climate_modes.Off
        if controller_on: #TODO review all of this
            if control_mode == 0: #user control
                if heating_enabled:
                    climate_mode = Climate_modes.Heat
                elif cooling_enabled:
                    climate_mode = Climate_modes.Cool
            else:
                climate_mode = Climate_modes.Auto

        current_action = Climate_action.Off
        if controller_on:
            current_action = Climate_action.Idle
            # user controlled and two temp
            if control_mode == 0: # user control
                if climate_mode == Climate_modes.Heat and temp_current < temp_required_heat:
                    current_action = Climate_action.Heating
                elif climate_mode == Climate_modes.Cool and temp_current > temp_required_cool:
                    current_action = Climate_action.Cooling
            elif control_mode == 1: # two temp
                if temp_current < temp_required_heat:
                    current_action = Climate_action.Heating
                elif temp_current > temp_required_cool:
                    current_action = Climate_action.Cooling
            elif control_mode == 2: # one temp
                if temp_current < temp_required_heat:
                    current_action = Climate_action.Heating
                else:
                    current_action = Climate_action.Cooling

        # 1 -> schedule
        # 6 -> manual
        preset = 0 if schedule_mode else 5

        device_value.ha_value = new_object(
            climate_controller=new_object(
                current=temp_current, #current_temperature

                required=temp_required_heat, #target_temperature / target_temperature_high
                required_cool=temp_required_cool, #target_temperature_low

                climate_mode=climate_mode, #hvac_mode: Off/Heat_cool/Heat/Cool
                # Off -> controller is turned off
                # Heat_cool -> follow temp range
                # Heat -> only heating
                # Cool -> only cooling

                current_action=current_action, #hvac_action: Off/Heating/Cooling/Idle
                # Off -> controller is off
                # Heating -> heating is on
                # Cooling -> cooling is on
                # Idle -> temp is in range

                #non exposed
                critical_temp=temp_critical_max,
                correction_temp=temp_correction,
                public_holiday=holiday_mode,

                vacation=vacation,

                control_mode=control_mode,
                current_preset=preset,
            ),
        )

    @staticmethod
    def __handle_virt_heat_reg(device_value: DeviceValue) -> None:
        state=int(device_value.trim_inels_status_values(
            VIRT_REG_DATA, STATE, ""
        ), 16)

        reg=device_value.trim_inels_status_values(
            VIRT_REG_DATA, VIRT_HEAT_REG, ""
        )
        reg = f"{int(reg, 16):0>8b}"

        heat_reg=reg[7] == "1"
        heat_source = reg[6] == "1"

        device_value.ha_value = new_object(
            heating_out = heat_reg
        )

    @staticmethod
    def __handle_virt_cool_reg(device_value: DeviceValue) -> None:
        state=int(device_value.trim_inels_status_values(
            VIRT_REG_DATA, STATE, ""
        ), 16)

        reg=device_value.trim_inels_status_values(
            VIRT_REG_DATA, VIRT_HEAT_REG, ""
        )
        reg = f"{int(reg, 16):0>8b}"

        cool_reg=reg[7] == "1"
        cool_source = reg[6] == "1"

        device_value.ha_value = new_object(
            cooling_out=cool_reg,
        )

class ButtonHAHandler(HAValueHandler):
    @staticmethod
    def update_ha_value(device_value: DeviceValue) -> None:
        if device_value.inels_type == RF_CONTROLLER:
            ButtonHAHandler.__handle_rf_controller(device_value)
        elif device_value.inels_type == RF_2_BUTTON_CONTROLLER:
            ButtonHAHandler.__handle_rf_2_button_controller(device_value)
        elif device_value.inels_type == GSB3_90SX:
            ButtonHAHandler.__handle_gsb3_90sx(device_value)
        elif device_value.inels_type in [GSB3_20SX, GSB3_40SX, GSB3_60SX, GBP3_60]:
            ButtonHAHandler.__handle_gsb(device_value)
        elif device_value.inels_type == GSP3_100:
            ButtonHAHandler.__handle_gsp3_100(device_value)
        elif device_value.inels_type == GDB3_10:
            ButtonHAHandler.__handle_gdb3_10(device_value)
        else:
            _LOGGER.warning(f"Unsupported inels_type: {device_value.inels_type}")

    @staticmethod
    def __handle_rf_controller(device_value: DeviceValue) -> None:
        if device_value.inels_status_value is None:
            #No connection can be made, so just communicate low battery
            device_value.ha_value = new_object(
                low_battery = True,
                btn = [False, False, False, False]
            )
        else:
            state = device_value.trim_inels_status_values(DEVICE_TYPE_19_DATA, STATE, "")
            state_hex_str = f"0x{state}"  # 0xSTATE
            # interpret the value and write it in binary
            state_bin_str = f"{int(state_hex_str, 16):0>8b}"

            # read which button was last pressed
            identity = device_value.trim_inels_status_values(
                DEVICE_TYPE_19_DATA, IDENTITY, ""
            )


            #NEW
            low_battery = state_bin_str[4] == "1" # 1 -> low
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
                    btn[number-1] = pressed

            device_value.ha_value = new_object(
                low_battery=low_battery,
                btn=btn
            )

    @staticmethod
    def __handle_rf_2_button_controller(device_value: DeviceValue) -> None:
        if device_value.inels_status_value is None:
            device_value.ha_value = new_object(
                low_battery=True,
                btn=[False, False]
            )
        else:
            state = device_value.trim_inels_status_values(DEVICE_TYPE_19_DATA, STATE, "")
            state = f"0x{state}"  # 0xSTATE
            state = f"{int(state, 16):0>8b}"

            identity = device_value.trim_inels_status_values(DEVICE_TYPE_19_DATA, IDENTITY, "")

            low_battery = state[4] == "1"
            pressed = state[3] == "1"
            if device_value.last_value is None:
                btn = [False, False]
            else:
                btn = device_value.last_value.ha_value.btn

            if identity in BUTTON_NUMBER:
                number = BUTTON_NUMBER[identity]
                if number <= 2:
                    btn[number-1] = pressed

            device_value.ha_value = new_object(
                low_battery=low_battery,
                btn=btn,
            )

    @staticmethod
    def __handle_gsb3_90sx(device_value: DeviceValue) -> None:
        digital_inputs = device_value.trim_inels_status_values(
            GSB3_90SX_DATA, GSB3_90SX, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"


        temp = device_value.trim_inels_status_values(
            GSB3_90SX_DATA, TEMP_IN, "")

        light_in = device_value.trim_inels_status_values(
            GSB3_90SX_DATA, LIGHT_IN, "")

        ain = device_value.trim_inels_status_values(
            GSB3_90SX_DATA, AIN, "")

        humidity = device_value.trim_inels_status_values(
            GSB3_90SX_DATA, HUMIDITY, "")

        dewpoint = device_value.trim_inels_status_values(
            GSB3_90SX_DATA, DEW_POINT, "")

        device_value.ha_value = new_object(
            interface=[
                digital_inputs[7] == "1",#0
                digital_inputs[6] == "1",
                digital_inputs[5] == "1",
                digital_inputs[4] == "1",
                digital_inputs[3] == "1",
                digital_inputs[2] == "1",
                digital_inputs[1] == "1",
                digital_inputs[0] == "1",
                digital_inputs[15] == "1",#8
            ],
            din=[
                digital_inputs[14] == "1",#9
                digital_inputs[13] == "1",#10
            ],
            prox=digital_inputs[12] == "1",#11

            # Actually important:
            # temperature
            temp_in=temp,

            # light in
            light_in=light_in,

            # AIN
            ain=ain,

            # humidity
            humidity=humidity,

            # dewpoint
            dewpoint=dewpoint,

            # disabled
            disabled=False,
            # backlit
            backlit=False,
        )

    @staticmethod
    def __handle_gsb(device_value: DeviceValue) -> None:
        switches = device_value.trim_inels_status_values(
            GLASS_CONTROLLER_DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = device_value.trim_inels_status_values(
            GLASS_CONTROLLER_DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        interface = []
        for i in range(GSB3_AMOUNTS[device_value.inels_type]):
            interface.append(switches[7-i] == "1")

        din = []
        for i in range(2):
            din.append(digital_inputs[7-i] == "1")

        temp = device_value.trim_inels_status_values(
            GLASS_CONTROLLER_DATA, TEMP_IN, "")

        light_in = device_value.trim_inels_status_values(
            GLASS_CONTROLLER_DATA, LIGHT_IN, "")

        ain = device_value.trim_inels_status_values(
            GLASS_CONTROLLER_DATA, AIN, "")

        device_value.ha_value = new_object(
            interface=interface,
            din=din,
            # temperature
            temp_in=temp,

            # light in
            light_in=light_in,

            # AIN
            ain=ain,
        )

    @staticmethod
    def __handle_gsp3_100(device_value: DeviceValue) -> None:
        switches = device_value.trim_inels_status_values(
            GLASS_CONTROLLER_DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = device_value.trim_inels_status_values(
            GLASS_CONTROLLER_DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        interface = []
        for i in range(8):
            interface.append(switches[7-i] == "1")
        din = []
        for i in range(2):
            interface.append(digital_inputs[7-i]=="1")
            din.append(digital_inputs[5-i]=="1")

        temp_in = device_value.trim_inels_status_values(GLASS_CONTROLLER_DATA, TEMP_IN, "")
        light_in = device_value.trim_inels_status_values(GLASS_CONTROLLER_DATA, LIGHT_IN, "")
        ain = device_value.trim_inels_status_values(GLASS_CONTROLLER_DATA, AIN, "")
        device_value.ha_value = new_object(
            interface=interface,
            din=din,
            temp_in=temp_in,
            light_in=light_in,
            ain=ain,
        )

    @staticmethod
    def __handle_gdb3_10(device_value: DeviceValue) -> None:
        switches = device_value.trim_inels_status_values(
            GLASS_CONTROLLER_DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = device_value.trim_inels_status_values(
            GLASS_CONTROLLER_DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        interface = []
        for i in range(3):
            interface.append(switches[6-2*i]=="1")

        din = []
        for i in range(2):
            din.append(digital_inputs[7-i]=="1")

        temp_in = device_value.trim_inels_status_values(GLASS_CONTROLLER_DATA, TEMP_IN, "")
        light_in = device_value.trim_inels_status_values(GLASS_CONTROLLER_DATA, LIGHT_IN, "")
        ain = device_value.trim_inels_status_values(GLASS_CONTROLLER_DATA, AIN, "")
        device_value.ha_value = new_object(
            interface=interface,
            din=din,
            temp_in=temp_in,
            light_in=light_in,
            ain=ain,
        )

class SwitchInelsHandler(InelsValueHandler):
    @staticmethod
    def update_inels_value(device_value: DeviceValue) -> None:
        if device_value.inels_type is RF_SINGLE_SWITCH:
            if device_value.ha_value is None:
                device_value.inels_set_value = DEVICE_TYPE_07_COMM_TEST
            else:
                device_value.inels_set_value = f"{(2 - (device_value.ha_value.simple_relay[0].is_on)):02X}\n00\n"
        elif device_value.inels_type is RF_SWITCHING_UNIT:
            if device_value.ha_value is None:
                device_value.inels_set_value = DEVICE_TYPE_02_COMM_TEST
            else:
                device_value.inels_set_value = f"{(2 - (device_value.ha_value.simple_relay[0].is_on)):02X}\n00\n00\n"
        elif device_value.inels_type is RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR:
            if device_value.ha_value is None:
                device_value.inels_set_value = DEVICE_TYPE_07_COMM_TEST
            else:
                device_value.inels_set_value = SWITCH_WITH_TEMP_SET[device_value.ha_value.simple_relay[0].is_on]
        elif device_value.inels_type in [SA3_01B, SA3_02B, SA3_02M, SA3_04M, SA3_06M, SA3_012M, SA3_014M, IOU3_108M]:
            value = ""
            if hasattr(device_value.ha_value, "simple_relay"):
                for re in device_value.ha_value.simple_relay:
                    value += RELAY_SET[re.is_on]
                device_value.inels_set_value = value
            elif hasattr(device_value.ha_value, "relay"):
                for re in device_value.ha_value.relay:
                    value += RELAY_SET[re.is_on]
                device_value.inels_set_value = value
        elif device_value.inels_type is SA3_022M:
            value = ""
            for r in device_value.ha_value.relay:
                value += RELAY_SET[r.is_on]
            for s in device_value.ha_value.simple_shutters:
                value += SIMPLE_SHUTTER_STATE_SET[s.state]
            for v in device_value.ha_value.valve:
                value += RELAY_SET[v]
            device_value.inels_set_value = value
        elif device_value.inels_type is IOU3_108M:
            set_val = ""
            for r in device_value.ha_value.relay:
                set_val += RELAY_SET[r.is_on]
            device_value.inels_set_value = set_val
        elif device_value.inels_type is RC3_610DALI:
            set_val = "00\n" * 4 #4 bytes
            for a in device_value.ha_value.aout:
                set_val += f"{a.brightness:02X}\n"
            set_val += "00\n" * 2 #8 bytes
            for r in device_value.ha_value.relay:
                set_val += RELAY_SET[r.is_on] #16 bytes
            set_val += "00\n" * 4 #20 bytes
            for i in range(4):
                set_val += f"{device_value.ha_value.dali[i].brightness:02X}\n"
            set_val += "00\n" * 4
            for i in range(4, 8):
                set_val += f"{device_value.ha_value.dali[i].brightness:02X}\n"
            set_val += "00\n" * 4
            for i in range(8, 12):
                set_val += f"{device_value.ha_value.dali[i].brightness:02X}\n"
            set_val += "00\n" * 4
            for i in range(12, 16):
                set_val += f"{device_value.ha_value.dali[i].brightness:02X}\n"

            device_value.inels_set_value = set_val
        elif device_value.inels_type is FA3_612M:
            original_status = device_value.ha_value.last_status_val.split("\n")

            set_val = "00\n" * 4
            for a in device_value.ha_value.aout:
                set_val += f"{a.brightness:02X}\n"
            for i in range(4):
                set_val += f"{original_status[8 + i]}\n"
            fan_val = ""
            for i in range(3):
                fan_val += RELAY_SET[device_value.ha_value.fan_speed == (i + 1)]
            set_val += fan_val
            set_val += f"{original_status[15]}\n"

            device_value.inels_set_value = set_val
        elif device_value.inels_type in [GCR3_11, GCH3_31]:
            set_val = "04\n" if device_value.ha_value.simple_relay[0].is_on else "00\n"
            set_val += "00\n" * 9
            device_value.inels_set_value = set_val
        elif device_value.inels_type is BITS:
            set_val = {}
            for bit in device_value.ha_value.bit:
                set_val[bit.addr] = int(bit.is_on)

            device_value.inels_set_value = json.dumps({"cmd": set_val})


class NumberInelsHandler(InelsValueHandler):
    @staticmethod
    def update_inels_value(device_value: DeviceValue) -> None:
        set_val = {}
        for number in device_value.ha_value.number:
            set_val[number.addr] = int(number.value)

        device_value.inels_set_value = json.dumps({"cmd": set_val})


class LightInelsHandler(InelsValueHandler):
    @staticmethod
    def update_inels_value(device_value: DeviceValue) -> None:
        if device_value.inels_type in [RF_SINGLE_DIMMER, RF_DIMMER]:
            if device_value.ha_value is None:
                device_value.inels_set_value = DEVICE_TYPE_05_COMM_TEST
            else:
                out = round(device_value.ha_value.simple_light[0].brightness, -1)
                out = out if out < 100 else 100

                b = int((((0xFFFF - out) + 10000) * 1000) / 5)
                b = 0xFFFF - ((int(out/5)*1000) + 10000)
                b_str = f"{b:04X}"
                device_value.inels_set_value = f"01\n{b_str[0]}{b_str[1]}\n{b_str[2]}{b_str[3]}\n"
        elif device_value.inels_type is RF_DIMMER_RGB:
            if device_value.ha_value is None:
                device_value.inels_set_value = DEVICE_TYPE_13_COMM_TEST
            else:
                rgb = device_value.ha_value.rgb[0]
                device_value.inels_set_value = f"01\n{rgb.r:02X}\n{rgb.g:02X}\n{rgb.b:02X}\n{int(rgb.brightness*2.55):02X}\n00\n"
        elif device_value.inels_type is RF_LIGHT_BULB:
            if device_value.ha_value is None:
                device_value.inels_set_value = DEVICE_TYPE_13_COMM_TEST
            else:
                device_value.inels_set_value = f"0F\n00\n00\n00\n{round(device_value.ha_value.warm_light[0].brightness*2.55):02X}\n{round(device_value.ha_value.warm_light[0].relative_ct*2.55):02X}\n"
        elif device_value.inels_type is DA3_22M:
            # correct the values
            out1 = round(device_value.ha_value.light_coa_toa[0].brightness, -1)
            out1 = out1 if out1 < 100 else 100

            out2 = round(device_value.ha_value.light_coa_toa[1].brightness, -1)
            out2 = out2 if out2 < 100 else 100

            out1_str = f"{out1:02X}\n"
            out2_str = f"{out2:02X}\n"

            # EX: 00\n00\n00\n00\n64\n64\n # 100%/100%
            device_value.inels_set_value = "".join(["00\n" * 4, out1_str, out2_str])
        elif device_value.inels_type in [DAC3_04B, DAC3_04M]:
            set_val = "00\n" * 4
            for d in device_value.ha_value.aout:
                set_val += f"{d.brightness:02X}\n"
            device_value.inels_set_value = set_val
        elif device_value.inels_type in DCDA_33M:
            set_val = "00\n"*4
            for i in range(4):
                aout = device_value.ha_value.out[i].brightness
                set_val += f"{aout:02X}\n"
            device_value.inels_set_value = set_val
        elif device_value.inels_type is DA3_66M:
            set_val = "00\n"*4
            for i in range(4):
                out = device_value.ha_value.light_coa_toa[i].brightness
                out = out if out <= 100 else 100
                set_val += f"{out:02X}\n"
            set_val += "00\n"*4
            for i in range(4, 6):
                out = device_value.ha_value.light_coa_toa[i].brightness
                out = out if out <= 100 else 100
                set_val += f"{out:02X}\n"
            set_val += "00\n"*12
            device_value.inels_set_value = set_val
        elif device_value.inels_type is DALI_DMX_UNIT:
            set_val = "00\n"*4
            for i in range(4):
                out = device_value.ha_value.simple_light[i].brightness
                out = out if out <= 100 else 100
                set_val += f"{out:02X}\n"
            device_value.inels_set_value = set_val
        elif device_value.inels_type is DALI_DMX_UNIT_2:
            set_val = "00\n"*4
            for i in range(2):
                out = device_value.ha_value.warm_light[i].brightness
                out = min(out, 100)

                white = device_value.ha_value.warm_light[i].relative_ct
                white = min(white, 100)

                set_val += f"{out:02X}\n{white:02X}\n"
            device_value.inels_set_value = set_val

class CoverInelsHandler(InelsValueHandler):
    @staticmethod
    def update_inels_value(device_value: DeviceValue) -> None:
        if device_value.inels_type is RF_SHUTTERS:
            if device_value.ha_value is None:
                device_value.inels_set_value = DEVICE_TYPE_03_COMM_TEST
            else:
                shutter_set = RF_SHUTTER_STATE_SET[device_value.ha_value.shutters[0].state]
                device_value.inels_set_value = shutter_set + "00\n00\n"
        elif device_value.inels_type is RF_SHUTTER_UNIT:
            if device_value.ha_value is None:
                device_value.inels_set_value = DEVICE_TYPE_03_COMM_TEST
            else:
                if device_value.ha_value.shutters_with_pos[0].set_pos:
                    shutter_set = f"0A\n00\n{100 - round(device_value.ha_value.shutters_with_pos[0].position):02X}\n"
                else:
                    shutter_set = RF_SHUTTER_STATE_SET[device_value.ha_value.shutters_with_pos[0].state] + "00\n00\n"
                device_value.inels_set_value = shutter_set
        elif device_value.inels_type in [JA3_018M, JA3_014M]:
            device_value.inels_set_value = f"{''.join([SIMPLE_SHUTTER_STATE_SET[x.state] for x in device_value.ha_value.simple_shutters])}"

class ClimateInelsHandler(InelsValueHandler):
    @staticmethod
    def update_inels_value(device_value: DeviceValue) -> None:
        if device_value.inels_type is RF_WIRELESS_THERMOVALVE:
            required_temp = int(round(device_value.ha_value.climate.required * 2, 0))
            device_value.inels_set_value = f"00\n{required_temp:02X}\n00\n"
        elif device_value.inels_type is VIRT_CONTR:
            cc = device_value.ha_value.climate_controller

            current_temp = f"{int(cc.current * 100):08X}"
            current_temp = break_into_bytes(current_temp)
            current_temp.reverse()

            critical_temp = f"{int(cc.critical_temp * 100):08X}"
            critical_temp = break_into_bytes(critical_temp)
            critical_temp.reverse()

            manual_temp = f"{int((cc.required + cc.correction_temp) * 100):08X}"
            manual_temp = break_into_bytes(manual_temp)
            manual_temp.reverse()

            manual_cool_temp = f"{int((cc.required_cool + cc.correction_temp) * 100):08X}"
            manual_cool_temp = break_into_bytes(manual_cool_temp)
            manual_cool_temp.reverse()

            plan_in = "00\n"
            if cc.public_holiday > 0:
                plan_in = "80\n"
            elif cc.vacation:
                plan_in = "40\n"

            manual_in = 0
            if cc.current_preset == 5: #manual mode (in HA, this is the 4th preset, includes a default)
                manual_in = 7
            else:
                manual_in = cc.current_preset

            # off
            byte18 = 0  #TODO review this
            if cc.climate_mode != Climate_modes.Off:
                if cc.climate_mode == Climate_modes.Cool:
                    byte18 = 3
                else:
                    byte18 = 1

            set_val = "\n".join(current_temp) + "\n"
            set_val += "\n".join(critical_temp) + "\n"
            set_val += "\n".join(manual_temp) + "\n"
            set_val += "\n".join(manual_cool_temp) + "\n"
            set_val += plan_in
            set_val += f"{manual_in:02X}\n"
            set_val += f"{byte18:02X}\n"

            device_value.inels_set_value = set_val


class DeviceHandlerMapper:
    @staticmethod
    def get_handlers(device_type: str) -> Tuple[Optional[HAValueHandler], Optional[InelsValueHandler]]:
        if device_type is SWITCH:
            return (SwitchHAHandler, SwitchInelsHandler)
        elif device_type is NUMBER:
            return (NumberHAHandler, NumberInelsHandler)
        elif device_type is SENSOR:
            return (SensorHAHandler, None)
        elif device_type is LIGHT:
            return (LightHAHandler, LightInelsHandler)
        elif device_type is COVER:
            return (CoverHAHandler, CoverInelsHandler)
        elif device_type is CLIMATE:
            return (ClimateHAHandler, ClimateInelsHandler)
        elif device_type is BUTTON:
            return (ButtonHAHandler, None)

        return (None, None)

class DeviceValue:
    """Device value interpretation object."""

    def __init__(
        self,
        device_type: str,
        inels_type: str,
        inels_value: str = None,
        ha_value: Any = None,
        last_value: Any = None,
    ) -> None:
        self.device_type = device_type
        self.inels_type = inels_type
        self.__inels_status_value = inels_value
        self.__ha_value: Any = None
        self.__inels_set_value: str = ""
        self.__last_value = last_value
        self.__update_ha_value()
        self.__update_inels_value()

    def __update_ha_value(self) -> None:
        try:
            ha_handler, _ = DeviceHandlerMapper.get_handlers(self.device_type)
            if ha_handler:
                ha_handler.update_ha_value(self)
            else:
                _LOGGER.error("No handler found for HA update: %s", self.device_type)
        except Exception as e:
            status_value = self.inels_status_value.replace('\n', ' ') if self.inels_status_value else 'None'
            _LOGGER.error("Failed to update HA value for %s, status value was '%s': %s", self.device_type, status_value, str(e))
            self.__ha_value = dummy_val

    def __update_inels_value(self) -> None:
        try:
            if self.__ha_value is not dummy_val:
                _, inels_handler = DeviceHandlerMapper.get_handlers(self.device_type)
                if inels_handler:
                    inels_handler.update_inels_value(self)
                else:
                    _LOGGER.error("No handler found for Inels update: %s", self.device_type)
        except Exception as e:
            status_value = self.inels_status_value.replace('\n', ' ') if self.inels_status_value else 'None'
            _LOGGER.error("Error making 'set' value for device of type '%s', status value was '%s': %s", self.device_type, status_value, str(e))
            raise

    def trim_inels_status_values(self, selector: "dict[str, Any]", fragment: str, jointer: str) -> str:
        """Trim inels status from broker into the pure string."""
        data = self.__inels_status_value.split("\n")[:-1]

        selected = itemgetter(*selector[fragment])(data)
        return jointer.join(selected)

    def trim_inels_status_bytes(
        self, selector: "dict[str, Any]", fragment: str) -> "list[str]":
        """Split inels status section into its constituting bytes"""
        data = self.__inels_status_value.split("\n")[:-1]

        selected = itemgetter(*selector[fragment])(data)
        return selected

    @property
    def ha_value(self) -> Any:
        """Converted value from inels mqtt broker into
           the HA format

        Returns:
            Any: object to corespond to HA device
        """
        return self.__ha_value

    @ha_value.setter
    def ha_value(self, value: Any) -> None:
        """Set the HA value.

        Args:
            value (Any): The new value to set for the HA device.
        """
        # TODO: probably call self.__update_inels_value()
        self.__ha_value = value

    @property
    def inels_set_value(self) -> str:
        """Raw inels value for mqtt broker

        Returns:
            str: this is string format value for mqtt broker
        """
        return self.__inels_set_value

    @inels_set_value.setter
    def inels_set_value(self, value: str) -> None:
        """Set the raw inels value for mqtt broker.

        Args:
            value (str): The new value to set for the mqtt broker.
        """
        if not isinstance(value, str):
            raise ValueError("inels_set_value must be a string")
        self.__inels_set_value = value

    @property
    def inels_status_value(self) -> str:
        """Raw inels value from mqtt broker

        Returns:
            str: quated string from mqtt broker
        """
        return self.__inels_status_value

    @property
    def last_value(self) -> Any:
        """Get the last known value."""
        return self.__last_value

    @last_value.setter
    def last_value(self, value: Any) -> None:
        """Set the last known value."""
        self.__last_value = value
