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

RELAY = "relay"  # 100
TWOCHANNELDIMMER = "two channel dimmer"  # 101
THERMOSTAT = "thermostat"  # 102
BUTTONARRAY = "button array"  # 103


# device types
DEVICE_TYPE_DICT = {
    # RF
    "02": SWITCH,
    "03": COVER,
    "05": LIGHT,
    "07": SWITCH,
    "09": CLIMATE,
    "10": SENSOR,
    "19": BUTTON,
    # BUS
    "100": SWITCH,  # RELAY with temp sensor
    "101": LIGHT,  # TWOCHANNELDIMMER
    "102": SENSOR,  # THERMOSTAT
    #"103": BUTTON,  # BUTTONARRAY
}

# RF
RFSC_61 = "RFSC-61"
RFTI_10B = "RFTI-10B"
RFDAC_71B = "RFDAC-71B"
RFJA_12 = "RFJA-12"
RFATV_2 = "RFATV-2"
RFGB_40 = "RFGB-40"
RFKEY_40 = "RFKEY-40"
RFSTI_11B = "RFSTI-11B"

# BUS
SA3_01B = "SA3-01B"
DA3_22M = "DA3-22M"
GTR3_50 = "GTR3-50"
GSB3_90SX = "GSB3-90SX"

INELS_DEVICE_TYPE_DICT = {
    "02": RFSC_61,
    "03": RFJA_12,
    "05": RFDAC_71B,
    "07": RFSTI_11B,
    "09": RFATV_2,
    "10": RFTI_10B,
    "19": RFGB_40,

    "100": SA3_01B,
    "101": DA3_22M,
    "102": GTR3_50,
    "103": GSB3_90SX,
}

BATTERY = "battery"
TEMP_IN = "temp_in"
TEMP_OUT = "temp_out"
CURRENT_TEMP = "current_temp"
REQUIRED_TEMP = "required_temp"
OPEN_IN_PERCENTAGE = "open_in_percentage"
RAMP_UP = "ramp_up"  # náběh
TIME_RAMP_UP = "time_ramp"  # časový náběh
TIME_RAMP_DOWN = "time_ramp_down"  # časový doběh
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

STATE_OPEN = "open"
STATE_CLOSED = "closed"

# MY KEYWORDS
#SPARE = "spare"
RELAY_OVERFLOW = "relay_overflow"
DIMMER_OUT = "dimmer_out"
DIM_OUT_1 = "dimmer_output_1"
DIM_OUT_2 = "dimmer_output_2"
LIGHT_IN = "light_in"
FORCED_REPAIR = "forced_repair"  # Vnuceni oprava

AIN = "analog_temperature_input"
HUMIDITY = "humidity"
DEW_POINT = "dew_point"
PLUS_MINUS_BUTTONS = "plus_and_minus_buttons"

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
    RFDAC_71B: "01",
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
DEVICE_TYPE_07_DATA = {STATE: [1], TEMP_OUT: [3, 2]}
DEVICE_TYPE_05_DATA = {RFDAC_71B: [0, 1]}
TEMP_SENSOR_DATA = {BATTERY: [0], TEMP_IN: [2, 1], TEMP_OUT: [4, 3]}
SHUTTER_TYPE_03_DATA = {RFJA_12: [1]}
BUTTON_TYPE_19_DATA = {STATE: [0], IDENTITY: [1]}  # button identity (how many buttons it has?)
CLIMATE_TYPE_09_DATA = {
    OPEN_IN_PERCENTAGE: [0],
    CURRENT_TEMP: [1],
    BATTERY: [2],
    REQUIRED_TEMP: [3],
}
#   BUS
RELAY_DATA = {
    STATE: [0],
    # SPARE: [1],
    TEMP_IN: [2, 3],
    RELAY_OVERFLOW: [4]
}

TWOCHANNELDIMMER_DATA = {
    TEMP_IN: [0, 1],
    DA3_22M: [2],
    # TODO CHECK SPARE: [3],
    DIM_OUT_1: [4],
    DIM_OUT_2: [5],
}


THERMOSTAT_DATA = {
    # FORCED_REPAIR: [0],
    # SPARE: [1]
    GTR3_50: [1],
    TEMP_IN: [2, 3],
    PLUS_MINUS_BUTTONS: [7],
    LIGHT_IN: [8, 9, 10, 11],
    AIN: [12, 13],
    HUMIDITY: [14, 15],
    DEW_POINT: [16, 17],
}

BUTTONARRAY_DATA = {
    GSB3_90SX: [0, 1],
    TEMP_IN: [2, 3],
    LIGHT_IN: [4, 5, 6, 7],
    AIN: [8, 9],
    HUMIDITY: [10, 11],
    DEW_POINT: [12, 13],
}

NODATA_DATA = {
    
}

INELS_DEVICE_TYPE_DATA_STRUCT_DATA = {
    RFSC_61 : TEMP_SENSOR_DATA,
    RFJA_12 : SHUTTER_TYPE_03_DATA,
    RFDAC_71B : DEVICE_TYPE_05_DATA,
    RFSTI_11B : DEVICE_TYPE_07_DATA,
    RFATV_2 : CLIMATE_TYPE_09_DATA,
    RFTI_10B : TEMP_SENSOR_DATA, #(?)
    RFGB_40 : BUTTON_TYPE_19_DATA,
    #BUS
    SA3_01B: RELAY_DATA,
    DA3_22M: TWOCHANNELDIMMER_DATA,
    GTR3_50: THERMOSTAT_DATA,
    GSB3_90SX: BUTTONARRAY_DATA
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

BUTTON_DEVICE_AMOUNT = {RFGB_40: 4}

# FRAGMENT/MQTT CONSTANTS
FRAGMENT_DOMAIN = "fragment_domain"
FRAGMENT_SERIAL_NUMBER = "fragment_serial_number"
FRAGMENT_STATE = "fragment_state"
FRAGMENT_DEVICE_TYPE = "fragment_device_type"
FRAGMENT_UNIQUE_ID = "fragment_unique_id"

MQTT_BROKER_CLIENT_NAME = "inels-mqtt"
MQTT_DISCOVER_TOPIC = "inels/status/#"

TOPIC_FRAGMENTS = {
    FRAGMENT_DOMAIN: 0,
    FRAGMENT_STATE: 1,
    FRAGMENT_SERIAL_NUMBER: 2,
    FRAGMENT_DEVICE_TYPE: 3,
    FRAGMENT_UNIQUE_ID: 4,
}

# TODO fix typo
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

class BusErrors(IntEnum) :
    """Bus errors in integer form"""
    BUS_2B_NOT_CALIBRATED = 0x7FFA,
    BUS_2B_NO_VALUE = 0x7FFB,
    BUS_2B_NOT_CONFIGURED = 0x7FFC,
    BUS_2B_OUT_OF_RANGE = 0x7FFD,
    BUS_2B_MEASURE = 0x7FFE,
    BUS_2B_NO_SENSOR = 0x7FFF,
    BUS_2B_NOT_COMMUNICATING = 0x7FF9,
    
    BUS_4B_NOT_CALIBRATED = 0x7FFFFFFA,
    BUS_4B_NO_VALUE = 0x7FFFFFFB,
    BUS_4B_NOT_CONFIGURED = 0x7FFFFFFC,
    BUS_4B_OUT_OF_RANGE = 0x7FFFFFFD,
    BUS_4B_MEASURE = 0x7FFFFFFE,
    BUS_4B_NO_SENSOR = 0x7FFFFFFF,
    BUS_4B_NOT_COMMUNICATING = 0x7FFFFFF9,



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
