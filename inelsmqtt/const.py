"""Constances of inels-mqtt."""

from __future__ import annotations

from enum import IntEnum
from typing import Final

DISCOVERY_TIMEOUT_IN_SEC = 5

NAME = "inels-mqtt"

GATEWAY = "gateway"
SWITCH = "switch"
SENSOR = "sensor"
LIGHT = "light"
COVER = "cover"
CLIMATE = "climate"
BUTTON = "button"
BINARY_SENSOR = "binary_sensor"
NUMBER = "number"

# RF
RF_SINGLE_SWITCH = "Single switching unit"  # 01
RF_SWITCHING_UNIT = "Switching unit"  # 02
RF_SHUTTERS = "Shutters"  # 3
RF_SINGLE_DIMMER = "Single dimmer"  # 04
RF_DIMMER = "Dimmer"  # 05
RF_DIMMER_RGB = "RGB dimmer"  # 06
RF_SWITCHING_UNIT_WITH_EXTERNAL_TEMPERATURE_SENSOR = "Switching unit with external temperature sensor"  # 07
# RF_SWITCHING_UNIT_WITH_TEMPERATURE_SENSORS = (
#     "Switching unit with temperature sensors"  # 08
# )
RF_WIRELESS_THERMOVALVE = "Wireless Thermovalve"  # 9
RF_TEMPERATURE_INPUT = "Temperature input"  # 10
RF_THERMOSTAT = "Thermostat"  # 12
RF_LIGHT_BULB = "Light bulb"  # 13
RF_FLOOD_DETECTOR = "Flood detector"  # 15
RF_DETECTOR = "Detector"  # 16
RF_MOTION_DETECTOR = "Motion detector"  # 17
RF_2_BUTTON_CONTROLLER = "Two button controller"  # 18
RF_CONTROLLER = "Controller"  # 19
RF_PULSE_CONVERTER = "Pulse converter"  # 20
RF_SHUTTER_UNIT = "Shutter unit"  # 21
RF_TEMPERATURE_HUMIDITY_SENSOR = "Temperature and humidity sensor"  # 29
SYSTEM_BITS = "Virtual system bits"
SYSTEM_INTEGERS = "Virtual system integers"

# BUS
SA3_01B = "SA3-01B"
DA3_22M = "DA3-22M"
GRT3_50 = "GRT3-50"
GRT3_70 = "GRT3-70"
GSB3_90SX = "GSB3-90SX"
SA3_04M = "SA3-04M"
SA3_012M = "SA3-012M"
SA3_014M = "SA3-014M"
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
JA3_018M = "JA3-018M"
JA3_014M = "JA3-014M"
DALI_DMX_UNIT = "DALI-DMX-Unit"
DALI_DMX_UNIT_2 = "DALI-DMX-Unit-2"
MSB3_40 = "MSB3-40"
MSB3_60 = "MSB3-60"
MSB3_90 = "MSB3-90"
GSB3_40_V2 = "GSB3-40-V2"
GSB3_60_V2 = "GSB3-60-V2"
GSB3_90_V2 = "GSB3-90-V2"
GSB3_40SX_V2 = "GSB3-40SX-V2"
GSB3_60SX_V2 = "GSB3-60SX-V2"
GSB3_90SX_V2 = "GSB3-90SX-V2"
MCD3_01 = "MCD3-01"
PMS3_01 = "PMS3-01"
INTEGERS = "INTEGERS"
BITS = "BITS"
DIMMER_RGBW = "RGBW dimmer"

# Virtual bus
VIRT_CONTR = "Virtual controller"
VIRT_HEAT_REG = "Heat virtual regulator"
VIRT_COOL_REG = "Cool virtual regulator"

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
WHITE = "white"


class Shutter_state(IntEnum):
    Open = 0
    Closed = 1
    Stop_up = 2
    Stop_down = 3


class Card_read_state(IntEnum):
    No_card = 0
    Success = 1
    Failure = 2


class Climate_modes(IntEnum):
    Off = 0
    Heat = 1
    Cool = 2
    Heat_cool = 3
    Auto = 4


class Climate_action(IntEnum):
    Off = 0
    Idle = 1
    Heating = 2
    Cooling = 3


class Climate_presets(IntEnum):
    Regular = 0
    Vacation = 1
    Holiday = 2


BUTTON_NUMBER = {
    "01": 1,
    "02": 2,
    "04": 3,
    "08": 4,
    "16": 5,
    "32": 6,
}

WSB3_AMOUNTS = {WSB3_20: 2, WSB3_20H: 2, WSB3_40: 4, WSB3_40H: 4}

GSB3_AMOUNTS = {
    GSB3_20SX: 2,
    GSB3_40SX: 4,
    GSB3_60SX: 6,
    GSB3_90SX: 9,
    GBP3_60: 6,
    GSB3_40_V2: 4,
    GSB3_60_V2: 6,
    GSB3_90_V2: 9,
    GSB3_40SX_V2: 4,
    GSB3_60SX_V2: 6,
    GSB3_90SX_V2: 9,
    MSB3_40: 4,
    MSB3_60: 6,
    MSB3_90: 9,
}

VIRT_CONT_STATUS_TABLE = {
    0: "User control",
    1: "Two temperature autonomous",
    2: "Single temperature autonomous",
}

VIRT_REG_STATUS_TABLE = {
    1: "Enabled",
    2: "Error actual temperature",
    4: "Error required temperature",
    8: "Disabled",
    16: "Error critical temperature",
    32: "Error anti-freeze temperature",
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

GW_CONNECTED = {
    b'{"status":true}': True,
    b'{"status":false}': False,
    b'{"status": true}': True,
    b'{"status": false}': False,
}

DEVICE_CONNECTED = {
    "on\n": True,
    "off\n": False,
    '{"status": true}': True,
    '{"status": false}': False,
}


BUS_SENSOR_NOT_CALIBRATED = "Sensor error: not calibrated"
BUS_SENSOR_NO_VALUE = "Sensor error: no value"
BUS_SENSOR_NOT_CONFIGURED = "Sensor error: not configured"
BUS_SENSOR_OUT_OF_RANGE = "Sensor error: value out of range"
BUS_SENSOR_MEASURE = "Sensor error: measurement error"
BUS_SENSOR_NO_SENSOR = "Sensor error: no sensor"
BUS_SENSOR_NOT_COMMUNICATING = "Sensor error: no internal communication"
BUS_SENSOR_ERRORS = {
    0x9: BUS_SENSOR_NOT_COMMUNICATING,
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
