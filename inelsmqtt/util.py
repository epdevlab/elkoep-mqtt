"""Utility classes."""
import logging

from operator import itemgetter
from typing import Any, Dict

from inelsmqtt.mqtt_client import GetMessageType

from .const import (
    ANALOG_REGULATOR_SET_BYTES,
    BATTERY,
    CLIMATE_TYPE_09_DATA,
    COVER,
    CURRENT_TEMP,
    DEVICE_TYPE_05_DATA,
    DEVICE_TYPE_05_HEX_VALUES,
    BUTTON_TYPE_19_DATA,
    BUTTON_DEVICE_AMOUNT,
    BUTTON_NUMBER,
    DEVICE_TYPE_07_DATA,
    REQUIRED_TEMP,
    RFDAC_71B,
    LIGHT,
    SENSOR,
    RFJA_12,
    RFATV_2,
    RFSTI_11B,
    SHUTTER_SET,
    SHUTTER_STATE_LIST,
    SHUTTER_STATES,
    SWITCH,
    SWITCH_SET,
    SWITCH_STATE,
    RFTI_10B,
    CLIMATE,
    OPEN_IN_PERCENTAGE,
    RFGB_40,
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

    RELAY_DATA,
    TWOCHANNELDIMMER_DATA,
    THERMOSTAT_DATA,
    BUTTONARRAY_DATA,
    DEVICE_TYPE_106_DATA,
    DEVICE_TYPE_108_DATA,
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
    MIN_BRIGHTNESS,
    CHAN_TYPE,
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
    
    INELS_DEVICE_TYPE_DATA_STRUCT_DATA
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
        
        #is_rf = "RF" in self.__inels_type
            
        if self.__device_type is SWITCH:  # outlet switch
            if self.__inels_type is RFSTI_11B:
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

                self.__ha_value = new_object(on=(state == 0), temperature=temp)
                # simplified the command to just on/off
                self.__inels_set_value = SWITCH_WITH_TEMP_SET[self.__ha_value.on]              
            elif self.__inels_type is SA3_01B:
                state = int(self.__trim_inels_status_values(RELAY_DATA, STATE, ""), 16)
                temp = self.__trim_inels_status_values(RELAY_DATA, TEMP_IN, "")
                relay_overflow = int(self.__trim_inels_status_values(RELAY_DATA, RELAY_OVERFLOW, ""),16)
                self.__ha_value = new_object(
                    on=((state & 1) == 1), #XXX1 -> on, XXX0 -> off
                    temp_in=temp,
                    relay_overflow=(relay_overflow == 1)
                )
                self.__inels_set_value = RELAY_SET[self.__ha_value.on]
            elif self.__inels_type is SA3_02B:
                re = []
                for relay in self.__trim_inels_status_bytes(SA3_02B_DATA, RELAY):
                    re.append((int(relay, 16) & 1) != 0)
                
                temp_in = self.__trim_inels_status_values(SA3_02B_DATA, TEMP_IN, "")
                self.__ha_value = new_object(
                    re=re,
                    temp_in=temp_in,
                )
                
                set_val = ""
                for r in re:
                    set_val += "07\n" if r else "06\n"
                self.__inels_set_value=set_val
            elif self.__inels_type is SA3_02M: #TODO: generalize SA3_02M/04M/06M
                re = []
                for relay in self.__trim_inels_status_bytes(SA3_02M_DATA, RELAY):
                    re.append((int(relay, 16) & 1) != 0)
                
                digital_inputs = self.__trim_inels_status_values(
                    SA3_02M_DATA, SW, "")
                digital_inputs = f"0x{digital_inputs}"
                digital_inputs = f"{int(digital_inputs, 16):0>8b}"
                sw = []
                for i in range(2):
                    sw.append(digital_inputs[7 - i] == "1")
                    
                self.__ha_value = new_object(
                    re=re,
                    sw=sw,
                )
                
                set_val = ""
                for r in re:
                    set_val += "07\n" if r else "06\n"
                self.__inels_set_value=set_val
            elif self.__inels_type is SA3_04M:
                re = []
                for relay in self.__trim_inels_status_bytes(SA3_04M_DATA, RELAY):
                    re.append((int(relay, 16) & 1) != 0)
                
                digital_inputs = self.__trim_inels_status_values(
                    SA3_04M_DATA, SW, "")
                digital_inputs = f"0x{digital_inputs}"
                digital_inputs = f"{int(digital_inputs, 16):0>8b}"
                sw = []
                for i in range(4):
                    sw.append(digital_inputs[7 - i] == "1")
                    
                self.__ha_value = new_object(
                    re=re,
                    sw=sw,
                )
                
                set_val = ""
                for r in re:
                    set_val += "07\n" if r else "06\n"
                self.__inels_set_value=set_val
            elif self.__inels_type is SA3_06M:
                re = []
                for relay in self.__trim_inels_status_bytes(SA3_06M_DATA, RELAY):
                    re.append((int(relay, 16) & 1) != 0)
                
                digital_inputs = self.__trim_inels_status_values(
                    SA3_06M_DATA, SW, "")
                digital_inputs = f"0x{digital_inputs}"
                digital_inputs = f"{int(digital_inputs, 16):0>8b}"
                sw = []
                for i in range(6):
                    sw.append(digital_inputs[7 - i] == "1")
                    
                self.__ha_value = new_object(
                    re=re,
                    sw=sw,
                )
                
                set_val = ""
                for r in re:
                    set_val += "07\n" if r else "06\n"
                self.__inels_set_value=set_val
            elif self.__inels_type is SA3_012M:
                re=[]
                for relay in self.__trim_inels_status_bytes(DEVICE_TYPE_108_DATA, RELAY):
                    re.append((int(relay, 16) & 1) != 0)
                
                digital_inputs = self.__trim_inels_status_values(
                    DEVICE_TYPE_108_DATA, SA3_012M, "")
                digital_inputs = f"0x{digital_inputs}"
                digital_inputs = f"{int(digital_inputs, 16):0>16b}"
                
                sw=[]
                for i in range(8):
                    sw.append(digital_inputs[7 - i] == "1")
                for i in range(4):
                    sw.append(digital_inputs[15 - i] == "1")
                
                self.__ha_value = new_object(
                    re=re,
                    sw=sw,
                )
                set_val = ""
                for r in re:
                    set_val += "07\n" if r else "06\n"
                self.__inels_set_value=set_val
            elif self.__inels_type is SA3_022M:
                re=[]
                for relay in self.__trim_inels_status_bytes(SA3_022M_DATA, RELAY):
                    re.append((int(relay, 16) & 1) != 0)
                    
                #organize them into [[up, down], ...], [[open, close], ...]
                shutter=[]
                for s in self.__trim_inels_status_bytes(SA3_022M_DATA, SHUTTER):
                    shutter.append((int(s, 16) & 1) != 0)
                shutters=[]
                for i in range(int(len(shutter)/2)):
                    shutters.append([shutter[2*i], shutter[2*i+1]])
                
                valve=[]
                for v in self.__trim_inels_status_bytes(SA3_022M_DATA, VALVE):
                    valve.append((int(v, 16) & 1) != 0)
                valves=[]
                for i in range(int(len(valve)/2)):
                    valves.append([valve[2*i], valve[2*i+1]])
            elif self.__inels_type is RC3_610DALI:
                #aout
                aout=[]
                for a in self.__trim_inels_status_bytes(RC3_610DALI_DATA, AOUT):
                    aout.append(int(a, 16))
                
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
                    
                sync_error = []
                aout_coa = []
                alerts = self.__trim_inels_status_values(
                    RC3_610DALI_DATA, ALERT, "")
                alerts = f"0x{alerts}"
                alerts = f"{int(alerts, 16):0>8b}"
                
                for i in range(4):
                    sync_error.append(alerts[7-i == "1"])
                for i in range(4, 6):
                    aout_coa.append(alerts[7-i] == "1")
                alert_dali_power = alerts[1] == "1"
                alert_dali_communication = alerts[0] == "1"
                
                dali_raw = self.__trim_inels_status_bytes(
                    RC3_610DALI_DATA, DALI)
                dali = []
                for d in dali_raw:
                    d = int(d, 16)
                    dali.append(d if d <= 100 else 100)
                
                last_status_val=self.__inels_status_value
                
                self.__ha_value = new_object(
                    re=re,
                    temps=temps,
                    din=din,
                    relay_overflow=relay_overflow,
                    aout=aout,
                    aout_coa=aout_coa,
                    sync_error=sync_error,
                    alert_dali_power=alert_dali_power,
                    alert_dali_communication=alert_dali_communication,
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
                    aout.append(int(a, 16))
                
                re=[]
                for relay in self.__trim_inels_status_bytes(FA3_612M_DATA, RELAY):
                    re.append((int(relay, 16) & 1) != 0)
                
                valves = [[re[0], re[1]], [re[2], re[3]]]
                fan_speed = 0
                if re[6]: #speed 3
                    fan_speed = 3
                elif re[5]: #speed 2
                    fan_speed = 2
                elif re[3]: #speed 1
                    fan_speed = 1
                
                heating_out = re[7]
                
                ains=[]
                ain_bytes = self.__trim_inels_status_bytes(
                    FA3_612M_DATA,
                    AIN,
                )
                for i in range(int(len(ain_bytes)/4)):
                    ains.append(ain_bytes[4*i] + ain_bytes[4*i+1] + ain_bytes[4*i+2] + ain_bytes[4*i+3])

                self.__ha_value = new_object(
                    din=din,
                    aout_coa=aout_coa,
                    sw=sw,
                    #relay_overflow=relay_overflow,
                    aout=aout,
                    valves=valves,
                    fan_speed=fan_speed,
                    heating_out=heating_out,
                    ains=ains,
                    last_status_val=last_status_val,
                )
            else:
                self.__ha_value = new_object(on = (SWITCH_STATE[self.__inels_status_value]))
                self.__inels_set_value = SWITCH_SET[self.__ha_value.on]
        elif self.__device_type is SENSOR:  # temperature sensor
            if self.__inels_type is RFTI_10B:
                self.__ha_value = self.__inels_status_value       
            elif self.__inels_type is GRT3_50:
                digital_inputs = self.__trim_inels_status_values(
                    THERMOSTAT_DATA, GRT3_50, "")
                digital_inputs_hex_str = f"0x{digital_inputs}"
                digital_inputs_bin_str = f"{int(digital_inputs_hex_str, 16):0>8b}"
                
                plusminus = self.__trim_inels_status_values(
                    THERMOSTAT_DATA, PLUS_MINUS_BUTTONS, "")
                plusminus = f"0x{plusminus}"
                plusminus = f"{int(plusminus, 16):0>8b}"
                
                temp_in = self.__trim_inels_status_values(THERMOSTAT_DATA, TEMP_IN, "")
                    
                light_in = self.__trim_inels_status_values(THERMOSTAT_DATA, LIGHT_IN, "")

                ain = self.__trim_inels_status_values(THERMOSTAT_DATA, AIN, "")
                
                humidity = self.__trim_inels_status_values(THERMOSTAT_DATA, HUMIDITY, "")

                dewpoint = self.__trim_inels_status_values(THERMOSTAT_DATA, DEW_POINT, "")


                self.__ha_value = new_object(
                    # digital inputs
                    din=[# 2
                        digital_inputs_bin_str[7] == "1", #0 -> 7, reverse endianness
                        digital_inputs_bin_str[6] == "1",
                    ],
                    sw=[# 5
                        digital_inputs_bin_str[5] == "1",
                        digital_inputs_bin_str[4] == "1",
                        digital_inputs_bin_str[3] == "1",
                        digital_inputs_bin_str[2] == "1",
                        digital_inputs_bin_str[1] == "1", #6
                    ],
                    plusminus=[
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
                
                sw=[] #up/down buttons
                for i in range(WSB3_AMOUNTS[self.__inels_type]):
                    sw.append(switches[7 - i] == "1")
                
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
                    sw=sw,
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
                sw=[] #up/down buttons
                din=[]
                for i in range(WSB3_AMOUNTS[self.__inels_type]):
                    sw.append(switches[7 - i] == "1")
                for i in range(2):
                    din.append(digital_inputs[7 - i] == "1")
            
                temp_in = self.__trim_inels_status_values(WSB3_240HUM_DATA, TEMP_IN, "")
                    
                ain = self.__trim_inels_status_values(WSB3_240HUM_DATA, AIN, "")
                
                humidity = self.__trim_inels_status_values(WSB3_240HUM_DATA, HUMIDITY, "")

                dewpoint = self.__trim_inels_status_values(WSB3_240HUM_DATA, DEW_POINT, "")

                self.__ha_value = new_object(
                    sw=sw,
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
                inputs = f"{int(inputs, 16):0>64b}"
                
                for i in range(4):
                    binary_input.append(int(inputs[7-2*i-1] + inputs[7-2*i], 2))
                    binary_input2.append(int(inputs[15-2*i-1] + inputs[15-2*i], 2))
                    binary_input3.append(int(inputs[23-2*i-1] + inputs[23-2*i], 2))
                binary_input.extend(binary_input2)
                binary_input.extend(binary_input3)
                
                for i in range(2):
                    binary_input.append(int(inputs[63-2*i-1] + inputs[63-2*i], 2))
                
                self.__ha_value = new_object(
                    input=binary_input
                )
            elif self.__inels_type is DMD3_1:
                light_in = self.__trim_inels_status_values(DMD3_1_DATA, LIGHT_IN, "")

                temp_in = self.__trim_inels_status_values(DMD3_1_DATA, TEMP_IN, "")    
                
                humidity = self.__trim_inels_status_values(DMD3_1_DATA, HUMIDITY, "")

                proximity = self.__trim_inels_status_values(
                    DMD3_1_DATA, DMD3_1, "")
                proximity = f"0x{proximity}"
                proximity = f"{int(proximity, 16):0>8b}"

                prox=proximity[7] == "1"

                self.__ha_value = new_object(
                    light_in=light_in,
                    temp_in=temp_in,
                    humidity=humidity,
                    prox=prox,
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
                
                sw = []
                din = []
                for i in range(2):
                    din.append(inputs[7-i]=="1")
                    sw.append(inputs[5-i]=="1")
                
                temp_in = self.__trim_inels_status_values(IDRT3_1_DATA, TEMP_IN, "")
                temp_out = self.__trim_inels_status_values(IDRT3_1_DATA, TEMP_OUT, "")
                
                self.__ha_value = new_object(
                    sw=sw,
                    din=din,
                    temp_in=temp_in,
                    temp_out=temp_out,
                )
            else:
                self.__ha_value = self.__inels_status_value
        elif self.__device_type is LIGHT:  # dimmer
            if self.__inels_type is RFDAC_71B:
                # value in percentage to present in HA
                self.__ha_value = DEVICE_TYPE_05_HEX_VALUES[self.__inels_status_value]

                # gets the hex values directly
                trimmed_data = self.__trim_inels_status_values(
                    DEVICE_TYPE_05_DATA, RFDAC_71B, " "
                )

                # simplified view of dimmer (sets brightness level)
                self.__inels_set_value = (  # "01 ?? ??"" sets this value to internal state
                    f"{ANALOG_REGULATOR_SET_BYTES[RFDAC_71B]} {trimmed_data}"
                )
            elif self.__inels_type is DA3_22M:
                temp = self.__trim_inels_status_values(TWOCHANNELDIMMER_DATA, TEMP_IN, "")

                state = self.__trim_inels_status_values(
                    TWOCHANNELDIMMER_DATA, DA3_22M, "")
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
                    sw=[
                        state_bin_str[7] == "1", #0
                        state_bin_str[6] == "1", #1
                    ],
                    din=[
                        state_bin_str[5] == "1",
                        state_bin_str[4] == "1"
                    ],

                    toa=[ # thermal overload alarm
                        state_bin_str[3] == "1",
                        state_bin_str[2] == "1",

                    ],
                    coa=[ # current overload alrm
                        state_bin_str[1] == "1", #6
                        state_bin_str[0] == "1", #7
                    ],

                    # This might be important
                    temp_in=temp,
                    
                    #generalization for multiple channel dimmers
                    out=out, # array
                    channel_number=2,
                )
                
                set_val = "00\n00\n00\n00\n"
                for i in range(self.__ha_value.channel_number):
                    set_val +=  f"{self.__ha_value.out[i]:02X}\n"
                self.__inels_set_value = set_val
            elif self.__inels_type is DA3_66M:
                state = self.__trim_inels_status_values(
                    DA3_66M_DATA, ALERT, ""
                )
                state = state = f"0x{state}"
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

                min_brightness = []
                min_brightness_raw = self.__trim_inels_status_bytes(
                    DA3_66M_DATA, MIN_BRIGHTNESS
                )
                for m in min_brightness_raw:
                    m = int(m, 16)
                    min_brightness.append(m if m <= 100 else 100)

                out = []
                outs = self.__trim_inels_status_bytes(
                    DA3_66M_DATA, OUT
                )
                for k, v in enumerate(outs):
                    v = int(v, 16)
                    v = v if v == 0 or v > min_brightness[k] else min_brightness[k]
                    out.append(v if v <= 100 else 100)
                
                channel_type = min_brightness = self.__trim_inels_status_bytes(
                    DA3_66M_DATA, CHAN_TYPE
                )

                self.__ha_value = new_object(
                    toa=toa,
                    coa=coa,
                    sw=sw,
                    din=din,
                    out=out,
                    min_brightness=min_brightness,
                    channel_type=channel_type
                )
                
                set_val = "00\n"*4
                for i in range(4):
                    set_val += f"{self.__ha_value.out[i]:02X}\n"
                set_val += "00\n"*4
                for i in range(4, 6):
                    set_val += f"{self.__ha_value.out[i]:02X}\n"
                set_val += "00\n"*12
                self.__inels_set_value = set_val
            else:
                self.__ha_value = self.__inels_status_value
        elif self.__device_type is COVER:  # Shutters
            ha_val = SHUTTER_STATES.get(self.__inels_status_value)

            # if the state is not obtained, grab last one (not sure why it wouldn't)
            self.__ha_value = ha_val if ha_val is not None else self.__last_value
            # give the new instruction (ex. 03 00 00 00)
            self.__inels_set_value = SHUTTER_SET[self.__ha_value]
        elif self.__device_type is CLIMATE:  # thermovalve
            if self.__inels_type is RFATV_2:
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
            elif self.__inels_type is VIRT_CONTR:
                temp_current = self.__trim_inels_status_values(
                    DEVICE_TYPE_166_DATA, CURRENT_TEMP, ""
                )
                temp_critical_max = self.__trim_inels_status_values(
                    DEVICE_TYPE_166_DATA, CRITICAL_MAX_TEMP, ""
                )
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
                temp_correction = self.__trim_inels_status_values(
                    DEVICE_TYPE_166_DATA, TEMP_CORRECTION, ""
                )
                holiday_mode = self.__trim_inels_status_values(
                    DEVICE_TYPE_166_DATA, PUBLIC_HOLIDAY, ""
                )
                control_mode = self.__trim_inels_status_values(
                    DEVICE_TYPE_166_DATA, CONTROL_MODE, ""
                )
                
                binary_vals = self.__trim_inels_status_values(
                    DEVICE_TYPE_166_DATA, VIRT_CONTR, ""
                )
                binary_vals = f"0x{binary_vals}"
                binary_vals = f"{int(binary_vals, 16):0>8b}"
                
                controller_on = binary_vals[7] == "1"
                manual_mode = binary_vals[6] == "1"
                heat_mode = binary_vals[5] == "1"
                cool_mode = binary_vals[4] == "1"
                is_holiday = binary_vals[3] == "1"
                regulator_disabled = binary_vals[2] == "1"

                self.__ha_value = new_object(
                    temp_current=temp_current,
                    temp_critical_max=temp_critical_max, #floor heating shutoff temp
                    temp_required_heat=temp_required_heat, #desired temperature
                    temp_max=temp_max, #maximum temperature
                    temp_critical_min=temp_critical_min, #floor heating force on temp (prevent pipe damage)
                    temp_required_cool=temp_required_cool, #desired temperature
                    temp_correction=temp_correction, #temperature correction
                    holiday_mode=holiday_mode, #holiday mode represents handling mode (>0, holidays enabled)
                    control_mode=control_mode,
                        # user control (user physically controls temp)
                        # autonomous 2 temperature (temperature moves between min and max malue)
                        # autonomous single temp (moves around 1 temperature)
                    
                    controller_on=controller_on, #controller is on
                    manual_mode=manual_mode, #driving mode (automatic, manual[physical])
                    heat_mode=heat_mode, #heating on
                    cool_mode=cool_mode, #cooling on
                    is_holiday=is_holiday, #is holiday
                    regulator_disabled=regulator_disabled, #"if 'on' reacts according to window-detector-in"
                )
                
            elif self.__inels_type is VIRT_HEAT_REG:
                state=int(self.__trim_inels_status_values(
                    VIRT_REG_DATA, STATE, ""
                ), 16)
                
                reg=self.__trim_inels_status_values(
                    VIRT_REG_DATA, VIRT_HEAT_REG, ""
                )
                
                heat_reg=reg[7] == "1"
                heat_source = reg[6] == "1"
                
                self.__ha_value = new_object(
                    state=state,
                    heat_reg=heat_reg,
                    heat_source=heat_source,
                )
                
            elif self.__inels_type is VIRT_COOL_REG:
                state=int(self.__trim_inels_status_values(
                    VIRT_REG_DATA, STATE, ""
                ), 16)
                
                reg=self.__trim_inels_status_values(
                    VIRT_REG_DATA, VIRT_HEAT_REG, ""
                )
                
                cool_reg=reg[7] == "1"
                cool_source = reg[6] == "1"
                
                self.__ha_value = new_object(
                    state=state,
                    cool_reg=cool_reg,
                    cool_source=cool_source,
                )
                
            else:
                self.__ha_value = self.__inels_status_value
        elif self.__device_type is BUTTON:
            if self.__inels_type is RFGB_40:
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
            elif self.__inels_type is GSB3_90SX:
                digital_inputs = self.__trim_inels_status_values(
                    BUTTONARRAY_DATA, GSB3_90SX, "")
                digital_inputs = f"0x{digital_inputs}"
                digital_inputs = f"{int(digital_inputs, 16):0>16b}"
                
                
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

                self.__ha_value = new_object(
                    sw=[
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

                    # my own additions
                    # disabled
                    disabled=False,
                    # backlit
                    backlit=False,
                )
            elif self.__inels_type in [GSB3_20SX, GSB3_40SX, GSB3_60SX, GBP3_60]:
                switches = self.__trim_inels_status_values(
                    GSB3_DATA, SW, "")
                switches = f"0x{switches}"
                switches = f"{int(switches, 16):0>8b}"
                
                digital_inputs = self.__trim_inels_status_values(
                    GSB3_DATA, SW, "")
                digital_inputs = f"0x{digital_inputs}"
                digital_inputs = f"{int(digital_inputs, 16):0>8b}"
                
                sw = []
                for i in range(GSB3_AMOUNTS[self.__inels_type]):
                    sw.append(switches[7-i] == "1")
                
                din = []
                for i in range(2):
                    din.append(digital_inputs[7-i] == "1")
                
                temp = self.__trim_inels_status_values(
                    GSB3_DATA, TEMP_IN, "")

                light_in = self.__trim_inels_status_values(
                    GSB3_DATA, LIGHT_IN, "")

                ain = self.__trim_inels_status_values(
                    GSB3_DATA, AIN, "")

                self.__ha_value = new_object(
                    sw=sw,
                    din=din,
                    # temperature
                    temp_in=temp,

                    # light in
                    light_in=light_in,

                    # AIN
                    ain=ain,
                    
                    # backlit
                    # backlit=False,
                )
            
            else:
                self.__ha_value = self.__inels_status_value
            
    def __trim_inels_status_values(
        self, selector: "dict[str, Any]", fragment: str, jointer: str
    ) -> str:
        """Trim inels status from broker into the pure string."""
        data = self.__inels_status_value.split("\n")[:-1]

        selected = itemgetter(*selector[fragment])(data)
        return jointer.join(selected)

    def __trim_inels_status_bytes(
        self, selector: "dict[str, Any]", fragment: str) -> list[str]:
        """Split inels status section into its constituting bytes"""
        data = self.__inels_status_value.split("\n")[:-1]

        selected = itemgetter(*selector[fragment])(data)
        return selected

    # Forms a set value from the ha value
    def __find_inels_value(self) -> None:
        """Find inels mqtt value for specific device."""
        if self.__device_type is SWITCH:
            if self.__inels_type is SA3_01B:
                self.__inels_set_value = RELAY_SET.get(self.__ha_value.on)
            elif self.__inels_type in [SA3_02B, SA3_02M, SA3_04M, SA3_06M, SA3_012M, SA3_022M]:
                value = ""
                for re in self.__ha_value.re:
                    value += RELAY_SET[re]
                self.__inels_set_value = value
            elif self.__inels_type is RFSTI_11B:
                state = int(
                    self.__trim_inels_status_values(DEVICE_TYPE_07_DATA, STATE, ""), 16
                )

                temp = (
                    int(
                        self.__trim_inels_status_values(
                            DEVICE_TYPE_07_DATA, TEMP_OUT, ""
                        ),
                        16,
                    )
                    / 100
                )

                self.__ha_value = new_object(on=(state == 1), temperature=temp)
                self.__inels_set_value = SWITCH_WITH_TEMP_SET[self.__ha_value.on]
            elif self.__inels_type is RC3_610DALI:
                set_val = "00\n" * 4 #4 bytes
                for a in self.__ha_value.aout:
                    set_val += f"{a:02X}\n"
                set_val += "00\n" * 2 #8 bytes
                for r in self.__ha_value.re:
                    set_val += RELAY_SET[r] #16 bytes
                set_val += "00\n" * 4 #20 bytes
                for i in range(4):
                    set_val += f"{self.__ha_value.dali[i]:02X}\n"
                set_val += "00\n" * 4
                for i in range(4, 8):
                    set_val += f"{self.__ha_value.dali[i]:02X}\n"
                set_val += "00\n" * 4
                for i in range(8, 12):
                    set_val += f"{self.__ha_value.dali[i]:02X}\n"
                set_val += "00\n" * 4
                for i in range(12, 16):
                    set_val += f"{self.__ha_value.dali[i]:02X}\n"
                    
                self.__inels_set_value = set_val
            elif self.__inels_type is FA3_612M:
                original_status = self.ha_value.last_status_val.split("\n")
                
                set_val = "00\n" * 4
                for a in self.ha_value.aout:
                    set_val += f"{a:02X}\n"
                for i in range(4):
                    set_val += f"{original_status[8 + i]}\n"
                fan_val = ""
                for i in range(3):
                    fan_val += RELAY_SET[self.ha_value.fan_speed == (i + 1)]
                set_val += fan_val
                set_val += f"{original_status[15]}\n"
                
                self.__inels_set_value = set_val
            else:
                # just a shortcut for setting it
                # basically set the status from the ha value
                self.__inels_status_value = self.__find_keys_by_value(
                    SWITCH_STATE,  # str -> bool
                    self.__ha_value.on,
                    self.__last_value
                )
                self.__inels_set_value = SWITCH_SET.get(self.__ha_value.on)
        elif self.__device_type is LIGHT:
            if self.__inels_type is RFDAC_71B:
                self.__inels_status_value = self.__find_keys_by_value(
                    DEVICE_TYPE_05_HEX_VALUES,  # str -> int
                    round(self.__ha_value, -1),
                    self.__last_value,
                )
                trimmed_data = self.__trim_inels_status_values(
                    DEVICE_TYPE_05_DATA, RFDAC_71B, " "
                )
                self.__inels_set_value = (  # 01 00 00
                    f"{ANALOG_REGULATOR_SET_BYTES[RFDAC_71B]} {trimmed_data}"
                )
                self.__ha_value = DEVICE_TYPE_05_HEX_VALUES[self.__inels_status_value]
            elif self.__inels_type is DA3_22M:
                # correct the values
                out1 = round(self.__ha_value.out[0], -1)
                out1 = out1 if out1 < 100 else 100

                out2 = round(self.__ha_value.out[1], -1)
                out2 = out2 if out2 < 100 else 100

                out1_str = f"{out1:02X}\n"
                out2_str = f"{out2:02X}\n"

                # EX: 00\n00\n00\n00\n64\n64\n # 100%/100%
                self.__inels_set_value = "".join(["00\n" * 4, out1_str, out2_str])
            elif self.__inels_type is DA3_66M:
                set_val = "00\n"*4
                for i in range(4):
                    out = self.__ha_value.out[i]
                    out = out if out <= 100 else 100
                    set_val += f"{out:02X}\n"
                set_val += "00\n"*4
                for i in range(4, 6):
                    out = self.__ha_value.out[i]
                    out = out if out <= 100 else 100
                    set_val += f"{out:02X}\n"
                set_val += "00\n"*12
                self.__inels_set_value = set_val
        elif self.__device_type is COVER:
            if self.__inels_type is RFJA_12:
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
        elif self.__device_type is CLIMATE:
            if self.__inels_type is RFATV_2:
                required_temp = int(round(self.__ha_value.required * 2, 0))
                self.__inels_set_value = f"00 {required_temp:x} 00".upper()
        elif self.__device_type is BUTTON:
            if self.__inels_type is GSB3_90SX:
                disabled = BUTTONARRAY_SET_DISABLED[self.__ha_value.disabled]
                backlit = BUTTONARRAY_SET_BACKLIT[self.__ha_value.backlit]

                self.__inels_set_value = "".join(["00\n" * 36, disabled, backlit])
            elif self.__inels_type is GSB3_20SX: #TODO revisit for color values
                self.__inels_set_value = "".join("00\n" * 4)
            elif self.__inels_type is GSB3_40SX:
                self.__inels_set_value = "".join("00\n" * 7)
            elif self.__inels_type is GSB3_60SX:
                self.__inels_set_value = "".join("00\n" * 10)
            elif self.__inels_type is IDRT3_1:
                self.__inels_set_value = "".join("00\n" * 9)
            else:
                self.__ha_value = ha_val

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
