"""Utility classes."""
from dataclasses import dataclass
import logging

from operator import itemgetter
from typing import Any, Dict

from inelsmqtt.mqtt_client import GetMessageType

from .const import (
    ADC3_60M_DATA,
    ANALOG_REGULATOR_SET_BYTES,
    BATTERY,
    BLUE,
    CARD_DATA,
    CARD_ID,
    DAC3_04_DATA,
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
    IM3_80B,
    IM3_140M,
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
)

#relay
@dataclass
class SimpleRelay():
    """Create simple relay"""
    is_on: bool

@dataclass
class Relay(SimpleRelay):
    """Create relay with overflow detection."""
    overflow: bool


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

class DeviceValue(object):
    """Device value interpretation object."""

    def __init__(
        self,
        device_type: str,
        inels_type: str,
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
        try:            
            if self.__device_type is SWITCH:  # outlet switch
                if self.__inels_type is RF_SINGLE_SWITCH:
                    if self.inels_status_value is None:
                        _LOGGER.info("inels_status_value was 'None' for %s", RF_SWITCHING_UNIT)
                        self.__inels_set_value = DEVICE_TYPE_07_COMM_TEST
                        self.__ha_value = None
                    else:
                        simple_relay: list[SimpleRelay] = []
                        simple_relay.append(
                            SimpleRelay(
                                is_on=int(self.__trim_inels_status_values(DEVICE_TYPE_02_DATA, RELAY, ""), 16) != 0
                            )
                        )

                        self.__ha_value = new_object(
                            simple_relay=simple_relay,
                        )

                        self.__inels_set_value = f"{(2 - (self.__ha_value.simple_relay[0].is_on)):02X}\n00\n"
                elif self.__inels_type is RF_SWITCHING_UNIT:
                    if self.inels_status_value is None:
                        _LOGGER.info("inels_status_value was 'None' for %s", RF_SWITCHING_UNIT)
                        self.__inels_set_value = DEVICE_TYPE_02_COMM_TEST
                        self.__ha_value = None
                    else:
                        simple_relay: list[SimpleRelay] = []
                        simple_relay.append(
                            SimpleRelay(
                                is_on=int(self.__trim_inels_status_values(DEVICE_TYPE_02_DATA, RELAY, ""), 16) != 0
                            )
                        )

                        self.__ha_value = new_object(
                            simple_relay=simple_relay,
                        )

                        self.__inels_set_value = f"{(2 - (self.__ha_value.simple_relay[0].is_on * 1)):02X}\n00\n00\n"
                elif self.__inels_type is RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR:
                    if self.inels_status_value is None:
                        _LOGGER.info("inels_status_value was 'None' for %s", RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR)
                        self.__inels_set_value = DEVICE_TYPE_07_COMM_TEST
                        self.__ha_value = None
                    else:
                        simple_relay: list[SimpleRelay] = []
                        simple_relay.append(
                            SimpleRelay(
                                is_on=int(self.__trim_inels_status_values(DEVICE_TYPE_07_DATA, RELAY, ""), 16) != 0
                            )
                        )
                        temp = self.__trim_inels_status_values(DEVICE_TYPE_07_DATA, TEMP_OUT, "")

                        self.__ha_value = new_object(
                            simple_relay=simple_relay,
                            temp_out=temp,
                        )

                        self.__inels_set_value = SWITCH_WITH_TEMP_SET[self.__ha_value.simple_relay[0].is_on]            
                elif self.__inels_type is SA3_01B:
                    re = []
                    re.append(int(self.__trim_inels_status_values(SA3_01B_DATA, RELAY, ""), 16) & 1 != 0) 
                    
                    temp = self.__trim_inels_status_values(SA3_01B_DATA, TEMP_IN, "")
                    
                    relay_overflow = []
                    relay_overflow.append(int(self.__trim_inels_status_values(SA3_01B_DATA, RELAY_OVERFLOW, ""),16) == 1)
                    
                    relay: list[Relay] = []
                    for i in range(len(re)):
                        relay.append(
                            Relay(
                                is_on=re[i],
                                overflow=relay_overflow[i],
                            )
                        )

                    self.__ha_value = new_object(
                        #re=re,
                        temp_in=temp,
                        #relay_overflow=relay_overflow

                        relay=relay
                    )
                    self.__inels_set_value = RELAY_SET[self.__ha_value.relay[0].is_on]
                elif self.__inels_type is SA3_02B:
                    simple_relay: list[SimpleRelay] = []
                    for relay in self.__trim_inels_status_bytes(SA3_02B_DATA, RELAY):
                        simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))
                    
                    temp_in = self.__trim_inels_status_values(SA3_02B_DATA, TEMP_IN, "")
                    self.__ha_value = new_object(
                        simple_relay=simple_relay,
                        temp_in=temp_in,
                    )
                    
                    set_val = ""
                    for r in simple_relay:
                        set_val += "07\n" if r.is_on else "06\n"
                    self.__inels_set_value=set_val
                elif self.__inels_type is SA3_02M: #TODO: generalize SA3_02M/04M/06M
                    simple_relay: list[SimpleRelay] = []
                    for relay in self.__trim_inels_status_bytes(SA3_02M_DATA, RELAY):
                        simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))
                    
                    digital_inputs = self.__trim_inels_status_values(
                        SA3_02M_DATA, SW, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>8b}"
                    sw = []
                    for i in range(2):
                        sw.append(digital_inputs[7 - i] == "1")
                        
                    self.__ha_value = new_object(
                        simple_relay=simple_relay,
                        sw=sw,
                    )
                    
                    set_val = ""
                    for r in simple_relay:
                        set_val += "07\n" if r else "06\n"
                    self.__inels_set_value=set_val
                elif self.__inels_type is SA3_04M:
                    simple_relay: list[SimpleRelay] = []
                    for relay in self.__trim_inels_status_bytes(SA3_04M_DATA, RELAY):
                        simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))
                    
                    digital_inputs = self.__trim_inels_status_values(
                        SA3_04M_DATA, SW, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>8b}"
                    sw = []
                    for i in range(4):
                        sw.append(digital_inputs[7 - i] == "1")
                        
                    self.__ha_value = new_object(
                        simple_relay=simple_relay,
                        sw=sw,
                    )
                    
                    set_val = ""
                    for r in simple_relay:
                        set_val += "07\n" if r.is_on else "06\n"
                    self.__inels_set_value=set_val
                elif self.__inels_type is SA3_06M:
                    simple_relay: list[SimpleRelay] = []
                    for relay in self.__trim_inels_status_bytes(SA3_06M_DATA, RELAY):
                        simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

                    digital_inputs = self.__trim_inels_status_values(
                        SA3_06M_DATA, SW, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>8b}"
                    sw = []
                    for i in range(6):
                        sw.append(digital_inputs[7 - i] == "1")
                        
                    self.__ha_value = new_object(
                        simple_relay=simple_relay,
                        sw=sw,
                    )
                    
                    set_val = ""
                    for r in simple_relay:
                        set_val += "07\n" if r.is_on else "06\n"
                    self.__inels_set_value=set_val
                elif self.__inels_type is SA3_012M:
                    simple_relay: list[SimpleRelay] = []
                    for relay in self.__trim_inels_status_bytes(SA3_012M_DATA, RELAY):
                        simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

                    digital_inputs = self.__trim_inels_status_values(
                        SA3_012M_DATA, SA3_012M, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>16b}"
                    
                    sw=[]
                    for i in range(8):
                        sw.append(digital_inputs[7 - i] == "1")
                    for i in range(4):
                        sw.append(digital_inputs[15 - i] == "1")
                    
                    self.__ha_value = new_object(
                        simple_relay=simple_relay,
                        sw=sw,
                    )
                    set_val = ""
                    for r in simple_relay:
                        set_val += "07\n" if r.is_on else "06\n"
                    self.__inels_set_value=set_val
                elif self.__inels_type is SA3_022M:
                    re=[]
                    for relay in self.__trim_inels_status_bytes(SA3_022M_DATA, RELAY):
                        re.append((int(relay, 16) & 1) != 0)
                    
                    overflows=[]
                    alerts = self.__trim_inels_status_values(
                        SA3_022M_DATA, RELAY_OVERFLOW, ""
                    )
                    alerts = f"0x{alerts}"
                    alerts = f"{int(alerts, 16):0>16b}"
                    for i in range(8): #0-7
                        overflows.append(alerts[7-i] == "1")
                    for i in range(8): #8-15
                        overflows.append(alerts[15-i] == "1")
                    
                    digital_inputs = self.__trim_inels_status_values(
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
                    for s in self.__trim_inels_status_bytes(SA3_022M_DATA, SHUTTER):
                        shutter.append((int(s, 16) & 1) != 0)
                    
                    valve=[]
                    for v in self.__trim_inels_status_bytes(SA3_022M_DATA, VALVE):
                        valve.append((int(v, 16) & 1) != 0)

                    self.__ha_value = new_object(
                        relay=relay,
                        shutter_motors=shutter,
                        valve=valve,
                        sw=sw,
                    )

                    set_val = ""
                    for r in self.ha_value.relay:
                        set_val += RELAY_SET[r.is_on]
                    for s in self.ha_value.shutter_motors:
                        set_val += RELAY_SET[s]
                    for v in self.ha_value.valve:
                        set_val += RELAY_SET[v]

                    self.__inels_set_value = set_val
                elif self.__inels_type is IOU3_108M:
                    re=[]
                    for relay in self.__trim_inels_status_bytes(IOU3_108M_DATA, RELAY):
                        re.append((int(relay, 16) & 1) != 0)
                    
                    temps = self.__trim_inels_status_values(IOU3_108M_DATA, TEMP_IN)
                    temps = [temps[0:4], temps[4:8]]
                    
                    digital_inputs = self.__trim_inels_status_values(
                        IOU3_108M_DATA, DIN, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>8b}"

                    din = []
                    for i in range(8):
                        din.append(digital_inputs[7-i] == '1')

                    digital_inputs = self.__trim_inels_status_values(
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

                    self.__ha_value = new_object(
                        relay=relay,
                        #re=re,
                        temps=temps,
                        din=din,
                        #relay_overflow=relay_overflow,
                    )
                elif self.__inels_type is RC3_610DALI: 
                    #aout
                    aout_brightness=[]
                    for a in self.__trim_inels_status_bytes(RC3_610DALI_DATA, AOUT):
                        aout_brightness.append(int(a, 16))

                    #relays
                    re=[]
                    for relay in self.__trim_inels_status_bytes(RC3_610DALI_DATA, RELAY):
                        re.append((int(relay, 16) & 1) != 0)
                    
                    #temperatures
                    temps = []
                    temp_bytes = self.__trim_inels_status_bytes(
                        RC3_610DALI_DATA,
                        TEMP_IN,
                    )
                    for i in range(int(len(temp_bytes)/2)):
                        temps.append(temp_bytes[2*i] + temp_bytes[2*i+1])
                    
                    #digital inputs
                    din=[]
                    digital_inputs = self.__trim_inels_status_values(
                        RC3_610DALI_DATA, DIN, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>8b}"
                    
                    for i in range(6):
                        din.append(digital_inputs[7-i] == "1")
                    
                    relay_overflow=[]
                    overflows = self.__trim_inels_status_values(
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
                    alerts = self.__trim_inels_status_values(
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
                            new_object(
                                brightness=aout_brightness[i],
                                aout_coa=aout_coa[i]
                            )
                        )

                    alert_dali_power = alerts[1] == "1"
                    alert_dali_communication = alerts[0] == "1"
                    
                    dali_raw = self.__trim_inels_status_bytes(
                        RC3_610DALI_DATA, DALI)
                    dali = []
                    for d in dali_raw:
                        dali.append(
                            new_object(
                                brightness=int(d, 16),
                                alert_dali_communication=alert_dali_communication,
                                alert_dali_power=alert_dali_power,
                            )
                        )
                    
                    self.__ha_value = new_object(
                        relay=relay,
                        temps=temps,
                        din=din,
                        aout=aout,
                        dali=dali,
                    )
                elif self.__inels_type is FA3_612M:
                    inputs = self.__trim_inels_status_values(FA3_612M_DATA, FA3_612M, "")
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
                    
                    overflows = self.__trim_inels_status_values(FA3_612M_DATA, RELAY_OVERFLOW, "")
                    overflows = f"0x{overflows}"
                    overflows = f"{int(overflows, 16):0>8b}"
                    
                    #relay_overflow = []
                    #for i in range(8):
                    #    relay_overflow.append(overflows[7-i] == "1")
                    
                    aout=[]
                    for a in self.__trim_inels_status_bytes(FA3_612M_DATA, AOUT):
                        aout.append(
                            new_object(brightness=int(a, 16))
                        )
                    
                    re=[]
                    for relay in self.__trim_inels_status_bytes(FA3_612M_DATA, RELAY):
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
                    ain_bytes = self.__trim_inels_status_bytes(
                        FA3_612M_DATA,
                        AIN,
                    )
                    for i in range(int(len(ain_bytes)/4)):
                        ains.append(ain_bytes[4*i] + ain_bytes[4*i+1] + ain_bytes[4*i+2] + ain_bytes[4*i+3])

                    last_status_val=self.__inels_status_value

                    self.__ha_value = new_object(
                        din=din,
                        aout_coa=aout_coa,
                        sw=sw,
                        aout=aout,
                        valves=valves,
                        fan_speed=fan_speed,
                        heating_out=heating_out,
                        ains=ains,
                        last_status_val=last_status_val,
                    )
                elif self.__inels_type in [GCR3_11, GCH3_31]:
                    state = self.__trim_inels_status_values(CARD_DATA, STATE, "")
                    state = f"0x{state}"
                    state = f"{int(state, 16):0>16b}"

                    simple_relay: list[SimpleRelay] = []
                    simple_relay.append(SimpleRelay(is_on=state[5] == "1"))
                    
                    card_present = (state[4] == "1")

                    card_id = self.__trim_inels_status_values(CARD_DATA, CARD_ID, "")
                    card_id_int = int(card_id, 16)
                    #if card removed before 
                    if card_id_int == 0 and self.__last_value is not None:
                        card_id = self.__last_value.card_id

                    interface = [
                        state[0] == "1",
                        state[12] == "1",
                        state[10] == "1"
                    ]

                    light_in = self.__trim_inels_status_values(CARD_DATA, LIGHT_IN, "")

                    temp_in = self.__trim_inels_status_values(CARD_DATA, TEMP_IN, "")
                    self.__ha_value = new_object(
                        simple_relay=simple_relay,
                        interface=interface,
                        temp_in=temp_in,
                        card_present=card_present,
                        card_id=card_id,
                    )
            elif self.__device_type is SENSOR:  # temperature sensor
                if self.__inels_type is RF_TEMPERATURE_INPUT:
                    battery = int(self.__trim_inels_status_values(DEVICE_TYPE_10_DATA, BATTERY, ""), 16)
                    temp_in = self.__trim_inels_status_values(DEVICE_TYPE_10_DATA, TEMP_IN, "")
                    temp_out = self.__trim_inels_status_values(DEVICE_TYPE_10_DATA, TEMP_OUT, "")

                    self.__ha_value = new_object(
                        low_battery=(battery!=0),
                        temp_in=temp_in,
                        temp_out=temp_out,
                    )
                elif self.__inels_type is RF_THERMOSTAT:
                    temp_in = int(self.__trim_inels_status_values(DEVICE_TYPE_12_DATA, TEMP_IN, ""), 16) * 0.5
                    battery = int(self.__trim_inels_status_values(DEVICE_TYPE_12_DATA, BATTERY, ""), 16)
                    # has 2 values, 0x80 and 0x81 on which 0x81 means low battery

                    self.__ha_value = new_object(
                        low_battery=(battery == 0x81),
                        temp_in=temp_in,
                    )
                elif self.__inels_type is RF_FLOOD_DETECTOR:
                    state = self.__trim_inels_status_values(DEVICE_TYPE_15_DATA, STATE, "")
                    state = f"0x{state}"
                    state = f"{int(state, 16):0>8b}"

                    ain = int(self.__trim_inels_status_values(DEVICE_TYPE_15_DATA, AIN, ""), 16) /100

                    low_battery=state[0] == "1"
                    flooded=state[7]=="1"
                    ains=[]
                    ains.append(ain)
                    self.__ha_value = new_object(
                        low_battery=low_battery,
                        flooded=flooded,
                        ains=ains,
                    )
                elif self.__inels_type is RF_DETECTOR:
                    state = self.__trim_inels_status_values(
                        DEVICE_TYPE_16_DATA, STATE, "")
                    state = f"0x{state}"
                    state = f"{int(state, 16):0>8b}"

                    low_battery=state[3] == "1"
                    detected=state[4] == "1"

                    self.__ha_value = new_object(
                        low_battery=low_battery,
                        detected=detected,
                    )
                elif self.__inels_type is RF_MOTION_DETECTOR:
                    state = self.__trim_inels_status_values(
                        DEVICE_TYPE_16_DATA, STATE, "")
                    state = f"0x{state}"
                    state = f"{int(state, 16):0>8b}"

                    low_battery=state[3] == "1"
                    motion=state[4] == "1"

                    self.__ha_value = new_object(
                        low_battery=low_battery,
                        motion=motion,
                    )
                elif self.__inels_type is RF_TEMPERATURE_HUMIDITY_SENSOR:
                    battery = int(self.__trim_inels_status_values(DEVICE_TYPE_29_DATA, BATTERY, ""), 16)
                    temp_in = self.__trim_inels_status_values(DEVICE_TYPE_29_DATA, TEMP_IN, "")
                    humidity = int(self.__trim_inels_status_values(DEVICE_TYPE_29_DATA, HUMIDITY, ""), 16)

                    self.__ha_value = new_object(
                        low_battery=(battery!=0),
                        temp_in=temp_in,
                        humidity=humidity,
                    )
                elif self.__inels_type is GRT3_50:
                    digital_inputs = self.__trim_inels_status_values(
                        GRT3_50_DATA, GRT3_50, "")
                    digital_inputs_hex_str = f"0x{digital_inputs}"
                    digital_inputs_bin_str = f"{int(digital_inputs_hex_str, 16):0>8b}"
                    
                    plusminus = self.__trim_inels_status_values(
                        GRT3_50_DATA, PLUS_MINUS_BUTTONS, "")
                    plusminus = f"0x{plusminus}"
                    plusminus = f"{int(plusminus, 16):0>8b}"
                    
                    temp_in = self.__trim_inels_status_values(GRT3_50_DATA, TEMP_IN, "")
                        
                    light_in = self.__trim_inels_status_values(GRT3_50_DATA, LIGHT_IN, "")

                    ain = self.__trim_inels_status_values(GRT3_50_DATA, AIN, "")
                    
                    humidity = self.__trim_inels_status_values(GRT3_50_DATA, HUMIDITY, "")

                    dewpoint = self.__trim_inels_status_values(GRT3_50_DATA, DEW_POINT, "")


                    self.__ha_value = new_object(
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
                elif self.__inels_type in [WSB3_20, WSB3_40]:
                    switches = self.__trim_inels_status_values(
                        WSB3_240_DATA, SW, "")
                    switches = f"0x{switches}"
                    switches = f"{int(switches, 16):0>8b}"
                    
                    digital_inputs = self.__trim_inels_status_values(
                        WSB3_240_DATA, DIN, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>8b}"
                    
                    interface=[] #up/down buttons
                    for i in range(WSB3_AMOUNTS[self.__inels_type]):
                        interface.append(switches[7 - i] == "1")
                    
                    din=[]
                    for i in range(2):
                        din.append(digital_inputs[7 - i] == "1")

                    temp_in=self.__trim_inels_status_values(
                        WSB3_240_DATA, TEMP_IN, ""
                    )
                    ain=self.__trim_inels_status_values(
                        WSB3_240_DATA, AIN, ""
                    )
                    
                    self.__ha_value = new_object(
                        interface=interface,
                        din=din,
                        temp_in=temp_in,
                        ain=ain,
                    )
                elif self.__inels_type in [WSB3_20H, WSB3_40H]:
                    switches = self.__trim_inels_status_values(
                        WSB3_240HUM_DATA, SW, "")
                    switches = f"0x{switches}"
                    switches = f"{int(switches, 16):0>8b}"
                    
                    
                    digital_inputs = self.__trim_inels_status_values(
                        WSB3_240HUM_DATA, DIN, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>8b}"
                    interface=[] #up/down buttons
                    din=[]
                    for i in range(WSB3_AMOUNTS[self.__inels_type]):
                        interface.append(switches[7 - i] == "1")
                    for i in range(2):
                        din.append(digital_inputs[7 - i] == "1")
                
                    temp_in = self.__trim_inels_status_values(WSB3_240HUM_DATA, TEMP_IN, "")
                        
                    ain = self.__trim_inels_status_values(WSB3_240HUM_DATA, AIN, "")
                    
                    humidity = self.__trim_inels_status_values(WSB3_240HUM_DATA, HUMIDITY, "")

                    dewpoint = self.__trim_inels_status_values(WSB3_240HUM_DATA, DEW_POINT, "")

                    self.__ha_value = new_object(
                        interface=interface,
                        din=din,
                        temp_in=temp_in,
                        ain=ain,
                        humidity=humidity,
                        dewpoint=dewpoint,
                    )
                elif self.__inels_type in [IM3_20B, IM3_40B]:
                    binary_input = []
                    inputs = self.__trim_inels_status_values(IM3_240B_DATA, IN, "")
                    inputs = f"0x{inputs}"
                    inputs = f"{int(inputs, 16):0>8b}"
                    for i in range(IM3_AMOUNTS[self.__inels_type]):
                        binary_input.append(int(inputs[7-2*i-1] + inputs[7-2*i], 2))
                    
                    temp = self.__trim_inels_status_values(IM3_240B_DATA, TEMP_IN, "")
                    self.__ha_value = new_object(
                        input=binary_input,
                        temp_in=temp,
                    )
                elif self.__inels_type is IM3_80B:
                    binary_input = []
                    binary_input2 = []
                    inputs = self.__trim_inels_status_values(IM3_80B_DATA, IN, "")
                    inputs = f"0x{inputs}"
                    inputs = f"{int(inputs, 16):0>16b}"
                    for i in range(4):
                        binary_input.append(int(inputs[7-2*i-1] + inputs[7-2*i], 2))
                        binary_input2.append(int(inputs[15-2*i-1] + inputs[15-2*i], 2))
                    binary_input.extend(binary_input2)
                    
                    temp = self.__trim_inels_status_values(IM3_80B_DATA, TEMP_IN, "")
                    self.__ha_value = new_object(
                        input=binary_input,
                        temp=temp,
                    )
                elif self.__inels_type is IM3_140M:
                    binary_input = []
                    binary_input2 = []
                    binary_input3 = []
                    inputs = self.__trim_inels_status_values(IM3_140M_DATA, IN, "")
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
                    
                    self.__ha_value = new_object(
                        input=binary_input
                    )
                elif self.__inels_type is DMD3_1:
                    light_in = self.__trim_inels_status_values(DMD3_1_DATA, LIGHT_IN, "")
                    temp_in = self.__trim_inels_status_values(DMD3_1_DATA, TEMP_IN, "")    
                    humidity = self.__trim_inels_status_values(DMD3_1_DATA, HUMIDITY, "")
                    motion = self.__trim_inels_status_values(
                        DMD3_1_DATA, DMD3_1, "")
                    motion = f"0x{motion}"
                    motion = f"{int(motion, 16):0>8b}"

                    motion=motion[7] == "1"

                    self.__ha_value = new_object(
                        light_in=light_in,
                        temp_in=temp_in,
                        humidity=humidity,
                        motion=motion,
                    )
                elif self.__inels_type is ADC3_60M:
                    ains=[]
                    ain_bytes = self.__trim_inels_status_bytes(
                        ADC3_60M_DATA, AIN,
                    )
                    for i in range(int(len(ain_bytes)/4)):
                        ains.append(ain_bytes[4*i] + ain_bytes[4*i+1] + ain_bytes[4*i+2] + ain_bytes[4*i+3])

                    self.__ha_value = new_object(
                        ains=ains,
                    )
                elif self.__inels_type in [TI3_10B, TI3_40B, TI3_60M]:
                    temps = []
                    temp_bytes = self.__trim_inels_status_bytes(
                        INELS_DEVICE_TYPE_DATA_STRUCT_DATA[self.__inels_type],
                        TEMP_IN,
                    )
                    
                    for i in range(int(len(temp_bytes)/2)):
                        temps.append(temp_bytes[2*i] + temp_bytes[2*i+1])
                    
                    self.__ha_value = new_object(
                        temps=temps
                    )
                elif self.__inels_type in IDRT3_1:
                    inputs = self.__trim_inels_status_values(IDRT3_1_DATA, SW, "")
                    inputs = f"0x{inputs}"
                    inputs = f"{int(inputs, 16):0>8b}"
                    
                    interface = []
                    din = []
                    for i in range(2):
                        din.append(inputs[7-i]=="1")
                        interface.append(inputs[5-i]=="1")
                    
                    temp_in = self.__trim_inels_status_values(IDRT3_1_DATA, TEMP_IN, "")
                    temp_out = self.__trim_inels_status_values(IDRT3_1_DATA, TEMP_OUT, "")
                    
                    self.__ha_value = new_object(
                        interface=interface,
                        din=din,
                        temp_in=temp_in,
                        temp_out=temp_out,
                    )
            elif self.__device_type is LIGHT:  # dimmer
                if self.__inels_type in [RF_SINGLE_DIMMER, RF_DIMMER]:
                    if self.inels_status_value is None:
                        _LOGGER.info("inels_status_value was None for RFDAC")
                        self.__inels_set_value = DEVICE_TYPE_05_COMM_TEST
                        self.__ha_value = None
                    else:
                        brightness = int(self.__trim_inels_status_values(DEVICE_TYPE_05_DATA, RF_DIMMER, ""), 16)
                        brightness = int((((0xFFFF - brightness) - 10000)/1000)*5)
                        brightness = round(brightness, -1)

                        simple_light = []
                        simple_light.append(
                            new_object(brightness=brightness)
                        )
                        self.__ha_value = new_object(simple_light=simple_light)
                elif self.__inels_type is RF_DIMMER_RGB:
                    if self.inels_status_value is None:
                        _LOGGER.info("inels_status_value was None for %s", RF_DIMMER_RGB)
                        self.__inels_set_value = DEVICE_TYPE_13_COMM_TEST
                        self.__ha_value = None
                    else:
                        red = int(self.__trim_inels_status_values(DEVICE_TYPE_06_DATA, RED, ""), 16)
                        green = int(self.__trim_inels_status_values(DEVICE_TYPE_06_DATA, GREEN, ""), 16)
                        blue = int(self.__trim_inels_status_values(DEVICE_TYPE_06_DATA, BLUE, ""), 16)
                        brightness = int(int(self.__trim_inels_status_values(DEVICE_TYPE_06_DATA, OUT, ""), 16)* 100.0/255.0)

                        rgb=[]
                        rgb.append(
                            new_object(
                                r=red,
                                g=green,
                                b=blue,
                                brightness=brightness,
                            )
                        )

                        self.__ha_value=new_object(
                            rgb=rgb
                        )
                elif self.__inels_type is RF_LIGHT_BULB:
                    if self.inels_status_value is None:
                        _LOGGER.info("inels_status_value was None for %s", RF_LIGHT_BULB)
                        self.__inels_set_value = DEVICE_TYPE_13_COMM_TEST
                        self.__ha_value = None
                    else:
                        simple_light = []
                        simple_light.append(new_object(brightness=int(
                            int(self.__trim_inels_status_values(DEVICE_TYPE_13_DATA, OUT, ""), 16) * 100.0/255.0
                        )))


                        self.__ha_value=new_object(simple_light=simple_light)
                elif self.__inels_type is DA3_22M:
                    temp = self.__trim_inels_status_values(DA3_22M_DATA, TEMP_IN, "")

                    state = self.__trim_inels_status_values(
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
                        self.__trim_inels_status_values(
                            DA3_22M_DATA, DIM_OUT_1, ""
                        ), 16
                    )

                    out2 = int(
                        self.__trim_inels_status_values(
                            DA3_22M_DATA, DIM_OUT_2, ""
                        ), 16
                    )
                    out1 = out1 if out1 <= 100 else 100
                    out2 = out2 if out2 <= 100 else 100
                    out = [out1, out2]

                    light_coa_toa = []
                    for i in range(2):
                        light_coa_toa.append(
                            new_object(
                                brightness=out[i],
                                thermal_alert=toa[i],
                                current_alert=coa[i],
                            )
                        )

                    self.__ha_value = new_object(
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
                    for i in range(len(self.__ha_value.light_coa_toa)):
                        set_val +=  f"{self.__ha_value.light_coa_toa[i].brightness:02X}\n"
                    self.__inels_set_value = set_val
                elif self.__inels_type is DAC3_04B:
                    temp_out = self.__trim_inels_status_values(DAC3_04_DATA, TEMP_OUT, "")
                    
                    aout_alert = int(self.__trim_inels_status_values(DAC3_04_DATA, ALERT, ""), 16) != 0

                    aout_str = self.__trim_inels_status_bytes(DAC3_04_DATA, OUT)
                    aout = []
                    for d in aout_str:
                        d = int(d, 16)
                        d = d if d <= 100 else 100
                        aout.append(
                            new_object(
                                brightness=d,
                                aout_coa=aout_alert,
                            )
                        )
                    
                    self.__ha_value = new_object(
                        temp_out=temp_in,
                        aout=aout,
                    )

                    set_val = "00\n" * 4
                    for d in aout:
                        set_val += f"{d.brightness:02X}\n"
                elif self.__inels_type is DAC3_04M:
                    temp_out = self.__trim_inels_status_values(DAC3_04_DATA, TEMP_OUT, "")

                    aout_alert = self.__trim_inels_status_values(DAC3_04_DATA, ALERT, "")
                    aout_coa=[]
                    for i in range(4):
                        aout_coa.append(aout_alert[6-i] == "1") #skip first bit

                    aout_str = self.__trim_inels_status_bytes(DAC3_04_DATA, OUT)
                    aout_val = []
                    for d in aout_str:
                        d = int(d, 16)
                        d = d if d <= 100 else 100
                        aout_val.append(d)

                    aout=[]
                    for i in range(4):
                        aout.append(
                            new_object(
                                brightness=aout_val[i],
                                aout_coa=aout_coa[i],
                            )
                        )
                    
                    self.__ha_value = new_object(
                        temp_out=temp_in,
                        aout=aout,
                    )

                    set_val = "00\n" * 4
                    for d in aout:
                        set_val += f"{d.brightness:02X}\n"
                elif self.__inels_type in DCDA_33M:
                    digital_inputs = self.__trim_inels_status_values(DCDA_33M_DATA, ALERT, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>8b}"

                    sw = []
                    coa = []
                    for i in range(3):
                        sw.append(digital_inputs[7-i] == "1")
                        coa.append(digital_inputs[4-i] == "1")
                    
                    coa.append(False) #only 3 alerts, so I fake the last one

                    aout_val=[]
                    aouts = self.__trim_inels_status_bytes(DCDA_33M_DATA, OUT)
                    for i in range(len(aouts)):
                        brightness = int(i, 16)
                        brightness = brightness if brightness > 100 else 100
                        aout_val.append(brightness)

                    aout=[]
                    for i in range(4):
                        aout.append(
                            brightness=aout_val[i],
                            aout_coa=coa[i],
                        )


                    self.__ha_value = new_object(
                        sw=sw,
                        aout=aout,
                    )

                    set_val = "00\n"*4
                    for i in range(4):
                        aout_val = aout[i].brightness
                        set_val += f"{aout_val:02X}\n"
                    self.__inels_set_value = set_val
                elif self.__inels_type is DA3_66M:
                    state = self.__trim_inels_status_values(
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
                    
                    switches = self.__trim_inels_status_values(
                        DA3_66M_DATA, SW, ""
                    )
                    switches = f"0x{switches}"
                    switches = f"{int(switches, 16):0>8b}"
                    
                    digital_inputs = self.__trim_inels_status_values(
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
                    outs = self.__trim_inels_status_bytes(
                        DA3_66M_DATA, OUT
                    )
                    
                    for o in outs:
                        out.append(int(o, 16))

                    light_coa_toa=[]
                    for i in range(6):
                        light_coa_toa.append(
                            new_object(
                                brightness=out[i],
                                toa=toa[i],
                                coa=coa[i],
                            )
                        )

                    self.__ha_value = new_object(
                        sw=sw,
                        din=din,
                        light_coa_toa=light_coa_toa,
                    )
                    
                    set_val = "00\n"*4
                    for i in range(4):
                        set_val += f"{self.__ha_value.light_coa_toa[i].brightness:02X}\n"
                    set_val += "00\n"*4
                    for i in range(4, 6):
                        set_val += f"{self.__ha_value.light_coa_toa[i].brightness:02X}\n"
                    set_val += "00\n"*12
                    self.__inels_set_value = set_val
            elif self.__device_type is COVER:  # Shutters
                if self.__inels_type is RF_SHUTTERS:
                    if self.inels_status_value is None:
                        _LOGGER.info("inels_status_value was 'None' for %s", RF_SHUTTERS)
                        self.__inels_set_value = DEVICE_TYPE_03_COMM_TEST
                        self.__ha_value = None
                    else:
                        # shutters True -> closed, False -> open
                        shutters = []
                        shutter_val = int(self.__trim_inels_status_values(DEVICE_TYPE_03_DATA, SHUTTER, ""), 16)

                        # So as to continue driving it down if it aisn't closed
                        # and continue opening it if it isn't open
                        if shutter_val not in [Shutter_state.Open, Shutter_state.Closed]: 
                            shutter_val = self.__last_value.shutters[0].state
                        shutters.append(
                            new_object(state=shutter_val)
                        )

                        self.__ha_value = new_object(
                            shutters=shutters,
                        )

                        self.__inels_set_value = f"{RF_SHUTTER_STATE_SET[shutters[0].state]}\n00\n00\n"
                elif self.__inels_type is RF_SHUTTER_UNIT:
                    if self.inels_status_value is None:
                        _LOGGER.info("inels_status_value was 'None' for %s", RF_SHUTTER_UNIT)
                        self.__inels_set_value = DEVICE_TYPE_03_COMM_TEST
                        self.__ha_value = None
                    else:
                        shutters_with_pos = []
                        shutter_val = int(self.__trim_inels_status_values(DEVICE_TYPE_21_DATA, SHUTTER, ""))
                        shutter_val = ((shutter_val >> 1) & 1) | (shutter_val & 1) << 1 #swap bit 0 with bit 1

                        if (self.__last_value is not None) and (shutter_val not in [Shutter_state.Open, Shutter_state.Closed]):
                            shutter_val = self.__last_value.shutters[0].state

                        position = int(self.__trim_inels_status_values(DEVICE_TYPE_21_DATA, POSITION, ""), 16) * 100.0 / 255.0

                        shutters_with_pos.append(
                            new_object(
                                state=shutter_val,
                                position=position,
                                set_pos=False,
                            )
                        )

                        self.__ha_value = new_object(
                            shutters_with_pos=shutters_with_pos,
                        )
                        self.__inels_set_value = f"{RF_SHUTTER_STATE_SET[shutters_with_pos[0].state]}\n00\n00\n"
            elif self.__device_type is CLIMATE:  # thermovalve
                if self.__inels_type is RF_WIRELESS_THERMOVALVE:
                    # fetches all the status values and compacts them into a new object
                    temp_current_hex = self.__trim_inels_status_values(
                        DEVICE_TYPE_09_DATA, CURRENT_TEMP, ""
                    )
                    temp_current = int(temp_current_hex, 16) * 0.5
                    temp_required_hex = self.__trim_inels_status_values(
                        DEVICE_TYPE_09_DATA, REQUIRED_TEMP, ""
                    )
                    temp_required = int(temp_required_hex, 16) * 0.5
                    battery = int(self.__trim_inels_status_values(
                        DEVICE_TYPE_09_DATA, BATTERY, ""
                    ), 16)
                    open_to_hex = self.__trim_inels_status_values(
                        DEVICE_TYPE_09_DATA, OPEN_IN_PERCENTAGE, ""
                    )
                    open_to_percentage = int(open_to_hex, 16) * 0.5

                    self.__ha_value = new_object(
                        low_battery=(battery!=0),
                        climate=new_object(
                            current=temp_current,
                            required=temp_required,
                            open_in_percentage=open_to_percentage,
                        )
                    )             
                elif self.__inels_type is VIRT_CONTR:
                    temp_current = self.__trim_inels_status_values(
                        DEVICE_TYPE_166_DATA, CURRENT_TEMP, ""
                    )
                    temp_critical_max = int(self.__trim_inels_status_values(
                        DEVICE_TYPE_166_DATA, CRITICAL_MAX_TEMP, ""
                    ), 16) / 100
                    temp_required_heat = self.__trim_inels_status_values(
                        DEVICE_TYPE_166_DATA, REQUIRED_HEAT_TEMP, ""
                    )
                    temp_max = self.__trim_inels_status_values(
                        DEVICE_TYPE_166_DATA, MAX_TEMP, ""
                    )
                    temp_critical_min = self.__trim_inels_status_values(
                        DEVICE_TYPE_166_DATA, CRITICAL_MIN_TEMP, ""
                    )
                    temp_required_cool = self.__trim_inels_status_values(
                        DEVICE_TYPE_166_DATA, REQUIRED_COOL_TEMP, ""
                    )
                    temp_correction = (self.__trim_inels_status_values(
                        DEVICE_TYPE_166_DATA, TEMP_CORRECTION, ""
                    ), 16)/100
                    holiday_mode = int(self.__trim_inels_status_values(
                        DEVICE_TYPE_166_DATA, PUBLIC_HOLIDAY, ""
                    ), 16)
                    control_mode = int(self.__trim_inels_status_values(
                        DEVICE_TYPE_166_DATA, CONTROL_MODE, ""
                    ))
                    
                    binary_vals = self.__trim_inels_status_values(
                        DEVICE_TYPE_166_DATA, VIRT_CONTR, ""
                    )
                    binary_vals = f"0x{binary_vals}"
                    binary_vals = f"{int(binary_vals, 16):0>8b}"
                    
                    controller_on = binary_vals[7] == "1"
                    manual_mode = binary_vals[6] == "1"
                    heat_mode = binary_vals[5] == "1"
                    cool_mode = binary_vals[4] == "1"
                    vacation = binary_vals[3] == "1"
                    regulator_disabled = binary_vals[2] == "1"

                    control_mode = int(control_mode)
                    #0 -> user control (?)
                    #1 -> 2 temp
                    #2 -> single temp

                    current_mode = Climate_modes.Off 
                    if controller_on: #TODO review all of this
                        current_mode = Climate_modes.Heat_cool #both manual and automatic 2 temperatures will be heat_cool
                        if control_mode == 2: # 1 temp
                            if temp_current > temp_required_heat:
                                current_mode = Climate_modes.Cool
                            else:
                                current_mode = Climate_modes.Heat

                    current_action = Climate_action.Off
                    if controller_on:
                        current_action = Climate_action.Idle
                        if heat_mode:
                            current_action = Climate_action.Heating
                        elif cool_mode:
                            current_action = Climate_action.Cooling

                    self.__ha_value = new_object(
                        climate_controller=new_object(
                            current=temp_current, #current_temperature
                            
                            required=temp_required_heat, #target_temperature
                            required_heat=temp_required_heat, #target_temperature_high
                            required_cool=temp_required_cool, #target_temperature_low

                            current_mode=current_mode, #hvac_mode: Off/Heat_cool/Heat/Cool
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
                        ),
                    )
                elif self.__inels_type is VIRT_HEAT_REG:
                    state=int(self.__trim_inels_status_values(
                        VIRT_REG_DATA, STATE, ""
                    ), 16)
                    
                    reg=self.__trim_inels_status_values(
                        VIRT_REG_DATA, VIRT_HEAT_REG, ""
                    )
                    reg = f"{int(reg, 16):0>8b}"

                    heat_reg=reg[7] == "1"
                    heat_source = reg[6] == "1"
                    
                    self.__ha_value = new_object(
                        heating_out = heat_reg
                    )
                elif self.__inels_type is VIRT_COOL_REG:
                    state=int(self.__trim_inels_status_values(
                        VIRT_REG_DATA, STATE, ""
                    ), 16)
                    
                    reg=self.__trim_inels_status_values(
                        VIRT_REG_DATA, VIRT_HEAT_REG, ""
                    )
                    reg = f"{int(reg, 16):0>8b}"

                    cool_reg=reg[7] == "1"
                    cool_source = reg[6] == "1"
                    
                    self.__ha_value = new_object(
                        cooling_out=cool_reg,
                    )
            elif self.__device_type is BUTTON:
                if self.__inels_type is RF_CONTROLLER:
                    if self.__inels_status_value is None:
                        #No connection can be made, so just communicate low battery
                        self.__ha_value = new_object(
                            low_battery = True,
                            btn = [False, False, False, False]
                        )
                    else:
                        state = self.__trim_inels_status_values(DEVICE_TYPE_19_DATA, STATE, "")
                        state_hex_str = f"0x{state}"  # 0xSTATE
                        # interpret the value and write it in binary
                        state_bin_str = f"{int(state_hex_str, 16):0>8b}"

                        # read which button was last pressed
                        identity = self.__trim_inels_status_values(
                            DEVICE_TYPE_19_DATA, IDENTITY, ""
                        )


                        #NEW
                        low_battery = state_bin_str[4] == "1" # 1 -> low
                        pressed = state_bin_str[3] == "1"
                        if self.__last_value is None:
                            btn = [
                                False,
                                False,
                                False,
                                False,
                            ]
                        else:
                            btn = self.__last_value.btn

                        if identity in BUTTON_NUMBER:
                            number = BUTTON_NUMBER[identity]
                            if number <= 4:
                                btn[number-1] = pressed

                        self.__ha_value = new_object(
                            low_battery=low_battery,
                            btn=btn
                        )
                elif self.__inels_type is RF_2_BUTTON_CONTROLLER:
                    if self.__inels_status_value is None:
                        self.__ha_value = new_object(
                            low_battery=True,
                            btn=[False, False]
                        )
                    else:
                        state = self.__trim_inels_status_values(DEVICE_TYPE_19_DATA, STATE, "")
                        state = f"0x{state}"  # 0xSTATE
                        state = f"{int(state, 16):0>8b}"

                        identity = self.__trim_inels_status_values(DEVICE_TYPE_19_DATA, IDENTITY, "")

                        low_battery = state[4] == "1"
                        pressed = state[3] == "1"
                        if self.__last_value is None:
                            btn = [False, False]
                        else:
                            btn = self.__last_value.btn
                        
                        if identity in BUTTON_NUMBER:
                            number = BUTTON_NUMBER[identity]
                            if number <= 2:
                                btn[number-1] = pressed

                        self.__ha_value = new_object(
                            low_battery=low_battery,
                            btn=btn,
                        )
                elif self.__inels_type is GSB3_90SX:
                    digital_inputs = self.__trim_inels_status_values(
                        GSB3_90SX_DATA, GSB3_90SX, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>16b}"
                    
                    
                    temp = self.__trim_inels_status_values(
                        GSB3_90SX_DATA, TEMP_IN, "")

                    light_in = self.__trim_inels_status_values(
                        GSB3_90SX_DATA, LIGHT_IN, "")

                    ain = self.__trim_inels_status_values(
                        GSB3_90SX_DATA, AIN, "")

                    humidity = self.__trim_inels_status_values(
                        GSB3_90SX_DATA, HUMIDITY, "")

                    dewpoint = self.__trim_inels_status_values(
                        GSB3_90SX_DATA, DEW_POINT, "")

                    self.__ha_value = new_object(
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
                elif self.__inels_type in [GSB3_20SX, GSB3_40SX, GSB3_60SX, GBP3_60]:
                    switches = self.__trim_inels_status_values(
                        GLASS_CONTROLLER_DATA, SW, "")
                    switches = f"0x{switches}"
                    switches = f"{int(switches, 16):0>8b}"
                    
                    digital_inputs = self.__trim_inels_status_values(
                        GLASS_CONTROLLER_DATA, SW, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>8b}"
                    
                    interface = []
                    for i in range(GSB3_AMOUNTS[self.__inels_type]):
                        interface.append(switches[7-i] == "1")
                    
                    din = []
                    for i in range(2):
                        din.append(digital_inputs[7-i] == "1")
                    
                    temp = self.__trim_inels_status_values(
                        GLASS_CONTROLLER_DATA, TEMP_IN, "")

                    light_in = self.__trim_inels_status_values(
                        GLASS_CONTROLLER_DATA, LIGHT_IN, "")

                    ain = self.__trim_inels_status_values(
                        GLASS_CONTROLLER_DATA, AIN, "")

                    self.__ha_value = new_object(
                        interface=interface,
                        din=din,
                        # temperature
                        temp_in=temp,

                        # light in
                        light_in=light_in,

                        # AIN
                        ain=ain,
                    )
                elif self.__inels_type is GSP3_100:
                    switches = self.__trim_inels_status_values(
                        GLASS_CONTROLLER_DATA, SW, "")
                    switches = f"0x{switches}"
                    switches = f"{int(switches, 16):0>8b}"
                    
                    digital_inputs = self.__trim_inels_status_values(
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
                    
                    temp_in = self.__trim_inels_status_values(GLASS_CONTROLLER_DATA, TEMP_IN, "")
                    light_in = self.__trim_inels_status_values(GLASS_CONTROLLER_DATA, LIGHT_IN, "")
                    ain = self.__trim_inels_status_values(GLASS_CONTROLLER_DATA, AIN, "")
                    self.__ha_value = new_object(
                        interface=interface,
                        din=din,
                        temp_in=temp_in,
                        light_in=light_in,
                        ain=ain,
                    )
                elif self.__inels_type is GDB3_10:
                    switches = self.__trim_inels_status_values(
                        GLASS_CONTROLLER_DATA, SW, "")
                    switches = f"0x{switches}"
                    switches = f"{int(switches, 16):0>8b}"
                    
                    digital_inputs = self.__trim_inels_status_values(
                        GLASS_CONTROLLER_DATA, SW, "")
                    digital_inputs = f"0x{digital_inputs}"
                    digital_inputs = f"{int(digital_inputs, 16):0>8b}"

                    interface = []
                    for i in range(3):
                        interface.append(switches[6-2*i]=="1")
                    for i in range(2):
                        din.append(digital_inputs[7-i]=="1")
                    
                    temp_in = self.__trim_inels_status_values(GLASS_CONTROLLER_DATA, TEMP_IN, "")
                    light_in = self.__trim_inels_status_values(GLASS_CONTROLLER_DATA, LIGHT_IN, "")
                    ain = self.__trim_inels_status_values(GLASS_CONTROLLER_DATA, AIN, "")
                    self.__ha_value = new_object(
                        interface=interface,
                        din=din,
                        temp_in=temp_in,
                        light_in=light_in,
                        ain=ain,
                    )
        except Exception as err:
            _LOGGER.error("Error making HA value for device of type '%s', status value was '%s'", self.__inels_type, None if not self.inels_status_value else self.inels_status_value.replace("\n", " "))
            self.__ha_value = dummy_val
            #raise

    def __trim_inels_status_values(
        self, selector: "dict[str, Any]", fragment: str, jointer: str
    ) -> str:
        """Trim inels status from broker into the pure string."""
        data = self.__inels_status_value.split("\n")[:-1]

        selected = itemgetter(*selector[fragment])(data)
        return jointer.join(selected)

    def __trim_inels_status_bytes(
        self, selector: "dict[str, Any]", fragment: str) -> "list[str]":
        """Split inels status section into its constituting bytes"""
        data = self.__inels_status_value.split("\n")[:-1]

        selected = itemgetter(*selector[fragment])(data)
        return selected

    # Forms a set value from the ha value
    def __find_inels_value(self) -> None:
        """Find inels mqtt value for specific device."""
        if self.__ha_value is not dummy_val:
            try:
                if self.__device_type is SWITCH:
                    if self.__inels_type is RF_SINGLE_SWITCH:
                        if self.__ha_value is None:
                            self.__inels_set_value = DEVICE_TYPE_07_COMM_TEST
                        else:
                            self.__inels_set_value = f"{(2 - (self.__ha_value.simple_relay[0].is_on)):02X}\n00\n"
                    elif self.__inels_type is RF_SWITCHING_UNIT:
                        if self.__ha_value is None:
                            self.__inels_set_value = DEVICE_TYPE_02_COMM_TEST
                        else:
                            self.__inels_set_value = f"{(2 - (self.__ha_value.simple_relay[0].is_on)):02X}\n00\n00\n"
                    elif self.__inels_type is RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR:
                        if self.__ha_value is None:
                            self.__inels_set_value = DEVICE_TYPE_07_COMM_TEST
                        else:
                            self.__inels_set_value = SWITCH_WITH_TEMP_SET[self.__ha_value.simple_relay[0].is_on]            
                    elif self.__inels_type in [SA3_01B, SA3_02B, SA3_02M, SA3_04M, SA3_06M, SA3_012M, IOU3_108M]:
                        value = ""
                        if hasattr(self.__ha_value, "simple_relay"):
                            for re in self.__ha_value.simple_relay:
                                value += RELAY_SET[re.is_on]
                            self.__inels_set_value = value
                        elif hasattr(self.__ha_value, "relay"):
                            for re in self.__ha_value.relay:
                                value += RELAY_SET[re.is_on]
                            self.__inels_set_value = value
                    elif self.__inels_type is SA3_022M:
                        value = ""
                        for r in self.__ha_value.relay:
                            value += RELAY_SET[r.is_on]
                        for s in self.__ha_value.shutter_motors:
                            value += RELAY_SET[s]
                        for v in self.__ha_value.valve:
                            value += RELAY_SET[v]
                        self.__inels_set_value = value
                    elif self.__inels_type is IOU3_108M:
                        set_val = ""
                        for r in self.__ha_value.relay:
                            set_val += RELAY_SET[r.is_on]
                        self.__inels_set_value = set_val
                    elif self.__inels_type is RC3_610DALI:
                        set_val = "00\n" * 4 #4 bytes
                        for a in self.__ha_value.aout:
                            set_val += f"{a.brightness:02X}\n"
                        set_val += "00\n" * 2 #8 bytes
                        for r in self.__ha_value.relay:
                            set_val += RELAY_SET[r.is_on] #16 bytes
                        set_val += "00\n" * 4 #20 bytes
                        for i in range(4):
                            set_val += f"{self.__ha_value.dali[i].brightness:02X}\n"
                        set_val += "00\n" * 4
                        for i in range(4, 8):
                            set_val += f"{self.__ha_value.dali[i].brightness:02X}\n"
                        set_val += "00\n" * 4
                        for i in range(8, 12):
                            set_val += f"{self.__ha_value.dali[i].brightness:02X}\n"
                        set_val += "00\n" * 4
                        for i in range(12, 16):
                            set_val += f"{self.__ha_value.dali[i].brightness:02X}\n"
                            
                        self.__inels_set_value = set_val
                    elif self.__inels_type is FA3_612M:
                        original_status = self.ha_value.last_status_val.split("\n")
                        
                        set_val = "00\n" * 4
                        for a in self.ha_value.aout:
                            set_val += f"{a.brightness:02X}\n"
                        for i in range(4):
                            set_val += f"{original_status[8 + i]}\n"
                        fan_val = ""
                        for i in range(3):
                            fan_val += RELAY_SET[self.ha_value.fan_speed == (i + 1)]
                        set_val += fan_val
                        set_val += f"{original_status[15]}\n"
                        
                        self.__inels_set_value = set_val
                    elif self.__inels_type in [GCR3_11, GCH3_31]:
                        set_val = "04\n" if self.ha_value.simple_relay[0].is_on else "00\n"
                        set_val += "00\n" * 9
                        self.__inels_set_value = set_val 
                elif self.__device_type is LIGHT:
                    if self.__inels_type in [RF_SINGLE_DIMMER, RF_DIMMER]:
                        if self.__ha_value is None:
                            self.__inels_set_value = DEVICE_TYPE_05_COMM_TEST
                        else:
                            out = round(self.__ha_value.simple_light[0].brightness, -1)
                            out = out if out < 100 else 100

                            b = int((((0xFFFF - out) + 10000) * 1000) / 5)
                            b = 0xFFFF - ((int(out/5)*1000) + 10000)
                            b_str = f"{b:04X}"
                            self.__inels_set_value = f"01\n{b_str[0]}{b_str[1]}\n{b_str[2]}{b_str[3]}\n"
                    elif self.__inels_type is RF_DIMMER_RGB:
                        if self.__ha_value is None:
                            self.__inels_set_value = DEVICE_TYPE_13_COMM_TEST
                        else:
                            rgb = self.__ha_value.rgb[0]
                            self.__inels_set_value = f"01\n{rgb.r:02X}\n{rgb.g:02X}\n{rgb.b:02X}\n{int(rgb.brightness*2.55):02X}\n00\n"
                    elif self.__inels_type is RF_LIGHT_BULB:
                        if self.__ha_value is None:
                            self.__inels_set_value = DEVICE_TYPE_13_COMM_TEST
                        else:
                            self.__inels_set_value = f"15\n00\n00\n00\n{int(self.ha_value.simple_light[0].brightness*2.55):02X}\n00\n"
                    elif self.__inels_type is DA3_22M:
                        # correct the values
                        out1 = round(self.__ha_value.light_coa_toa[0].brightness, -1)
                        out1 = out1 if out1 < 100 else 100

                        out2 = round(self.__ha_value.light_coa_toa[1].brightness, -1)
                        out2 = out2 if out2 < 100 else 100

                        out1_str = f"{out1:02X}\n"
                        out2_str = f"{out2:02X}\n"

                        # EX: 00\n00\n00\n00\n64\n64\n # 100%/100%
                        self.__inels_set_value = "".join(["00\n" * 4, out1_str, out2_str])
                    elif self.__inels_type in [DAC3_04B, DAC3_04M]:
                        set_val = "00\n" * 4
                        for d in self.ha_value.aout:
                            set_val += f"{d.brightness:02X}\n"
                        self.__inels_set_value = set_val
                    elif self.__inels_type in DCDA_33M:
                        set_val = "00\n"*4
                        for i in range(4):
                            aout = self.__ha_value.out[i].brightness
                            set_val += f"{aout:02X}\n"
                        self.__inels_set_value = set_val
                    elif self.__inels_type is DA3_66M:
                        set_val = "00\n"*4
                        for i in range(4):
                            out = self.__ha_value.light_coa_toa[i].brightness
                            out = out if out <= 100 else 100
                            set_val += f"{out:02X}\n"
                        set_val += "00\n"*4
                        for i in range(4, 6):
                            out = self.__ha_value.light_coa_toa[i].brightness
                            out = out if out <= 100 else 100
                            set_val += f"{out:02X}\n"
                        set_val += "00\n"*12
                        self.__inels_set_value = set_val
                elif self.__device_type is COVER:
                    if self.__inels_type is RF_SHUTTERS:
                        if self.__ha_value is None:
                            self.__inels_set_value = DEVICE_TYPE_03_COMM_TEST
                        else:
                            shutter_set = RF_SHUTTER_STATE_SET[self.__ha_value.shutters[0].state]
                            self.__inels_set_value = shutter_set + "00\n00\n"
                    elif self.__device_type is RF_SHUTTER_UNIT:
                        if self.__ha_value is None:
                            self.__inels_set_value = DEVICE_TYPE_03_COMM_TEST
                        else:
                            if self.__ha_value.shutters_with_pos[0].set_pos:
                                shutter_set = f"0A\n00\n{int(round(self.__ha_value.shutters_with_pos[0].position*2.55, 1)):02X}\n"
                            else:
                                shutter_set = RF_SHUTTER_STATE_SET[self.__ha_value.shutters_with_pos[0].state] + "00\n00\n"
                            self.__inels_set_value = shutter_set
                elif self.__device_type is CLIMATE:
                    if self.__inels_type is RF_WIRELESS_THERMOVALVE:
                        required_temp = int(round(self.__ha_value.climate.required * 2, 0))
                        self.__inels_set_value = f"00\n{required_temp:02X}\n00\n"
                    elif self.__inels_type is VIRT_CONTR:
                        cc = self.ha_value.climate_controller

                        current_temp = f"{(cc.current * 100):08X}"
                        current_temp = break_into_bytes(cc.current_temp)

                        critical_temp = f"{(cc.critical_temp * 100):08X}"
                        critical_temp = break_into_bytes(critical_temp)

                        manual_temp = f"{((cc.required + cc.correction_temp) * 100):08X}"
                        manual_temp = break_into_bytes(manual_temp)

                        manual_cool_temp = f"{((cc.required_cool + cc.correction_temp) * 100):08X}"
                        manual_cool_temp = break_into_bytes(manual_cool_temp)

                        plan_in = "00\n"
                        if cc.public_holiday > 0:
                            plan_in = "80\n"
                        elif cc.vacation:
                            plan_in = "40\n"

                        manual_in = 0
                        if cc.control_mode == 0: #manual mode
                            manual_in = 7

                        byte18 = 1 #TODO review this

                        set_val = "\n".join(current_temp) + "\n"
                        set_val += "\n".join(critical_temp) + "\n"
                        set_val += "\n".join(manual_temp) + "\n"
                        set_val += "\n".join(manual_cool_temp) + "\n"
                        set_val += plan_in
                        set_val += f"{manual_in:02X}\n"
                        set_val += f"{byte18:02X}\n"

                        self.__inels_set_value = set_val
            except Exception as err:
                _LOGGER.error("Error making 'set' value for device of type '%s', status value was '%s'", self.__inels_type, None if not self.inels_status_value else self.inels_status_value.replace("\n", " "))
                raise

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
    if platform == SWITCH:
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
