"""Constances of inels-mqtt."""
from __future__ import annotations
from typing import Final
from enum import IntEnum

DISCOVERY_TIMEOUT_IN_SEC = 5

NAME = "inels-mqtt"

SWITCH = "switch"
SENSOR = "sensor"
LIGHT = "light"
COVER = "cover"
CLIMATE = "climate"
BUTTON = "button"
BINARY_SENSOR = "binary_sensor"

# RF
RF_SINGLE_SWITCH = "Single switching unit"  # 01
RF_SWITCHING_UNIT = "Switching unit" #02
RF_SHUTTERS = "Shutters" #3
RF_SINGLE_DIMMER = "Single dimmer"  # 04
RF_DIMMER = "Dimmer" #05
RF_DIMMER_RGB = "RGB dimmer"  # 06
RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR = (
    "Switching unit with external temperature sensor" #07
)
# RF_SWITCHING_UNIT_WITH_TEMPERATURE_SENSORS = (
#     "Switching unit with temperature sensors"  # 08
# )
RF_WIRELESS_THERMOVALVE = "Wireless Thermovalve" #9
RF_TEMPERATURE_INPUT = "Temperature input" #10
RF_THERMOSTAT = "Thermostat" #12
RF_LIGHT_BULB = "Light bulb" #13
RF_FLOOD_DETECTOR = "Flood detector"  # 15
RF_DETECTOR = "Detector"  # 16
RF_MOTION_DETECTOR = "Motion detector"  # 17
RF_2_BUTTON_CONTROLLER = "Two button controller"  # 18
RF_CONTROLLER = "Controller" #19
RF_PULSE_CONVERTER = "Pulse converter"  # 20
RF_SHUTTER_UNIT = "Shutter unit" #21
RF_TEMPERATURE_HUMIDITY_SENSOR = "Temperature and humidity sensor"  # 29
SYSTEM_BITS = "Virtual system bits"
SYSTEM_INTEGERS = "Virtual system integers"

# BUS
SA3_01B = "SA3-01B"
DA3_22M = "DA3-22M"
GRT3_50 = "GRT3-50"
GSB3_90SX = "GSB3-90SX"
SA3_04M = "SA3-04M"
SA3_012M = "SA3-012M"
IM3_80B = "IM3-80B"
IM3_140M = "IM3-140M"
WSB3_20H = "WSB3-20H"
GSB3_60SX = "GSB3-60Sx"
IDRT3_1 = "IDRT3-1"
ADC3_60M = "ADC3-60M"
DA3_66M = "DA3-66M"
DAC3_04B = "DAC3-04B"
DAC3_04M = "DAC3-04M"
DCDA_33M = "DCDA-33M"
DMD3_1 = "DMD3-1"
FA3_612M = "FA3-612M"
GBP3_60 = "GBP3-60"
GCH3_31 = "GCH3-31"
GCR3_11 = "GCR3-11"
GDB3_10 = "GDB3-10"
GSB3_20SX = "GSB3_20Sx"
GSB3_40SX = "GSB3_40Sx"
GSP3_100 = "GSP3-100"
IM3_20B = "IM3-20B"
IM3_40B = "IM3-40B"
IOU3_108M = "IOU3-108M"
SA3_02B = "SA3-02B"
SA3_02M = "SA3-02M"
SA3_06M = "SA3-06M"
SA3_022M = "SA3-022M"
TI3_10B = "TI3-10B"
TI3_40B = "TI3-40B"
TI3_60M = "TI3-60M"
WSB3_20 = "WSB3-20"
WSB3_40 = "WSB3-40"
WSB3_40H = "WSB3-40H"
RC3_610DALI = "RC3-610DALI"

#Virtual bus
VIRT_CONTR = "Virtual controller"
VIRT_HEAT_REG = "Heat virtual regulator"
VIRT_COOL_REG = "Cool virtual regulator"


INELS_DEVICE_TYPE_DICT = {
    "01": RF_SINGLE_SWITCH,
    "02": RF_SWITCHING_UNIT,
    "03": RF_SHUTTERS,
    "04": RF_SINGLE_DIMMER,
    "05": RF_DIMMER,
    "06": RF_DIMMER_RGB,
    "07": RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR,
    "09": RF_WIRELESS_THERMOVALVE,
    "10": RF_TEMPERATURE_INPUT,
    "12": RF_THERMOSTAT,
    "13": RF_LIGHT_BULB,
    "15": RF_FLOOD_DETECTOR,
    "16": RF_DETECTOR,
    "17": RF_MOTION_DETECTOR,
    "18": RF_2_BUTTON_CONTROLLER,
    "19": RF_CONTROLLER,
    "21": RF_SHUTTER_UNIT,
    "29": RF_TEMPERATURE_HUMIDITY_SENSOR,

    "100": SA3_01B,
    "101": DA3_22M,
    "102": GRT3_50,
    "103": GSB3_90SX,
    "104": SA3_02B,
    "105": SA3_02M,
    "106": SA3_04M,
    "107": SA3_06M,
    "108": SA3_012M,
    "109": SA3_022M,
    "111": FA3_612M,
    #"112": IOU3_108M, #util
    "114": RC3_610DALI,
    "115": IM3_20B,
    "116": IM3_40B,
    "117": IM3_80B,
    "120": DMD3_1,
    "121": IM3_140M,
    "122": WSB3_20,
    "123": WSB3_40,
    "124": WSB3_20H,
    "125": WSB3_40H,
    "128": GCR3_11, #util
    "129": GCH3_31, #util
    #"136": GSP3_100, #util
    #"137": GDB3_10, #util
    "138": GSB3_40SX,
    "139": GSB3_60SX,
    "140": GSB3_20SX,
    "141": GBP3_60,
    "147": DAC3_04B,
    "148": DAC3_04M,
    #"150": DCDA_33M, #util
    "151": DA3_66M,
    "156": ADC3_60M, #util
    "157": TI3_10B,
    "158": TI3_40B,
    "159": TI3_60M,
    "160": IDRT3_1,

    #"166": VIRT_CONTR,
    #"167": VIRT_HEAT_REG,
    #"168": VIRT_COOL_REG,
}

#TODO retire this system
# device types
DEVICE_TYPE_DICT = {
    # RF
    "01": SWITCH, #RF_SINGLE_SWITCH
    "02": SWITCH, #RF_SWITCHING_UNIT
    "03": COVER, #RF_SHUTTERS
    "04": LIGHT, #RF_SINGLE_DIMMER
    "05": LIGHT, #RF_DIMMER
    "06": LIGHT, #RF_DIMMER_RGB
    "07": SWITCH, #RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR
    "09": CLIMATE, #RF_WIRELESS_THERMOVALVE
    "10": SENSOR, #RF_TEMPERATURE_INPUT
    "12": SENSOR, #RF_THERMOSTAT
    "13": LIGHT, #RF_LIGHT_BULB
    "15": SENSOR, #RF_LEVEL_DETECTOR
    "16": SENSOR, #RF_DETECTOR
    "17": SENSOR, #RF_MOTION_DETECTOR
    "18": BUTTON, #RF_2_BUTTON_CONTROLLER
    "19": BUTTON, #RFGB_40
    "21": COVER, #RF_SHUTTER_UNIT
    "29": SENSOR, #RF_TEMPERATURE_HUMIDITY_SENSOR
    # BUS
    "100": SWITCH, #SA3_01B
    "101": LIGHT, #DA3-22M
    "102": SENSOR, #GTR3_50
    "103": BUTTON, #GSB3_90SX
    "104": SWITCH, #SA3_02B,
    "105": SWITCH, #SA3_02M
    "106": SWITCH, #SA3_04M
    "107": SWITCH, #SA3_06M,
    "108": SWITCH, #SA3_012M
    "109": SWITCH, #SA3_022M,

    "111": SWITCH, # FA3_612M,
    #"112": SWITCH, # IOU3_108M,
    "114" : SWITCH, #RC3_610DALI,

    "115": SENSOR, #IM3_20B,
    "116": SENSOR, #IM3_40B,
    "117": SENSOR, #IM3_80B
    "120": SENSOR, #DMD3_1,

    "121": SENSOR, #IM3_140M
    "122": SENSOR, #WSB3_20,
    "123": SENSOR, #WSB3_40,
    "124": SENSOR, #WSB3_20HUM / H
    "125": SENSOR, #WSB3_40HUM,
    "128": SWITCH, # GCR3_11,
    "129": SWITCH, # GCH3_31,
    #"136": SENSOR, # GSP3_100,
    #"137": SENSOR, # GDB3_10,
    "138": BUTTON, # GSB3_40SX,
    "139": BUTTON, # GSB3_60SX
    "140": BUTTON, # GSB3_20SX,
    "141": BUTTON, # GBP3_60,

    "147": LIGHT, # DAC3_04B,
    "148": LIGHT, # DAC3_04M,
    #"150": LIGHT, # DCDA_33M,

    "151": LIGHT, #DA3_66M,

    "156": SENSOR, #ADC3_60M,

    "157": SENSOR,# TI3_10B,
    "158": SENSOR,# TI3_40B,
    "159": SENSOR,# TI3_60M,
    
    "160": SENSOR, #IDRT3_1
    
    #"166": CLIMATE, #VIRT_CONTR
    #"167": CLIMATE, #VIRT_HEAT_REG
    #"168": CLIMATE, #VIRT_COOL_REG
}


BATTERY = "battery"
TEMP_IN = "temp_in"
TEMP_OUT = "temp_out"
TEMPERATURE = "temperature"
CURRENT_TEMP = "current_temp"
CRITICAL_TEMP = "critical_temp"
REQUIRED_TEMP = "required_temp"
REQUIRED_HEAT_TEMP = "required_heating_temp"
REQUIRED_COOL_TEMP = "required_cooling_temp"
CRITICAL_MAX_TEMP = "critical_max_temp"
CRITICAL_MIN_TEMP = "critical_min_temp"
MAX_TEMP = "max_temp"
TEMP_CORRECTION = "temp_correction"
PUBLIC_HOLIDAY = "public_holiday"
CONTROL_MODE = "control_holiday"
OPEN_IN_PERCENTAGE = "open_in_percentage"
RAMP_UP = "ramp_up"
TIME_RAMP_UP = "time_ramp"
TIME_RAMP_DOWN = "time_ramp_down"
TEST_COMMUNICATION = "test_communication"
PULL_DOWN = "pull_down"
PULL_UP = "pull_up"
PUSH_BUTTON_DOWN = "push_button_down"
PUSH_BUTTON_UP = "push_button_up"
RELEASE_BUTTON_DOWN = "release_button_down"
RELEASE_BUTTON_UP = "relese_button_up"
SET_TIME_UP = "set_time_up"
SET_TIME_DOWN = "set_time_down"
STOP_DOWN = "stop_down"
STOP_UP = "stop_up"
STOP = "stop"
STATE = "state"
IDENTITY = "identity"
ON = "on"
RELAY = "relay"
POSITION = "position"
RED = "red"
GREEN = "green"
BLUE = "blue"


STATE_OPEN = "open"
STATE_CLOSED = "closed"

# MY KEYWORDS
RELAY_OVERFLOW = "relay_overflow"
DIMMER_OUT = "dimmer_out"
DIM_OUT_1 = "dimmer_output_1"
DIM_OUT_2 = "dimmer_output_2"
LIGHT_IN = "light_in"
FORCED_REPAIR = "forced_repair"

AIN = "analog_temperature_input"
HUMIDITY = "humidity"
DEW_POINT = "dew_point"
PLUS_MINUS_BUTTONS = "plus_and_minus_buttons"
OUT = "out"
ALERT = "alert"
SW = "sw"
DIN = "din"
MIN_BRIGHTNESS = "minimum_brightness"
CHAN_TYPE = "channel_type"
CARD_ID = "card_id"
IN = "in"
SHUTTER = "shutter"
VALVE = "valve"
DALI = "dali"
AOUT = "aout"

# COVER CONSTANTS
COVER_SET_BYTES = {
    PULL_DOWN: "01",
    PULL_UP: "02",
    PUSH_BUTTON_DOWN: "03",
    RELEASE_BUTTON_DOWN: "04",
    PUSH_BUTTON_UP: "05",
    RELEASE_BUTTON_UP: "06",
    SET_TIME_UP: "07",
    SET_TIME_DOWN: "08",
    TEST_COMMUNICATION: "09",
}

COVER_TIME_SET_CONSTANT = 0.06577

# SHUTTER CONSTANTS
class Shutter_state(IntEnum):
    Open = 0
    Closed = 1
    Stop_up = 2
    Stop_down = 3

RF_SHUTTER_STATE_SET = {
    Shutter_state.Open: "01\n",
    Shutter_state.Closed: "02\n",
    Shutter_state.Stop_up: "04\n",
    Shutter_state.Stop_down: "06\n",
}

class Card_read_state(IntEnum):
    No_card = 0
    Success = 1
    Failure = 2

SHUTTER_STATE_LIST = [STATE_OPEN, STATE_CLOSED]

SHUTTER_STATES = {
    "03\n01\n": STATE_OPEN,
    "03\n00\n": STATE_CLOSED,
}

SHUTTER_SET = {
    STATE_OPEN: "02 00 00",
    STATE_CLOSED: "01 00 00",
    STOP_DOWN: "03 00 00",
    STOP_UP: "05 00 00",
}

# ANALOG REG CONSTANTS
ANALOG_REGULATOR_SET_BYTES = {
    RF_DIMMER: "01",
    RAMP_UP: "02",
    TIME_RAMP_UP: "05",
    TIME_RAMP_DOWN: "06",
    TEST_COMMUNICATION: "07",
}

# DIMMER CONSTANTS
DEVICE_TYPE_05_HEX_VALUES = {
    "D8\nEF\n": 0,
    "D1\n1F\n": 10,
    "C9\n4F\n": 20,
    "C1\n7F\n": 30,
    "B9\nAF\n": 40,
    "B1\nDF\n": 50,
    "AA\n0F\n": 60,
    "A2\n3F\n": 70,
    "9A\n6F\n": 80,
    "92\n9F\n": 90,
    "8A\nCF\n": 100,
}

# DEVICE DATA
#   RF
DEVICE_TYPE_02_DATA = {RELAY: [1]}
DEVICE_TYPE_07_DATA = {RELAY: [1], TEMP_OUT: [3, 2]}
DEVICE_TYPE_05_DATA = {RF_DIMMER: [0, 1]}
DEVICE_TYPE_06_DATA = {RED: [1], GREEN: [2], BLUE: [3], OUT: [4]}
DEVICE_TYPE_10_DATA = {BATTERY: [0], TEMP_IN: [2, 1], TEMP_OUT: [4, 3]}
DEVICE_TYPE_03_DATA = {SHUTTER: [1]}
DEVICE_TYPE_09_DATA = {
    OPEN_IN_PERCENTAGE: [0],
    CURRENT_TEMP: [1],
    BATTERY: [2],
    REQUIRED_TEMP: [3],
}
DEVICE_TYPE_12_DATA = {TEMP_IN: [0], BATTERY: [2]}
DEVICE_TYPE_13_DATA = {OUT: [4]}
DEVICE_TYPE_15_DATA = {STATE: [0], AIN: [2, 1]}
DEVICE_TYPE_16_DATA = {STATE: [0]}
DEVICE_TYPE_19_DATA = {STATE: [0], IDENTITY: [1]}
DEVICE_TYPE_21_DATA = {SHUTTER: [1], POSITION: [2]}
DEVICE_TYPE_29_DATA = {BATTERY: [0], TEMP_IN: [2, 1], HUMIDITY: [3]}
#   BUS
SA3_01B_DATA = {
    RELAY: [0],
    TEMP_IN: [2, 3],
    RELAY_OVERFLOW: [4]
}
DA3_22M_DATA = {
    TEMP_IN: [0, 1],
    DA3_22M: [2],
    DIM_OUT_1: [4],
    DIM_OUT_2: [5],
}
GRT3_50_DATA = {
    GRT3_50: [1],
    TEMP_IN: [2, 3],
    PLUS_MINUS_BUTTONS: [7],
    LIGHT_IN: [8, 9, 10, 11],
    AIN: [12, 13],
    HUMIDITY: [14, 15],
    DEW_POINT: [16, 17],
}

GSB3_90SX_DATA = {
    GSB3_90SX: [0, 1],
    TEMP_IN: [2, 3],
    LIGHT_IN: [4, 5, 6, 7],
    AIN: [8, 9],
    HUMIDITY: [10, 11],
    DEW_POINT: [12, 13],
}

SA3_04M_DATA = {
    RELAY: [0, 1, 2, 3], #relays
    SA3_04M: [4], #switch inputs
}

SA3_012M_DATA = {
    RELAY: list(range(12)), #relays
    SA3_012M: [12, 13], #switch inputs
}

IM3_80B_DATA = {
    IN: [0, 1],
    TEMP_IN: [2, 3],
}

IM3_140M_DATA = {
    IN: [0, 1, 2, 3]
}

DEVICE_TYPE_124_DATA = {
    WSB3_20H: [0, 1],
    TEMP_IN: [2, 3],
    AIN: [4, 5],
    HUMIDITY: [6, 7],
    DEW_POINT: [8, 9],
}

DEVICE_TYPE_139_DATA = {
    GSB3_60SX: [0, 1],
    TEMP_IN: [2, 3],
    LIGHT_IN: [4, 5, 6, 7],
    AIN: [8, 9],
}

IDRT3_1_DATA = {
    SW: [1],
    TEMP_IN: [2, 3],
    TEMP_OUT: [8, 9],
}

ADC3_60M_DATA = {
    AIN: list(range(24)),
    ADC3_60M: [24],
}

DA3_66M_DATA = {
    ALERT: [1, 2],
    SW: [3],
    OUT: [4, 5, 6, 7, 12, 13],
    DIN: [8],
    #MIN_BRIGHTNESS: list(range(14, 20, 2)), #[2*i+14 for i in range(6)],
    #CHAN_TYPE: list(range(15, 21, 2)), #[2*i+15 for i in range(6)],
}

DAC3_04_DATA = {
    TEMP_IN: [0, 1],
    ALERT: [2],
    OUT: [4, 5, 6, 7],
}

DCDA_33M_DATA = {
    DCDA_33M: [2],
    OUT: [4, 5, 6, 7],
}

DMD3_1_DATA = {
    LIGHT_IN: [0, 1, 2, 3],
    TEMP_IN: [4, 5],
    HUMIDITY: [6, 7],
    DMD3_1: [8],
}

FA3_612M_DATA = {
    FA3_612M: [0, 1, 2],
    RELAY_OVERFLOW: [3],
    AOUT: list(range(4, 8)),
    RELAY: list(range(8, 16)),
    AIN: list(range(16, 28)),
}

GBP3_60_DATA = {
    SW: [0],
    DIN: [1],
    TEMP_IN: [2, 3],
    LIGHT_IN: [4, 5, 6, 7],
    AIN: [8, 9],
}

CARD_DATA = { #Card holder/reader
    STATE: [0, 1],
    CARD_ID: list(range (4, 12)),
    LIGHT_IN: [12, 13, 14, 15],
    TEMP_IN: [16, 17],
}

GDB3_10_DATA = { #generalize with GBP3_60
    SW: [0],
    DIN: [1],
    TEMP_IN: [2, 3],
    LIGHT_IN: [4, 5, 6, 7],
    AIN: [8, 9],
}

GSB3_DATA = { #same as upper one [GSB3-20SX, GSB3-40SX, GSB3-60SX]
    SW: [0],
    DIN: [1],
    TEMP_IN: [2, 3],
    LIGHT_IN: [4, 5, 6, 7],
    AIN: [8, 9],
}

GSP3_100_DATA = {
    GSP3_100: [0, 1],
    TEMP_IN: [2, 3],
    LIGHT_IN: [4, 5, 6, 7],
    AIN: [8, 9],
}

IM3_240B_DATA = {
    IN: [0],
    TEMP_IN: [1, 2],
}

IOU3_108M_DATA = {
    RELAY: list(range(8)),
    TEMP_IN: [8, 9, 10, 11, 12, 13, 14, 15],
    DIN: [24],
    RELAY_OVERFLOW: [25],
    ALERT: [26],
}

SA3_02B_DATA = {
    RELAY: [0, 1],
    TEMP_IN: [2, 3],
}

SA3_02M_DATA = {
    RELAY: [0, 1],
    SW: [2]
}

SA3_04M_DATA = {
    RELAY: [0, 1, 2, 3],
    SW: [4],
}

SA3_06M_DATA = {
    RELAY: [0, 1, 2, 3, 4, 5],
    SW: [6],
}

SA3_022M_DATA = {
    RELAY: list(range(16)),
    SHUTTER : [16, 17],
    VALVE: [18, 19, 20, 21],
    SW: [22, 23],
    ALERT: [24, 25],
    RELAY_OVERFLOW: [26, 27],
    SA3_022M: [28]
}

TI3_10B_DATA = {
    TEMP_IN: [0, 1]
}

TI3_40B_DATA = {
    TEMP_IN: list(range(8))
}

TI3_60M_DATA = {
    TEMP_IN: list(range(12))
}

WSB3_240_DATA = {
    SW: [0],
    DIN: [1],
    TEMP_IN: [2, 3],
    AIN: [4, 5],
}

WSB3_240HUM_DATA = {
    SW: [0],
    DIN: [1],
    TEMP_IN: [2, 3],
    AIN: [4, 5],
    HUMIDITY: [6, 7],
    DEW_POINT: [8, 9],
}

RC3_610DALI_DATA = {
    TEMP_IN: [2, 3, 18, 19],
    AOUT: [4, 5],
    RELAY: list(range(8, 16)),
    DALI: [20, 21, 22, 23, 28, 29, 30, 31, 36, 37, 38, 39, 44, 45, 46, 47],
    DIN: [24],
    RELAY_OVERFLOW: [25],
    ALERT: [26],
}

DEVICE_TYPE_166_DATA = {
    CURRENT_TEMP: [0, 1, 2, 3],
    CRITICAL_MAX_TEMP: [4, 5, 6, 7],
    REQUIRED_HEAT_TEMP: [8, 9, 10, 11],
    MAX_TEMP: [12, 13, 14, 15],
    CRITICAL_MIN_TEMP: [16, 17, 18, 19],
    REQUIRED_COOL_TEMP: [20, 21, 22, 23],
    TEMP_CORRECTION: [24, 25, 26, 27],
    PUBLIC_HOLIDAY: [28],
    CONTROL_MODE: [29],
    VIRT_CONTR: [30],
}

VIRT_REG_DATA = {
    STATE: [0],
    VIRT_HEAT_REG: [1],
}

#TODO update table
INELS_DEVICE_TYPE_DATA_STRUCT_DATA = {
    #RF
    RF_SWITCHING_UNIT : DEVICE_TYPE_02_DATA,
    RF_SHUTTERS : DEVICE_TYPE_03_DATA,
    RF_DIMMER : DEVICE_TYPE_05_DATA,
    RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR : DEVICE_TYPE_07_DATA,
    RF_WIRELESS_THERMOVALVE : DEVICE_TYPE_09_DATA,
    RF_TEMPERATURE_INPUT : DEVICE_TYPE_10_DATA,
    RF_CONTROLLER : DEVICE_TYPE_19_DATA,
    #BUS
    SA3_01B: SA3_01B_DATA,
    DA3_22M: DA3_22M_DATA,
    GRT3_50: GRT3_50_DATA,
    GSB3_90SX: GSB3_DATA,
    
    SA3_04M: SA3_04M_DATA,
    SA3_012M: SA3_012M_DATA,
    IM3_80B: IM3_80B_DATA,
    IM3_140M: IM3_140M_DATA,
    WSB3_20H: DEVICE_TYPE_124_DATA,
    IDRT3_1: IDRT3_1_DATA,
    VIRT_CONTR: DEVICE_TYPE_166_DATA,
    VIRT_HEAT_REG: VIRT_REG_DATA,
    VIRT_COOL_REG: VIRT_REG_DATA,
    
    TI3_10B: TI3_10B_DATA,
    TI3_40B: TI3_40B_DATA,
    TI3_60M: TI3_60M_DATA,
    GSB3_20SX: GSB3_DATA,
    GSB3_40SX: GSB3_DATA,
    GSB3_60SX: GSB3_DATA,
    GBP3_60: GSB3_DATA,
}


# BUTTON CONSTANTS
BUTTON_NUMBER = {
    "01": 1,
    "02": 2,
    "04": 3,
    "08": 4,
    "16": 5,
    "32": 6,
}

BUTTON_DEVICE_AMOUNT = {RF_CONTROLLER: 4}

SA3_AMOUNTS = {
    SA3_01B: 1,
    SA3_02B: 2,
    SA3_02M: 2,
    SA3_04M: 4,
    SA3_06M: 6,
    SA3_012M: 12,
    SA3_022M: 16,
}

DA3_AMOUNTS = {DA3_22M: 2, DA3_66M: 6}
GSB3_AMOUNTS = {GSB3_20SX: 2, GSB3_40SX: 4, GSB3_60SX: 6, GSB3_90SX: 9, GBP3_60: 6}
IM3_AMOUNTS = {IM3_20B: 2, IM3_40B: 4, IM3_80B: 8, IM3_140M: 14}
TI3_AMOUNTS = {TI3_10B: 1, TI3_40B: 4, TI3_60M: 6}
WSB3_AMOUNTS = {WSB3_20: 2, WSB3_20H: 2, WSB3_40: 4, WSB3_40H: 4}

VIRT_CONT_STATUS_TABLE = {
    0 : "User control",
    1 : "Two temperature autonomous",
    2 : "Single temperature autonomous",
}

VIRT_REG_STATUS_TABLE = {
    1 : "Enabled",
    2 : "Error actual temperature",
    4 : "Error required temperature",
    8 : "Disabled",
    16 : "Error critical temperature",
    32 : "Error anti-freeze temperature",
}



# FRAGMENT/MQTT CONSTANTS
FRAGMENT_DOMAIN = "fragment_domain"
FRAGMENT_SERIAL_NUMBER = "fragment_serial_number"
FRAGMENT_STATE = "fragment_state"
FRAGMENT_DEVICE_TYPE = "fragment_device_type"
FRAGMENT_UNIQUE_ID = "fragment_unique_id"

MQTT_BROKER_CLIENT_NAME = "inels-mqtt"
MQTT_DISCOVER_TOPIC = "inels/status/#"

MQTT_TOTAL_CONNECTED_TOPIC = "inels/connected/#"
MQTT_TOTAL_STATUS_TOPIC = "inels/status/#"

MQTT_STATUS_TOPIC_PREFIX = "inels/status/"
MQTT_SET_TOPIC_PREFIX = "inels/set/"

TOPIC_FRAGMENTS = {
    FRAGMENT_DOMAIN: 0,
    FRAGMENT_STATE: 1,
    FRAGMENT_SERIAL_NUMBER: 2,
    FRAGMENT_DEVICE_TYPE: 3,
    FRAGMENT_UNIQUE_ID: 4,
}

DEVICE_CONNECTED = {
    "on\n": True,
    "off\n": False,
}

# SWITCH CONSTANTS
SWITCH_ON_STATE = "02\n01\n"
SWITCH_OFF_STATE = "02\n00\n"

SWITCH_ON_SET = "01\n00\n00\n"
SWITCH_OFF_SET = "02\n00\n00\n"

SWITCH_SET = {
    True: SWITCH_ON_SET,
    False: SWITCH_OFF_SET,
}

SWITCH_STATE = {
    SWITCH_ON_STATE: True,
    SWITCH_OFF_STATE: False,
}

SWITCH_ON_WITH_TEMP_SET = "01\n00\n"
SWITCH_OFF_WITH_TEMP_SET = "02\n00\n"

SWITCH_WITH_TEMP_SET = {
    True: SWITCH_ON_WITH_TEMP_SET,
    False: SWITCH_OFF_WITH_TEMP_SET,
}

DEVICE_TYPE_02_COMM_TEST = "08\n00\n00\n"
DEVICE_TYPE_03_COMM_TEST = "09\n00\n00\n"
DEVICE_TYPE_05_COMM_TEST = "07\n00\n00\n"
DEVICE_TYPE_07_COMM_TEST = "08\n00\n"
DEVICE_TYPE_13_COMM_TEST = "07\n00\n00\n00\n00\n00\n"

#devices that support having no state topic at setup time
INELS_ASSUMED_STATE_DEVICES = [ 
    RF_2_BUTTON_CONTROLLER,
    RF_CONTROLLER,
]

INELS_COMM_TEST_DICT = {
    "01": DEVICE_TYPE_07_COMM_TEST, # same as 07
    "02": DEVICE_TYPE_02_COMM_TEST,
    "03": DEVICE_TYPE_03_COMM_TEST,
    "04": DEVICE_TYPE_05_COMM_TEST, # same as 05
    "05": DEVICE_TYPE_05_COMM_TEST,
    "06": DEVICE_TYPE_13_COMM_TEST, #same as 13
    "07": DEVICE_TYPE_07_COMM_TEST,
    "13": DEVICE_TYPE_13_COMM_TEST,
    "21": DEVICE_TYPE_03_COMM_TEST, # same as 03
}

# RELAY (100)
# state
RELAY_ON_STATE = "02\n01\n"
RELAY_OFF_STATE = "02\n00\n"

# set
RELAY_ON_SET = "07\n"
RELAY_OFF_SET = "06\n"

RELAY_SET = {
    True: RELAY_ON_SET,
    False: RELAY_OFF_SET,
}

RELAY_STATE = {
    RELAY_ON_STATE: True,
    RELAY_OFF_STATE: False,
}

RELAY_ON_WITH_TEMP_SET = "06\n"
RELAY_OFF_WITH_TEMP_SET = "07\n"

RELAY_WITH_TEMP_SET = {
    True: RELAY_ON_WITH_TEMP_SET,
    False: RELAY_OFF_WITH_TEMP_SET,
}

RELAY_NUMBER = {
    SA3_01B: 1,
    SA3_04M: 4,
    SA3_012M: 12,
}

# TWO CHANNEL DIMMER (101)

TWOCHANNELDIMMER_RAMP_VAL = "04\n"

# THERMOSTAT (102)
THERMOSTAT_SET_BACKLIT_DISPLAY = {
    False: "00\n",
    True: "08\n",
}

THERMOSTAT_SET_BACKLIT_BUTTONS = {
    False: "00\n",
    True: "80\n",
}

# BUTTON ARRAY (103)
BUTTONARRAY_SET_DISABLED = {
    False: "00\n",
    True: "01\n",
}

BUTTONARRAY_SET_BACKLIT = {
    False: "00\n",
    True: "32\n",
}

BUS_SENSOR_NOT_CALIBRATED = "Sensor error: not calibrated"
BUS_SENSOR_NO_VALUE = "Sensor error: no value"
BUS_SENSOR_NOT_CONFIGURED = "Sensor error: not configured"
BUS_SENSOR_OUT_OF_RANGE = "Sensor error: value out of range"
BUS_SENSOR_MEASURE = "Sensor error: measurement error"
BUS_SENSOR_NO_SENSOR = "Sensor error: no sensor"
BUS_SENSOR_NOT_COMMUNICATING = "Sensor error: no internal communication"
BUS_SENSOR_ERRORS = {
    0X9: BUS_SENSOR_NOT_COMMUNICATING,
    0xA: BUS_SENSOR_NOT_CALIBRATED,
    0xB: BUS_SENSOR_NO_VALUE,
    0xC: BUS_SENSOR_NOT_CONFIGURED,
    0xD: BUS_SENSOR_OUT_OF_RANGE,
    0xE: BUS_SENSOR_MEASURE,
    0xF: BUS_SENSOR_NO_SENSOR,
}

# MQTT/INELS CONSTANTS

MQTT_TRANSPORTS = {"tcp", "websockets"}

MQTT_TIMEOUT: Final = "timeout"
MQTT_HOST: Final = "host"
MQTT_USERNAME: Final = "username"
MQTT_PASSWORD: Final = "password"
MQTT_PORT: Final = "port"
MQTT_CLIENT_ID: Final = "client_id"
MQTT_PROTOCOL: Final = "protocol"
MQTT_TRANSPORT: Final = "transport"
PROTO_31 = "3.1"
PROTO_311 = "3.1.1"
PROTO_5 = 5

VERSION = "0.1.0"

MANUFACTURER: Final = "ELKO EP s.r.o"
