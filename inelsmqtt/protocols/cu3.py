from __future__ import annotations

import json
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    from inelsmqtt.utils.core import DeviceValue

from inelsmqtt.const import (
    ADC3_60M,
    AIN,
    ALERT,
    AOUT,
    BITS,
    BUTTON,
    CARD_ID,
    CLIMATE,
    CONTROL_MODE,
    COVER,
    CRITICAL_MAX_TEMP,
    CRITICAL_MIN_TEMP,
    CURRENT_TEMP,
    DA3_22M,
    DA3_66M,
    DAC3_04B,
    DAC3_04M,
    DALI,
    DALI_DMX_UNIT,
    DALI_DMX_UNIT_2,
    DCDA_33M,
    DEW_POINT,
    DIM_OUT_1,
    DIM_OUT_2,
    DIMMER_RGBW,
    DIN,
    DMD3_1,
    FA3_612M,
    GBP3_60,
    GCH3_31,
    GCR3_11,
    GDB3_10,
    GRT3_50,
    GRT3_70,
    GSB3_20SX,
    GSB3_40_V2,
    GSB3_40SX,
    GSB3_40SX_V2,
    GSB3_60_V2,
    GSB3_60SX,
    GSB3_60SX_V2,
    GSB3_90_V2,
    GSB3_90SX,
    GSB3_90SX_V2,
    GSB3_AMOUNTS,
    GSP3_100,
    HUMIDITY,
    IDRT3_1,
    IM3_20B,
    IM3_40B,
    IM3_80B,
    IM3_140M,
    IN,
    INTEGERS,
    IOU3_108M,
    JA3_014M,
    JA3_018M,
    LIGHT,
    LIGHT_IN,
    MAX_TEMP,
    MCD3_01,
    MSB3_40,
    MSB3_60,
    MSB3_90,
    NUMBER,
    OUT,
    PLUS_MINUS_BUTTONS,
    PMS3_01,
    PUBLIC_HOLIDAY,
    RC3_610DALI,
    RELAY,
    RELAY_OVERFLOW,
    REQUIRED_COOL_TEMP,
    REQUIRED_HEAT_TEMP,
    SA3_01B,
    SA3_012M,
    SA3_014M,
    SA3_02B,
    SA3_02M,
    SA3_022M,
    SA3_04M,
    SA3_06M,
    SENSOR,
    SHUTTER,
    STATE,
    SW,
    SWITCH,
    TEMP_CORRECTION,
    TEMP_IN,
    TEMP_OUT,
    TI3_10B,
    TI3_40B,
    TI3_60M,
    VALVE,
    VIRT_CONTR,
    VIRT_COOL_REG,
    VIRT_HEAT_REG,
    WSB3_20,
    WSB3_20H,
    WSB3_40,
    WSB3_40H,
    WSB3_AMOUNTS,
    Climate_action,
    Climate_modes,
    Shutter_state,
)
from inelsmqtt.utils.common import (
    AOUTLight,
    Bit,
    DALILight,
    DataDict,
    Formatter,
    LightCoaToa,
    Number,
    Relay,
    RGBWLight,
    Shutter,
    SimpleLight,
    SimpleRelay,
    WarmLight,
    break_into_bytes,
    new_object,
    parse_formated_json,
    trim_inels_status_bytes,
    trim_inels_status_values,
)


class Base:
    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        return ""


class DT_100:
    class Command(IntEnum):
        ON = 0b111
        OFF = 0b110

    INELS_TYPE = SA3_01B
    HA_TYPE = SWITCH
    TYPE_ID = "100"

    DATA: DataDict = {RELAY: [0], TEMP_IN: [2, 3], RELAY_OVERFLOW: [4]}

    RELAY_SET = {
        True: Command.ON,
        False: Command.OFF,
    }

    @staticmethod
    def create_command_payload(cmd: List[int]) -> str:
        return Formatter.format_data(cmd)

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        re = []
        re.append(int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, RELAY, ""), 16) & 1 != 0)

        temp = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")

        relay_overflow = []
        relay_overflow.append(
            int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, RELAY_OVERFLOW, ""), 16) == 1
        )

        relay = [Relay(is_on=re[i], overflow=relay_overflow[i]) for i in range(len(re))]

        return new_object(
            # re=re,
            temp_in=temp,
            # relay_overflow=relay_overflow
            relay=relay,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        cmd: List[int] = []
        if hasattr(device_value.ha_value, "simple_relay"):
            for re in device_value.ha_value.simple_relay:
                cmd.append(cls.RELAY_SET[re.is_on])
        elif hasattr(device_value.ha_value, "relay"):
            for re in device_value.ha_value.relay:
                cmd.append(cls.RELAY_SET[re.is_on])

        return cls.create_command_payload(cmd)


class DT_101(Base):
    INELS_TYPE = DA3_22M
    HA_TYPE = LIGHT
    TYPE_ID = "101"

    DATA: DataDict = {
        TEMP_IN: [0, 1],
        DA3_22M: [2],
        DIM_OUT_1: [4],
        DIM_OUT_2: [5],
    }

    @staticmethod
    def create_command_payload(out1: int = 0, out2: int = 0) -> str:
        return Formatter.format_data([0, 0, 0, 0, out1, out2])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        temp = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")

        state = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DA3_22M, "")
        state_hex_str = f"0x{state}"
        state_bin_str = f"{int(state_hex_str, 16):0>8b}"

        toa = [  # thermal overload alarm
            state_bin_str[3] == "1",
            state_bin_str[2] == "1",
        ]
        coa = [  # current overload alrm
            state_bin_str[1] == "1",  # 6
            state_bin_str[0] == "1",  # 7
        ]

        out1 = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, DIM_OUT_1, ""), 16)

        out2 = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, DIM_OUT_2, ""), 16)
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

        return new_object(
            # May not be that interesting for HA
            sw=[
                state_bin_str[7] == "1",  # 0
                state_bin_str[6] == "1",  # 1
            ],
            din=[state_bin_str[5] == "1", state_bin_str[4] == "1"],
            temp_in=temp,
            light_coa_toa=light_coa_toa,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        out1 = round(device_value.ha_value.light_coa_toa[0].brightness, -1)
        out1 = out1 if out1 < 100 else 100

        out2 = round(device_value.ha_value.light_coa_toa[1].brightness, -1)
        out2 = out2 if out2 < 100 else 100

        return cls.create_command_payload(out1, out2)


class DT_102(Base):
    INELS_TYPE = GRT3_50
    HA_TYPE = SENSOR
    TYPE_ID = "102"

    DATA: DataDict = {
        GRT3_50: [1],
        TEMP_IN: [2, 3],
        PLUS_MINUS_BUTTONS: [7],
        LIGHT_IN: [8, 9, 10, 11],
        AIN: [12, 13],
        HUMIDITY: [14, 15],
        DEW_POINT: [16, 17],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, GRT3_50, "")
        digital_inputs_hex_str = f"0x{digital_inputs}"
        digital_inputs_bin_str = f"{int(digital_inputs_hex_str, 16):0>8b}"

        plusminus = trim_inels_status_values(device_value.inels_status_value, cls.DATA, PLUS_MINUS_BUTTONS, "")
        plusminus = f"0x{plusminus}"
        plusminus = f"{int(plusminus, 16):0>8b}"

        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        light_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, LIGHT_IN, "")
        ain = trim_inels_status_values(device_value.inels_status_value, cls.DATA, AIN, "")
        humidity = trim_inels_status_values(device_value.inels_status_value, cls.DATA, HUMIDITY, "")
        dewpoint = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DEW_POINT, "")

        return new_object(
            # digital inputs
            din=[  # 2
                digital_inputs_bin_str[7] == "1",  # 0 -> 7, reverse endianness
                digital_inputs_bin_str[6] == "1",
            ],
            interface=[  # 5
                digital_inputs_bin_str[5] == "1",
                digital_inputs_bin_str[4] == "1",
                digital_inputs_bin_str[3] == "1",
                digital_inputs_bin_str[2] == "1",
                digital_inputs_bin_str[1] == "1",  # 6
                plusminus[7] == "1",  # plus
                plusminus[6] == "1",  # minus
            ],
            temp_in=temp_in,
            light_in=light_in,
            ain=ain,
            humidity=humidity,
            dewpoint=dewpoint,
            backlit=False,
        )


class DT_103(Base):
    INELS_TYPE = GSB3_90SX
    HA_TYPE = BUTTON
    TYPE_ID = "103"

    DATA: DataDict = {
        GSB3_90SX: [0, 1],
        TEMP_IN: [2, 3],
        LIGHT_IN: [4, 5, 6, 7],
        AIN: [8, 9],
        HUMIDITY: [10, 11],
        DEW_POINT: [12, 13],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, GSB3_90SX, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"

        temp = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")

        light_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, LIGHT_IN, "")

        ain = trim_inels_status_values(device_value.inels_status_value, cls.DATA, AIN, "")

        humidity = trim_inels_status_values(device_value.inels_status_value, cls.DATA, HUMIDITY, "")

        dewpoint = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DEW_POINT, "")

        return new_object(
            interface=[
                digital_inputs[7] == "1",  # 0
                digital_inputs[6] == "1",
                digital_inputs[5] == "1",
                digital_inputs[4] == "1",
                digital_inputs[3] == "1",
                digital_inputs[2] == "1",
                digital_inputs[1] == "1",
                digital_inputs[0] == "1",
                digital_inputs[15] == "1",  # 8
            ],
            din=[
                digital_inputs[14] == "1",  # 9
                digital_inputs[13] == "1",  # 10
            ],
            prox=digital_inputs[12] == "1",  # 11
            temp_in=temp,
            light_in=light_in,
            ain=ain,
            humidity=humidity,
            dewpoint=dewpoint,
            disabled=False,
            backlit=False,
        )


class DT_104(DT_100):
    INELS_TYPE = SA3_02B
    HA_TYPE = SWITCH
    TYPE_ID = "104"

    DATA: DataDict = {
        RELAY: [0, 1],
        TEMP_IN: [2, 3],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        simple_relay: list[SimpleRelay] = []
        for relay in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")

        return new_object(
            simple_relay=simple_relay,
            temp_in=temp_in,
        )


class DT_105(DT_100):
    INELS_TYPE = SA3_02M
    HA_TYPE = SWITCH
    TYPE_ID = "105"

    DATA: DataDict = {RELAY: [0, 1], SW: [2]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        simple_relay: list[SimpleRelay] = []
        for relay in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"
        sw = []
        for i in range(2):
            sw.append(digital_inputs[7 - i] == "1")

        return new_object(
            simple_relay=simple_relay,
            sw=sw,
        )


class DT_106(DT_100):
    INELS_TYPE = SA3_04M
    HA_TYPE = SWITCH
    TYPE_ID = "106"

    DATA: DataDict = {
        RELAY: [0, 1, 2, 3],
        SW: [4],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        simple_relay: list[SimpleRelay] = []
        for relay in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"
        sw = []
        for i in range(4):
            sw.append(digital_inputs[7 - i] == "1")

        return new_object(
            simple_relay=simple_relay,
            sw=sw,
        )


class DT_107(DT_100):
    INELS_TYPE = SA3_06M
    HA_TYPE = SWITCH
    TYPE_ID = "107"

    DATA: DataDict = {
        RELAY: [0, 1, 2, 3, 4, 5],
        SW: [6],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        simple_relay: list[SimpleRelay] = []
        for relay in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"
        sw = []
        for i in range(6):
            sw.append(digital_inputs[7 - i] == "1")

        return new_object(
            simple_relay=simple_relay,
            sw=sw,
        )


class DT_108(DT_100):
    INELS_TYPE = SA3_012M
    HA_TYPE = SWITCH
    TYPE_ID = "108"

    DATA: DataDict = {
        RELAY: list(range(12)),
        SW: [12, 13],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        simple_relay: list[SimpleRelay] = []
        for relay in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=((int(relay, 16) & 1) != 0)))

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"

        sw = []
        for i in range(8):
            sw.append(digital_inputs[7 - i] == "1")
        for i in range(4):
            sw.append(digital_inputs[15 - i] == "1")

        return new_object(
            simple_relay=simple_relay,
            sw=sw,
        )


class DT_109(Base):
    class Command(IntEnum):
        OPEN = 0b111
        CLOSE = 0b110

    INELS_TYPE = SA3_022M
    HA_TYPE = SWITCH
    TYPE_ID = "109"

    DATA: DataDict = {
        RELAY: list(range(16)),
        SHUTTER: [16, 17],
        VALVE: [18, 19, 20, 21],
        SW: [22, 23],
        ALERT: [24, 25],
        RELAY_OVERFLOW: [26, 27],
        SA3_022M: [28],
    }

    RELAY_SET = {
        True: Command.OPEN,
        False: Command.CLOSE,
    }

    SHUTTER_STATE_SET = {
        Shutter_state.Open: [Command.OPEN, Command.CLOSE],
        Shutter_state.Closed: [Command.CLOSE, Command.OPEN],
        Shutter_state.Stop_up: [Command.CLOSE, Command.CLOSE],
        Shutter_state.Stop_down: [Command.CLOSE, Command.CLOSE],
    }

    @staticmethod
    def create_command_payload(cmd: List[int]) -> str:
        return Formatter.format_data(cmd)

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        re = []
        for _relay in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, RELAY):
            re.append((int(_relay, 16) & 1) != 0)

        overflows = []
        alerts = trim_inels_status_values(device_value.inels_status_value, cls.DATA, RELAY_OVERFLOW, "")
        alerts = f"0x{alerts}"
        alerts = f"{int(alerts, 16):0>16b}"
        for i in range(8):  # 0-7
            overflows.append(alerts[7 - i] == "1")
        for i in range(8):  # 8-15
            overflows.append(alerts[15 - i] == "1")

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"

        sw = []
        for i in range(8):
            sw.append(digital_inputs[7 - i] == "1")
        for i in range(8):
            sw.append(digital_inputs[15 - i] == "1")

        relay = [Relay(is_on=re[i], overflow=overflows[i]) for i in range(len(re))]

        shutter = [
            int(s, 16) & 1 != 0 for s in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, SHUTTER)
        ]

        simple_shutters = []
        shutters = list(zip(shutter[::2], shutter[1::2], strict=True))
        for s in shutters:
            if s[0]:
                state = Shutter_state.Open
            elif s[1]:
                state = Shutter_state.Closed
            else:
                state = Shutter_state.Stop_down
            simple_shutters.append(Shutter(state=state, is_closed=None))

        valve = []
        for v in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, VALVE):
            valve.append((int(v, 16) & 1) != 0)

        return new_object(
            relay=relay,
            shutter_motors=shutter,
            simple_shutters=simple_shutters,
            valve=valve,
            sw=sw,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        cmd: List[int] = []
        for r in device_value.ha_value.relay:
            cmd.append(cls.RELAY_SET[r.is_on])
        for s in device_value.ha_value.simple_shutters:
            cmd.extend(cls.SHUTTER_STATE_SET[s.state])
        for v in device_value.ha_value.valve:
            cmd.append(cls.RELAY_SET[v])
        return cls.create_command_payload(cmd)


class DT_111:
    class Command(IntEnum):
        ON = 0b111
        OFF = 0b110

    INELS_TYPE = FA3_612M
    HA_TYPE = SWITCH
    TYPE_ID = "111"

    DATA: DataDict = {
        FA3_612M: [0, 1, 2],
        RELAY_OVERFLOW: [3],
        AOUT: list(range(4, 8)),
        RELAY: list(range(8, 16)),
        AIN: list(range(16, 28)),
    }

    RELAY_SET = {
        True: Command.ON,
        False: Command.OFF,
    }

    @staticmethod
    def create_command_payload(cmd: List[int]) -> str:
        return Formatter.format_data([0, 0, 0, 0] + cmd)

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, FA3_612M, "")
        inputs = f"0x{inputs}"
        inputs = f"{int(inputs, 16):0>24b}"

        din = []
        for i in range(3):
            din.append(inputs[7 - i] == "1")

        aout_coa = []
        for i in range(4, 8):
            aout_coa.append(inputs[7 - i] == "1")

        sw = []
        for i in range(8):
            sw.append(inputs[15 - i] == "1")

        roa = []
        for i in range(3):
            roa.append(inputs[23 - i] == "1")

        sw.append(inputs[23 - 3] == "1")

        overflows = trim_inels_status_values(device_value.inels_status_value, cls.DATA, RELAY_OVERFLOW, "")
        overflows = f"0x{overflows}"
        overflows = f"{int(overflows, 16):0>8b}"

        i = 0
        aout = []
        for a in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, AOUT):
            aout.append(
                AOUTLight(
                    brightness=int(a, 16),
                    aout_coa=aout_coa[i],
                )
            )
            i = i + 1

        re = []
        for relay in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, RELAY):
            re.append((int(relay, 16) & 1) != 0)

        valves = [[re[0], re[1]], [re[2], re[3]]]
        fan_speed = 0
        if re[6]:  # speed 3
            fan_speed = 3
        elif re[5]:  # speed 2
            fan_speed = 2
        elif re[4]:  # speed 1
            fan_speed = 1

        heating_out = re[7]

        ains = []
        ain_bytes = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, AIN)
        for i in range(int(len(ain_bytes) / 4)):
            ains.append(ain_bytes[4 * i] + ain_bytes[4 * i + 1] + ain_bytes[4 * i + 2] + ain_bytes[4 * i + 3])

        last_status_val = device_value.inels_status_value

        return new_object(
            din=din,
            sw=sw,
            aout=aout,
            valves=valves,
            fan_speed=fan_speed,
            heating_out=heating_out,
            ains=ains,
            last_status_val=last_status_val,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        original_status = device_value.ha_value.last_status_val.split("\n")

        set_val = []
        for a in device_value.ha_value.aout:
            set_val.append(a.brightness)

        set_val.extend(int(original_status[8 + i], 16) for i in range(4))

        set_val.extend([cls.RELAY_SET[device_value.ha_value.fan_speed == (i + 1)] for i in range(3)])

        set_val.append(int(original_status[15], 16))

        return cls.create_command_payload(set_val)


class DT_112(DT_100):
    INELS_TYPE = IOU3_108M
    HA_TYPE = SWITCH
    TYPE_ID = "112"

    DATA: DataDict = {
        RELAY: list(range(8)),
        TEMP_IN: [8, 9, 10, 11, 12, 13, 14, 15],
        DIN: [24],
        RELAY_OVERFLOW: [25],
        ALERT: [26],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        re = []
        for _relay in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, RELAY):
            re.append((int(_relay, 16) & 1) != 0)

        temps_str = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        temps: List[str] = [temps_str[0:8], temps_str[8:16]]

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        din = []
        for i in range(8):
            din.append(digital_inputs[7 - i] == "1")

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, RELAY_OVERFLOW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        relay_overflow = []
        for _ in range(8):
            relay_overflow.append(digital_inputs[7 - 1] == "1")

        relay = [Relay(is_on=re[i], overflow=relay_overflow[i]) for i in range(len(re))]

        return new_object(
            relay=relay,
            # re=re,
            temps=temps,
            din=din,
            # relay_overflow=relay_overflow,
        )


class DT_114(Base):
    class Command(IntEnum):
        ON = 0b111
        OFF = 0b110

    INELS_TYPE = RC3_610DALI
    HA_TYPE = SWITCH
    TYPE_ID = "114"

    DATA: DataDict = {
        TEMP_IN: [2, 3, 18, 19],
        AOUT: [4, 5],
        RELAY: list(range(8, 16)),
        DALI: [20, 21, 22, 23, 28, 29, 30, 31, 36, 37, 38, 39, 44, 45, 46, 47],
        DIN: [24],
        RELAY_OVERFLOW: [25],
        ALERT: [26],
    }

    RELAY_SET = {
        True: Command.ON,
        False: Command.OFF,
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        # aout
        aout_brightness = []
        for a in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, AOUT):
            aout_brightness.append(int(a, 16))

        # relays
        re = []
        for _relay in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, RELAY):
            re.append((int(_relay, 16) & 1) != 0)

        # temperatures
        temps = []
        temp_bytes = trim_inels_status_bytes(
            device_value.inels_status_value,
            cls.DATA,
            TEMP_IN,
        )
        for i in range(int(len(temp_bytes) / 2)):
            temps.append(temp_bytes[2 * i] + temp_bytes[2 * i + 1])

        # digital inputs
        din = []
        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        for i in range(6):
            din.append(digital_inputs[7 - i] == "1")

        relay_overflow = []
        overflows = trim_inels_status_values(device_value.inels_status_value, cls.DATA, RELAY_OVERFLOW, "")
        overflows = f"0x{overflows}"
        overflows = f"{int(overflows, 16):0>8b}"
        for i in range(len(re)):
            relay_overflow.append(overflows[7 - i] == "1")

        relay = [Relay(is_on=re[i], overflow=relay_overflow[i]) for i in range(len(re))]

        sync_error = []
        aout_coa = []
        alerts = trim_inels_status_values(device_value.inels_status_value, cls.DATA, ALERT, "")
        alerts = f"0x{alerts}"
        alerts = f"{int(alerts, 16):0>8b}"

        for i in range(4):
            sync_error.append(alerts[7 - i] == "1")
        for i in range(4, 6):
            aout_coa.append(alerts[7 - i] == "1")

        aout = []
        for i in range(2):
            aout.append(AOUTLight(brightness=aout_brightness[i], aout_coa=aout_coa[i]))

        alert_dali_power = alerts[1] == "1"
        alert_dali_communication = alerts[0] == "1"

        dali_raw = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, DALI)
        dali = []
        for d in dali_raw:
            dali.append(
                DALILight(
                    brightness=int(d, 16),
                    alert_dali_communication=alert_dali_communication,
                    alert_dali_power=alert_dali_power,
                )
            )

        return new_object(
            relay=relay,
            temps=temps,
            din=din,
            aout=aout,
            dali=dali,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        set_val = [0] * 4

        set_val.extend([a.brightness for a in device_value.ha_value.aout])
        set_val.extend([0] * 2)

        set_val.extend([cls.RELAY_SET[r.is_on] for r in device_value.ha_value.relay])
        set_val.extend([0] * 4)

        set_val.extend([device_value.ha_value.dali[i].brightness for i in range(4)])
        set_val.extend([0] * 4)

        set_val.extend([device_value.ha_value.dali[i].brightness for i in range(4, 8)])
        set_val.extend([0] * 4)

        set_val.extend([device_value.ha_value.dali[i].brightness for i in range(8, 12)])
        set_val.extend([0] * 4)

        set_val.extend([device_value.ha_value.dali[i].brightness for i in range(12, 16)])

        return Formatter.format_data(set_val)


class DT_115(Base):
    INELS_TYPE = IM3_20B
    HA_TYPE = SENSOR
    TYPE_ID = "115"

    DATA: DataDict = {
        IN: [0],
        TEMP_IN: [1, 2],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        binary_input = []
        inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, IN, "")
        inputs = f"0x{inputs}"
        inputs = f"{int(inputs, 16):0>8b}"
        for i in range(2):
            binary_input.append(int(inputs[7 - 2 * i - 1] + inputs[7 - 2 * i], 2))

        temp = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        return new_object(
            input=binary_input,
            temp_in=temp,
        )


class DT_116(Base):
    INELS_TYPE = IM3_40B
    HA_TYPE = SENSOR
    TYPE_ID = "116"

    DATA: DataDict = {
        IN: [0],
        TEMP_IN: [1, 2],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        binary_input = []
        inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, IN, "")
        inputs = f"0x{inputs}"
        inputs = f"{int(inputs, 16):0>8b}"
        for i in range(4):
            binary_input.append(int(inputs[7 - 2 * i - 1] + inputs[7 - 2 * i], 2))

        temp = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        return new_object(
            input=binary_input,
            temp_in=temp,
        )


class DT_117(Base):
    INELS_TYPE = IM3_80B
    HA_TYPE = SENSOR
    TYPE_ID = "117"

    DATA: DataDict = {
        IN: [0, 1],
        TEMP_IN: [2, 3],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        binary_input = []
        binary_input2 = []
        inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, IN, "")
        inputs = f"0x{inputs}"
        inputs = f"{int(inputs, 16):0>16b}"
        for i in range(4):
            binary_input.append(int(inputs[7 - 2 * i - 1] + inputs[7 - 2 * i], 2))
            binary_input2.append(int(inputs[15 - 2 * i - 1] + inputs[15 - 2 * i], 2))
        binary_input.extend(binary_input2)

        temp = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        return new_object(
            input=binary_input,
            temp=temp,
        )


class DT_120(Base):
    INELS_TYPE = DMD3_1
    HA_TYPE = SENSOR
    TYPE_ID = "120"

    DATA: DataDict = {
        LIGHT_IN: [0, 1, 2, 3],
        TEMP_IN: [4, 5],
        HUMIDITY: [6, 7],
        DMD3_1: [8],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        light_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, LIGHT_IN, "")
        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        humidity = trim_inels_status_values(device_value.inels_status_value, cls.DATA, HUMIDITY, "")
        motion_str = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DMD3_1, "")
        motion_str = f"0x{motion_str}"
        motion_str = f"{int(motion_str, 16):0>8b}"

        motion = motion_str[7] == "1"

        return new_object(
            light_in=light_in,
            temp_in=temp_in,
            humidity=humidity,
            motion=motion,
        )


class DT_121(Base):
    INELS_TYPE = IM3_140M
    HA_TYPE = SENSOR
    TYPE_ID = "121"

    DATA: DataDict = {IN: [0, 1, 2, 3]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        binary_input = []
        binary_input2 = []
        binary_input3 = []
        inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, IN, "")
        inputs = f"0x{inputs}"
        inputs = f"{int(inputs, 16):0>32b}"

        for i in range(4):
            binary_input.append(int(inputs[7 - 2 * i - 1] + inputs[7 - 2 * i], 2))
            binary_input2.append(int(inputs[15 - 2 * i - 1] + inputs[15 - 2 * i], 2))
            binary_input3.append(int(inputs[23 - 2 * i - 1] + inputs[23 - 2 * i], 2))
        binary_input.extend(binary_input2)
        binary_input.extend(binary_input3)

        for i in range(2):
            binary_input.append(int(inputs[31 - 2 * i - 1] + inputs[31 - 2 * i], 2))

        return new_object(input=binary_input)


class DT_122(Base):
    INELS_TYPE = WSB3_20
    HA_TYPE = SENSOR
    TYPE_ID = "122"

    DATA: DataDict = {
        SW: [0],
        DIN: [1],
        TEMP_IN: [2, 3],
        AIN: [4, 5],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        switches = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        interface = []  # up/down buttons
        for i in range(WSB3_AMOUNTS[device_value.inels_type]):
            interface.append(switches[7 - i] == "1")

        din = []
        for i in range(2):
            din.append(digital_inputs[7 - i] == "1")

        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        ain = trim_inels_status_values(device_value.inels_status_value, cls.DATA, AIN, "")

        return new_object(
            interface=interface,
            din=din,
            temp_in=temp_in,
            ain=ain,
        )


class DT_123(DT_122):
    INELS_TYPE = WSB3_40
    HA_TYPE = SENSOR
    TYPE_ID = "123"


class DT_124(Base):
    INELS_TYPE = WSB3_20H
    HA_TYPE = SENSOR
    TYPE_ID = "124"

    DATA: DataDict = {
        SW: [0],
        DIN: [1],
        TEMP_IN: [2, 3],
        AIN: [4, 5],
        HUMIDITY: [6, 7],
        DEW_POINT: [8, 9],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        switches = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"
        interface = []  # up/down buttons
        din = []
        for i in range(WSB3_AMOUNTS[device_value.inels_type]):
            interface.append(switches[7 - i] == "1")
        for i in range(2):
            din.append(digital_inputs[7 - i] == "1")

        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")

        ain = trim_inels_status_values(device_value.inels_status_value, cls.DATA, AIN, "")

        humidity = trim_inels_status_values(device_value.inels_status_value, cls.DATA, HUMIDITY, "")

        dewpoint = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DEW_POINT, "")

        return new_object(
            interface=interface,
            din=din,
            temp_in=temp_in,
            ain=ain,
            humidity=humidity,
            dewpoint=dewpoint,
        )


class DT_125(DT_124):
    INELS_TYPE = WSB3_40H
    HA_TYPE = SENSOR
    TYPE_ID = "125"


class DT_128:
    class Command(IntEnum):
        ON = 0x04
        OFF = 0x00

    INELS_TYPE = GCR3_11
    HA_TYPE = SWITCH
    TYPE_ID = "128"

    DATA: DataDict = {  # Card holder/reader
        STATE: [0, 1],
        CARD_ID: list(range(4, 12)),
        LIGHT_IN: [12, 13, 14, 15],
        TEMP_IN: [16, 17],
    }

    @staticmethod
    def create_command_payload(cmd: int = 0) -> str:
        return Formatter.format_data([cmd, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        state = trim_inels_status_values(device_value.inels_status_value, cls.DATA, STATE, "")
        state = f"0x{state}"
        state = f"{int(state, 16):0>16b}"

        simple_relay: list[SimpleRelay] = []
        simple_relay.append(SimpleRelay(is_on=bool(int(state[5]))))

        card_present = state[4] == "1"

        card_id = trim_inels_status_values(device_value.inels_status_value, cls.DATA, CARD_ID, "")
        card_id_int = int(card_id, 16)
        # if card removed before
        if card_id_int == 0 and device_value.last_value is not None:
            card_id = device_value.last_value.card_id

        interface = [state[0] == "1", state[12] == "1", state[10] == "1"]

        light_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, LIGHT_IN, "")
        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")

        return new_object(
            simple_relay=simple_relay,
            interface=interface,
            temp_in=temp_in,
            card_present=card_present,
            card_id=card_id,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        cmd = cls.Command.ON if device_value.ha_value.simple_relay[0].is_on else cls.Command.OFF
        return cls.create_command_payload(cmd)


class DT_129(DT_128):
    INELS_TYPE = GCH3_31
    HA_TYPE = SWITCH
    TYPE_ID = "129"


class DT_136(Base):
    INELS_TYPE = GSP3_100
    HA_TYPE = BUTTON
    TYPE_ID = "136"

    DATA: DataDict = {
        SW: [0],
        DIN: [1],
        TEMP_IN: [2, 3],
        LIGHT_IN: [4, 5, 6, 7],
        AIN: [8, 9],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        switches = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        interface = []
        for i in range(8):
            interface.append(switches[7 - i] == "1")

        din = []
        for i in range(2):
            interface.append(digital_inputs[7 - i] == "1")
            din.append(digital_inputs[5 - i] == "1")

        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        light_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, LIGHT_IN, "")
        ain = trim_inels_status_values(device_value.inels_status_value, cls.DATA, AIN, "")

        return new_object(
            interface=interface,
            din=din,
            temp_in=temp_in,
            light_in=light_in,
            ain=ain,
        )


class DT_137(Base):
    INELS_TYPE = GDB3_10
    HA_TYPE = BUTTON
    TYPE_ID = "137"

    DATA: DataDict = {
        SW: [0],
        DIN: [1],
        TEMP_IN: [2, 3],
        LIGHT_IN: [4, 5, 6, 7],
        AIN: [8, 9],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        switches = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        interface = []
        din = []
        for i in range(3):
            interface.append(switches[6 - 2 * i] == "1")
        for i in range(2):
            din.append(digital_inputs[7 - i] == "1")

        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        light_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, LIGHT_IN, "")
        ain = trim_inels_status_values(device_value.inels_status_value, cls.DATA, AIN, "")

        return new_object(
            interface=interface,
            din=din,
            temp_in=temp_in,
            light_in=light_in,
            ain=ain,
        )


class DT_138(Base):
    INELS_TYPE = GSB3_40SX
    HA_TYPE = BUTTON
    TYPE_ID = "138"

    DATA: DataDict = {
        SW: [0],
        DIN: [1],
        TEMP_IN: [2, 3],
        LIGHT_IN: [4, 5, 6, 7],
        AIN: [8, 9],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        switches = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        interface = []
        for i in range(GSB3_AMOUNTS[device_value.inels_type]):
            interface.append(switches[7 - i] == "1")

        din = []
        for i in range(2):
            din.append(digital_inputs[7 - i] == "1")

        temp = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")

        light_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, LIGHT_IN, "")

        ain = trim_inels_status_values(device_value.inels_status_value, cls.DATA, AIN, "")

        return new_object(
            interface=interface,
            din=din,
            temp_in=temp,
            light_in=light_in,
            ain=ain,
        )


class DT_139(DT_138):
    INELS_TYPE = GSB3_60SX
    HA_TYPE = BUTTON
    TYPE_ID = "139"


class DT_140(DT_138):
    INELS_TYPE = GSB3_20SX
    HA_TYPE = BUTTON
    TYPE_ID = "140"


class DT_141(DT_138):
    INELS_TYPE = GBP3_60
    HA_TYPE = BUTTON
    TYPE_ID = "141"


class DT_143(Base):
    INELS_TYPE = GSB3_40_V2
    HA_TYPE = SENSOR
    TYPE_ID = "143"

    DATA: DataDict = {
        SW: [0],
        DIN: [1],
        TEMP_IN: [2, 3],
        LIGHT_IN: [4, 5, 6, 7],
        AIN: [8, 9],
        HUMIDITY: [10, 11],
        DEW_POINT: [12, 13],
    }

    INTERFACE_BUTTON_COUNT = 4

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        switches = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        interface = []

        # Determine the number of buttons to process based on INTERFACE_BUTTON_COUNT
        num_buttons = cls.INTERFACE_BUTTON_COUNT if cls.INTERFACE_BUTTON_COUNT < 8 else cls.INTERFACE_BUTTON_COUNT - 1

        # Append states from 'switches' based on the number of buttons
        for i in range(num_buttons):
            interface.append(switches[7 - i] == "1")

        # If there are 8 or more buttons, use the last digital input for the button
        if cls.INTERFACE_BUTTON_COUNT >= 8:
            interface.append(digital_inputs[7] == "1")

        din = [digital_inputs[6] == "1"]
        # if cls.DIN_COUNT > 1:
        #     din.append(digital_inputs[5] == "1")

        prox = digital_inputs[4] == "1"

        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")

        light_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, LIGHT_IN, "")

        ain = trim_inels_status_values(device_value.inels_status_value, cls.DATA, AIN, "")

        humidity = trim_inels_status_values(device_value.inels_status_value, cls.DATA, HUMIDITY, "")

        dewpoint = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DEW_POINT, "")

        return new_object(
            interface=interface,
            din=din,
            prox=prox,
            temp_in=temp_in,
            light_in=light_in,
            ain=ain,
            humidity=humidity,
            dewpoint=dewpoint,
        )


class DT_144(DT_143):
    INELS_TYPE = GSB3_60_V2
    HA_TYPE = SENSOR
    TYPE_ID = "144"

    INTERFACE_BUTTON_COUNT = 6


class DT_146(DT_143):
    INELS_TYPE = GSB3_90_V2
    HA_TYPE = SENSOR
    TYPE_ID = "146"

    INTERFACE_BUTTON_COUNT = 9


class DT_147:
    INELS_TYPE = DAC3_04B
    HA_TYPE = LIGHT
    TYPE_ID = "147"

    DATA: DataDict = {
        TEMP_OUT: [0, 1],
        ALERT: [2],
        OUT: [4, 5, 6, 7],
    }

    @staticmethod
    def create_command_payload(cmd: List[int]) -> str:
        return Formatter.format_data([0, 0, 0, 0] + cmd)

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        temp_out = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_OUT, "")

        aout_alert = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, ALERT, ""), 16) != 0

        aout_str = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, OUT)
        aout = []
        for d in aout_str:
            brightness = min(int(d, 16), 100)
            aout.append(
                AOUTLight(
                    brightness=brightness,
                    aout_coa=aout_alert,
                )
            )

        return new_object(
            temp_out=temp_out,
            aout=aout,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        set_val = []
        for a in device_value.ha_value.aout:
            set_val.append(a.brightness)
        return cls.create_command_payload(set_val)


class DT_148:
    INELS_TYPE = DAC3_04M
    HA_TYPE = LIGHT
    TYPE_ID = "148"

    DATA: DataDict = {
        TEMP_OUT: [0, 1],
        ALERT: [2],
        OUT: [4, 5, 6, 7],
    }

    @staticmethod
    def create_command_payload(cmd: List[int]) -> str:
        return Formatter.format_data([0, 0, 0, 0] + cmd)

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        temp_out = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_OUT, "")

        aout_alert = trim_inels_status_values(device_value.inels_status_value, cls.DATA, ALERT, "")
        aout_alert_bits = f"{int(aout_alert, 16):0>8b}"
        aout_coa = []
        for i in range(4):
            aout_coa.append(aout_alert_bits[6 - i] == "1")  # skip first bit

        aout_str = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, OUT)
        aout_val = []
        for d in aout_str:
            brightness = min(int(d, 16), 100)
            aout_val.append(brightness)

        aout = []
        for i in range(4):
            aout.append(
                AOUTLight(
                    brightness=aout_val[i],
                    aout_coa=aout_coa[i],
                )
            )

        return new_object(
            temp_out=temp_out,
            aout=aout,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        set_val = []
        for a in device_value.ha_value.aout:
            set_val.append(a.brightness)
        return cls.create_command_payload(set_val)


class DT_150:
    INELS_TYPE = DCDA_33M
    HA_TYPE = LIGHT
    TYPE_ID = "150"

    DATA: DataDict = {
        ALERT: [2],
        OUT: [4, 5, 6, 7],
    }

    @staticmethod
    def create_command_payload(cmd: List[int]) -> str:
        return Formatter.format_data([0, 0, 0, 0] + cmd)

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, ALERT, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        sw = []
        coa = []
        for i in range(3):
            sw.append(digital_inputs[7 - i] == "1")
            coa.append(digital_inputs[4 - i] == "1")

        coa.append(False)  # only 3 alerts, so I fake the last one

        aout_val = []
        aouts = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, OUT)
        for i in range(len(aouts)):
            brightness = int(aouts[i], 16)
            brightness = brightness if brightness < 100 else 100
            aout_val.append(brightness)

        aout = []
        for i in range(4):
            aout.append(
                AOUTLight(
                    brightness=aout_val[i],
                    aout_coa=coa[i],
                )
            )

        return new_object(
            sw=sw,
            aout=aout,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        set_val = []
        for i in range(4):
            set_val.append(device_value.ha_value.aout[i].brightness)
        return cls.create_command_payload(set_val)


class DT_151:
    INELS_TYPE = DA3_66M
    HA_TYPE = LIGHT
    TYPE_ID = "151"

    DATA: DataDict = {
        ALERT: [1, 2],
        SW: [3],
        OUT: [4, 5, 6, 7, 12, 13],
        DIN: [8],
        # MIN_BRIGHTNESS: list(range(14, 20, 2)),
        # CHAN_TYPE: list(range(15, 21, 2)),
    }

    @staticmethod
    def create_command_payload(cmd: List[int]) -> str:
        return Formatter.format_data([0] * 4 + cmd[:4] + [0] * 4 + cmd[4:] + [0] * 12)

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        state = trim_inels_status_values(device_value.inels_status_value, cls.DATA, ALERT, "")
        state = f"0x{state}"
        state = f"{int(state, 16):0>16b}"

        toa = []
        coa = []
        for i in range(4):
            toa.append(state[7 - 2 * i] == "1")
            coa.append(state[7 - 2 * i - 1] == "1")
        for i in range(2):
            toa.append(state[15 - 2 * i] == "1")
            coa.append(state[15 - 2 * i - 1] == "1")

        switches = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        switches = f"0x{switches}"
        switches = f"{int(switches, 16):0>8b}"

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"

        sw = []
        din = []
        for i in range(6):
            sw.append(switches[7 - i] == "1")
            din.append(digital_inputs[7 - i] == "1")

        out = []
        outs = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, OUT)

        for o in outs:
            out.append(int(o, 16))

        light_coa_toa = []
        for i in range(6):
            light_coa_toa.append(
                LightCoaToa(
                    brightness=out[i],
                    toa=toa[i],
                    coa=coa[i],
                )
            )

        return new_object(
            sw=sw,
            din=din,
            light_coa_toa=light_coa_toa,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        cmd: List[int] = []
        for i in range(6):
            brightness = min(device_value.ha_value.light_coa_toa[i].brightness, 100)
            cmd.append(brightness)

        return cls.create_command_payload(cmd)


class DT_153(Base):
    INELS_TYPE = DIMMER_RGBW
    HA_TYPE = LIGHT
    TYPE_ID = "153"

    DATA: DataDict = {
        "LED_1": [4, 5, 6, 7, 12],
        "LED_2": [13, 14, 15, 20, 21],
        "LED_3": [22, 23, 28, 29, 30],
        TEMP_IN: [8, 9],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        """Create a HA value object for a RGBW."""
        led_1 = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, "LED_1")
        led_2 = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, "LED_2")
        led_3 = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, "LED_3")

        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")

        rgbw = []
        for led in [led_1, led_2, led_3]:
            r, g, b, w, y = [int(i, 16) for i in led]
            rgbw.append(RGBWLight(r=r, g=g, b=b, w=w, brightness=y))

        return new_object(rgbw=rgbw, temp_in=temp_in)

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        """Generate command string to set the RGBW and brightness values."""
        led_1, led_2, led_3 = device_value.ha_value.rgbw
        command = [
            0,
            0,
            0,
            0,
            led_1.r,
            led_1.g,
            led_1.b,
            led_1.w,
            0,
            0,
            0,
            0,
            led_1.brightness,
            led_2.r,
            led_2.g,
            led_2.b,
            0,
            0,
            0,
            0,
            led_2.w,
            led_2.brightness,
            led_3.r,
            led_3.g,
            0,
            0,
            0,
            0,
            led_3.b,
            led_3.w,
            led_3.brightness,
            0,
        ]
        return Formatter.format_data(command)


class DT_156(Base):
    INELS_TYPE = ADC3_60M
    HA_TYPE = SENSOR
    TYPE_ID = "156"

    DATA: DataDict = {
        AIN: list(range(24)),
        ADC3_60M: [24],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        ains = []
        ain_bytes = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, AIN)
        for i in range(int(len(ain_bytes) / 4)):
            ains.append(ain_bytes[4 * i] + ain_bytes[4 * i + 1] + ain_bytes[4 * i + 2] + ain_bytes[4 * i + 3])

        return new_object(
            ains=ains,
        )


class DT_157(Base):
    INELS_TYPE = TI3_10B
    HA_TYPE = SENSOR
    TYPE_ID = "157"

    DATA: DataDict = {TEMP_IN: [0, 1]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        temps = []
        temp_bytes = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, TEMP_IN)

        for i in range(int(len(temp_bytes) / 2)):
            temps.append(temp_bytes[2 * i] + temp_bytes[2 * i + 1])

        return new_object(temps=temps)


class DT_158(DT_157):
    INELS_TYPE = TI3_40B
    HA_TYPE = SENSOR
    TYPE_ID = "158"

    DATA: DataDict = {TEMP_IN: list(range(8))}


class DT_159(DT_157):
    INELS_TYPE = TI3_60M
    HA_TYPE = SENSOR
    TYPE_ID = "159"

    DATA: DataDict = {TEMP_IN: list(range(12))}


class DT_160(Base):
    INELS_TYPE = IDRT3_1
    HA_TYPE = SENSOR
    TYPE_ID = "160"

    DATA: DataDict = {
        SW: [1],
        TEMP_IN: [2, 3],
        TEMP_OUT: [8, 9],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        inputs = f"0x{inputs}"
        inputs = f"{int(inputs, 16):0>8b}"

        interface = []
        din = []
        for i in range(2):
            din.append(inputs[7 - i] == "1")
            interface.append(inputs[5 - i] == "1")

        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")
        temp_out = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_OUT, "")

        return new_object(
            interface=interface,
            din=din,
            temp_in=temp_in,
            temp_out=temp_out,
        )


class DT_163(Base):
    class Command(IntEnum):
        OPEN = 0b111
        CLOSE = 0b110

    INELS_TYPE = JA3_018M
    HA_TYPE = COVER
    TYPE_ID = "163"

    DATA: DataDict = {
        SHUTTER: list(range(18)),
        SW: [18, 19],
        ALERT: [20],
        RELAY_OVERFLOW: [21],
    }

    SHUTTER_STATE_SET = {
        Shutter_state.Open: [Command.OPEN, Command.CLOSE],
        Shutter_state.Closed: [Command.CLOSE, Command.OPEN],
        Shutter_state.Stop_up: [Command.CLOSE, Command.CLOSE],
        Shutter_state.Stop_down: [Command.CLOSE, Command.CLOSE],
    }

    @staticmethod
    def create_command_payload(cmd: List[int]) -> str:
        return Formatter.format_data(cmd)

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        shutter_relays = []
        for r in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, SHUTTER):
            shutter_relays.append((int(r, 16) & 1) != 0)

        simple_shutters = []
        shutters = list(zip(shutter_relays[::2], shutter_relays[1::2], strict=True))
        for s in shutters:
            if s[0]:
                state = Shutter_state.Open
            elif s[1]:
                state = Shutter_state.Closed
            else:
                state = Shutter_state.Stop_down
            simple_shutters.append(Shutter(state=state, is_closed=None))

        interface = []
        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"

        for i in range(8):
            interface.append(digital_inputs[7 - i] == "1")
        for i in range(8):
            interface.append(digital_inputs[15 - i] == "1")

        alerts = trim_inels_status_values(device_value.inels_status_value, cls.DATA, ALERT, "")
        alerts = f"0x{alerts}"
        alerts = f"{int(alerts, 16):0>8b}"

        for i in range(2):
            interface.append(alerts[7 - i] == "1")

        alert_power = alerts[4] == "1"
        alert_comm = [alerts[3] == "1", alerts[2] == "1", alerts[1] == "1"]

        overflows = trim_inels_status_values(device_value.inels_status_value, cls.DATA, RELAY_OVERFLOW, "")
        overflows = f"0x{overflows}"
        overflows = f"{int(overflows, 16):0>8b}"

        # TODO add overflows and alerts to the shutters
        relay_overflow = []
        for i in range(8):
            relay_overflow.append(overflows[7 - i] == "1")

        relay_overflow.append(alerts[0] == "1")

        # I'll register them as an interface and replace the names to SW 1 up/down, etc...

        return new_object(
            simple_shutters=simple_shutters,
            interface=interface,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        cmd: List[int] = []
        for x in device_value.ha_value.simple_shutters:
            cmd.extend(cls.SHUTTER_STATE_SET[x.state])
        return cls.create_command_payload(cmd)


class DT_164(Base):
    INELS_TYPE = DALI_DMX_UNIT
    HA_TYPE = LIGHT
    TYPE_ID = "164"

    DATA: DataDict = {
        OUT: list(range(4, 8)),
    }

    @staticmethod
    def create_command_payload(cmd: List[int]) -> str:
        return Formatter.format_data([0, 0, 0, 0] + cmd)

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        outs = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, OUT)
        simple_light = []
        for o in outs:
            brightness = min(int(o, 16), 100)
            simple_light.append(
                SimpleLight(
                    brightness=brightness,
                )
            )

        return new_object(
            simple_light=simple_light,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        cmd: List[int] = []
        for i in range(4):
            out = device_value.ha_value.simple_light[i].brightness
            cmd.append(min(out, 100))
        return cls.create_command_payload(cmd)


class DT_165(Base):
    INELS_TYPE = DALI_DMX_UNIT_2
    HA_TYPE = LIGHT
    TYPE_ID = "165"

    DATA: DataDict = {
        OUT: list(range(4, 8)),
    }

    @staticmethod
    def create_command_payload(cmd: List[int]) -> str:
        return Formatter.format_data([0, 0, 0, 0] + cmd)

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        outs = trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, OUT)
        warm_light = []
        lights = list(zip(outs[::2], outs[1::2], strict=True))

        for i in lights:
            b = min(int(i[0], 16), 100)
            w = min(int(i[1], 16), 100)
            warm_light.append(
                WarmLight(
                    brightness=b,
                    relative_ct=w,
                )
            )

        return new_object(
            warm_light=warm_light,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        cmd: List[int] = []
        for i in range(2):
            out = min(device_value.ha_value.warm_light[i].brightness, 100)
            cmd.append(out)

            white = min(device_value.ha_value.warm_light[i].relative_ct, 100)
            cmd.append(white)

        return cls.create_command_payload(cmd)


class DT_166:
    INELS_TYPE = VIRT_CONTR
    HA_TYPE = CLIMATE
    TYPE_ID = "166"

    DATA: DataDict = {
        CURRENT_TEMP: [3, 2, 1, 0],
        CRITICAL_MAX_TEMP: [7, 6, 5, 4],
        REQUIRED_HEAT_TEMP: [11, 10, 9, 8],
        MAX_TEMP: [15, 14, 13, 12],
        CRITICAL_MIN_TEMP: [19, 18, 17, 16],
        REQUIRED_COOL_TEMP: [23, 22, 21, 20],
        TEMP_CORRECTION: [27, 26, 25, 24],
        PUBLIC_HOLIDAY: [28],
        CONTROL_MODE: [29],
        VIRT_CONTR: [30],
    }

    @staticmethod
    def create_command_payload(out1: int = 0, out2: int = 0) -> str:
        return Formatter.format_data([0, 0, 0, 0, out1, out2])

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        temp_current: float = int(
            trim_inels_status_values(device_value.inels_status_value, cls.DATA, CURRENT_TEMP, ""), 16
        )
        if temp_current == 0x7FFFFFFB:
            temp_current = 0
        else:
            temp_current /= 100

        temp_critical_max = (
            int(
                trim_inels_status_values(  # check if 0x7F FF FF FB -> make it 50
                    device_value.inels_status_value, cls.DATA, CRITICAL_MAX_TEMP, ""
                ),
                16,
            )
            / 100
        )
        temp_required_heat: float = int(
            trim_inels_status_values(device_value.inels_status_value, cls.DATA, REQUIRED_HEAT_TEMP, ""), 16
        )
        if temp_required_heat == 0x7FFFFFFB:
            temp_required_heat = 0
        else:
            temp_required_heat /= 100

        temp_critical_min = (
            int(
                trim_inels_status_values(  # check if 0x7F FF FF FB -> make it -50
                    device_value.inels_status_value, cls.DATA, CRITICAL_MIN_TEMP, ""
                ),
                16,
            )
            / 100
        )
        temp_required_cool: float = int(
            trim_inels_status_values(device_value.inels_status_value, cls.DATA, REQUIRED_COOL_TEMP, ""), 16
        )
        if temp_required_cool == 0x7FFFFFFB:
            temp_required_cool = 0
        else:
            temp_required_cool /= 100

        temp_correction = (
            int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_CORRECTION, ""), 16) / 100
        )
        holiday_mode = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, PUBLIC_HOLIDAY, ""), 16)
        control_mode = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, CONTROL_MODE, ""))
        # 0 -> user control [ONLY IMPLEMENT THIS ONE FOR NOW]
        #   Has presets (Schedule, Fav1-4 and manual temp)
        # 1 -> 2 temp
        # 2 -> single temp

        binary_vals = trim_inels_status_values(device_value.inels_status_value, cls.DATA, VIRT_CONTR, "")
        binary_vals = f"0x{binary_vals}"
        binary_vals = f"{int(binary_vals, 16):0>8b}"

        controller_on = binary_vals[7] == "1"  # if controller is on
        schedule_mode = binary_vals[6] == "1"  # schedule or a set temperature
        heating_enabled = binary_vals[5] == "1"  # if heating is connected
        cooling_enabled = binary_vals[4] == "1"  # if cooling is connected
        vacation = binary_vals[3] == "1"
        regulator_disabled = binary_vals[2] == "1"  # window detection is on (?)

        climate_mode = Climate_modes.Off
        if controller_on:  # TODO review all of this
            if control_mode == 0:  # user control
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
            if control_mode == 0:  # user control
                if climate_mode == Climate_modes.Heat and temp_current < temp_required_heat:
                    current_action = Climate_action.Heating
                elif climate_mode == Climate_modes.Cool and temp_current > temp_required_cool:
                    current_action = Climate_action.Cooling
            elif control_mode == 1:  # two temp
                if temp_current < temp_required_heat:
                    current_action = Climate_action.Heating
                elif temp_current > temp_required_cool:
                    current_action = Climate_action.Cooling
            elif control_mode == 2:  # one temp
                if temp_current < temp_required_heat:
                    current_action = Climate_action.Heating
                else:
                    current_action = Climate_action.Cooling

        # 1 -> schedule
        # 6 -> manual
        preset = 0 if schedule_mode else 5

        return new_object(
            climate_controller=new_object(
                current=temp_current,  # current_temperature
                required=temp_required_heat,  # target_temperature / target_temperature_high
                required_cool=temp_required_cool,  # target_temperature_low
                climate_mode=climate_mode,  # hvac_mode: Off/Heat_cool/Heat/Cool
                # Off -> controller is turned off
                # Heat_cool -> follow temp range
                # Heat -> only heating
                # Cool -> only cooling
                current_action=current_action,  # hvac_action: Off/Heating/Cooling/Idle
                # Off -> controller is off
                # Heating -> heating is on
                # Cooling -> cooling is on
                # Idle -> temp is in range
                # non exposed
                critical_temp=temp_critical_max,
                correction_temp=temp_correction,
                public_holiday=holiday_mode,
                vacation=vacation,
                control_mode=control_mode,
                current_preset=preset,
            ),
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        cc = device_value.ha_value.climate_controller

        current_temp = [int(x, 16) for x in break_into_bytes(f"{int(cc.current * 100):08X}")]
        current_temp.reverse()

        critical_temp = [int(x, 16) for x in break_into_bytes(f"{int(cc.critical_temp * 100):08X}")]
        critical_temp.reverse()

        manual_temp = [int(x, 16) for x in break_into_bytes(f"{int((cc.required + cc.correction_temp) * 100):08X}")]
        manual_temp.reverse()

        manual_cool_temp = [
            int(x, 16) for x in break_into_bytes(f"{int((cc.required_cool + cc.correction_temp) * 100):08X}")
        ]
        manual_cool_temp.reverse()

        plan_in = 0
        if cc.public_holiday > 0:
            plan_in = 128  # 0x80
        elif cc.vacation:
            plan_in = 64  # 0x40

        manual_in = 0
        if cc.current_preset == 5:  # manual mode (in HA, this is the 4th preset, includes a default)
            manual_in = 7
        else:
            manual_in = cc.current_preset

        byte18 = 0  # TODO review this
        if cc.climate_mode != Climate_modes.Off:
            if cc.climate_mode == Climate_modes.Cool:
                byte18 = 3
            else:
                byte18 = 1

        set_val = current_temp + critical_temp + manual_temp + manual_cool_temp
        set_val += [plan_in, manual_in, byte18]

        return Formatter.format_data(set_val)


class DT_167(Base):
    INELS_TYPE = VIRT_HEAT_REG
    HA_TYPE = CLIMATE
    TYPE_ID = "167"

    DATA: DataDict = {
        STATE: [0],
        VIRT_HEAT_REG: [1],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        state = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, STATE, ""), 16)

        reg = trim_inels_status_values(device_value.inels_status_value, cls.DATA, VIRT_HEAT_REG, "")
        reg = f"{int(reg, 16):0>8b}"

        heat_reg = reg[7] == "1"
        heat_source = reg[6] == "1"

        return new_object(heating_out=heat_reg)


class DT_168(Base):
    INELS_TYPE = VIRT_COOL_REG
    HA_TYPE = CLIMATE
    TYPE_ID = "168"

    DATA: DataDict = {
        STATE: [0],
        VIRT_HEAT_REG: [1],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        state = int(trim_inels_status_values(device_value.inels_status_value, cls.DATA, STATE, ""), 16)

        reg = trim_inels_status_values(device_value.inels_status_value, cls.DATA, VIRT_HEAT_REG, "")
        reg = f"{int(reg, 16):0>8b}"

        cool_reg = reg[7] == "1"
        cool_source = reg[6] == "1"

        return new_object(
            cooling_out=cool_reg,
        )


class DT_169(DT_100):
    INELS_TYPE = SA3_014M
    HA_TYPE = SWITCH
    TYPE_ID = "169"

    DATA: DataDict = {
        RELAY: list(range(14)),  # relays
        SW: [17, 18],  # switch inputs
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        simple_relay: list[SimpleRelay] = []
        for relay in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, RELAY):
            simple_relay.append(SimpleRelay(is_on=bool(int(relay, 16) & 1)))

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"

        sw = []
        for i in range(8):
            sw.append(digital_inputs[7 - i] == "1")
        for i in range(6):
            sw.append(digital_inputs[15 - i] == "1")

        return new_object(
            simple_relay=simple_relay,
            sw=sw,
        )


class DT_170(DT_163):
    INELS_TYPE = JA3_014M
    HA_TYPE = COVER
    TYPE_ID = "170"

    DATA: DataDict = {
        SHUTTER: list(range(14)),
        SW: [17, 18],
        ALERT: [16],
        RELAY_OVERFLOW: [14, 15],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        shutter_relays = []
        for r in trim_inels_status_bytes(device_value.inels_status_value, cls.DATA, SHUTTER):
            shutter_relays.append((int(r, 16) & 1) != 0)

        simple_shutters = []
        shutters = list(zip(shutter_relays[::2], shutter_relays[1::2], strict=True))

        for s in shutters:
            if s[0]:
                state = Shutter_state.Open
            elif s[1]:
                state = Shutter_state.Closed
            else:
                state = Shutter_state.Stop_down
            simple_shutters.append(Shutter(state=state, is_closed=None))

        interface = []
        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>16b}"

        for i in range(8):
            interface.append(digital_inputs[7 - i] == "1")
        for i in range(6):
            interface.append(digital_inputs[13 - i] == "1")

        alerts = trim_inels_status_values(device_value.inels_status_value, cls.DATA, ALERT, "")
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

        overflows = trim_inels_status_values(device_value.inels_status_value, cls.DATA, RELAY_OVERFLOW, "")
        overflows = f"0x{overflows}"
        overflows = f"{int(overflows, 16):0>16b}"

        # TODO add overflows and alerts to the shutters
        relay_overflow: list[bool] = []
        for i in range(8):
            interface.append(overflows[7 - i] == "1")
        for i in range(6):
            interface.append(overflows[13 - i] == "1")

        # relay_overflow.append(alerts[0] == "1")

        # I'll register them as an interface and replace the names to SW 1 up/down, etc...

        return new_object(
            simple_shutters=simple_shutters,
            interface=interface,
        )


class DT_171(Base):
    INELS_TYPE = MCD3_01
    HA_TYPE = SENSOR
    TYPE_ID = "171"

    DATA: DataDict = {STATE: [0]}

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        state = trim_inels_status_values(device_value.inels_status_value, cls.DATA, STATE, "")
        motion = int(state, 16) == 1

        return new_object(
            motion=motion,
        )


class DT_172(DT_171):
    INELS_TYPE = PMS3_01
    HA_TYPE = SENSOR
    TYPE_ID = "172"


class DT_174(DT_143):
    INELS_TYPE = GSB3_40SX_V2
    HA_TYPE = SENSOR
    TYPE_ID = "174"

    INTERFACE_BUTTON_COUNT = 4


class DT_175(DT_143):
    INELS_TYPE = GSB3_60SX_V2
    HA_TYPE = SENSOR
    TYPE_ID = "175"

    INTERFACE_BUTTON_COUNT = 6


class DT_176(DT_143):
    INELS_TYPE = GSB3_90SX_V2
    HA_TYPE = SENSOR
    TYPE_ID = "176"

    INTERFACE_BUTTON_COUNT = 9


class DT_177(DT_143):
    INELS_TYPE = MSB3_40
    HA_TYPE = SENSOR
    TYPE_ID = "177"


class DT_178(DT_143):
    INELS_TYPE = MSB3_60
    HA_TYPE = SENSOR
    TYPE_ID = "178"

    INTERFACE_BUTTON_COUNT = 6


class DT_179(DT_143):
    INELS_TYPE = MSB3_90
    HA_TYPE = SENSOR
    TYPE_ID = "179"

    INTERFACE_BUTTON_COUNT = 9


class DT_180(Base):
    INELS_TYPE = GRT3_70
    HA_TYPE = SENSOR
    TYPE_ID = "180"

    DATA: DataDict = {
        SW: [1],
        TEMP_IN: [2, 3],
        DIN: [7],
        LIGHT_IN: [8, 9, 10, 11],
        AIN: [12, 13],
        HUMIDITY: [14, 15],
        DEW_POINT: [16, 17],
    }

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        switches = trim_inels_status_values(device_value.inels_status_value, cls.DATA, SW, "")
        switches_hex_str = f"0x{switches}"
        switches_bin_str = f"{int(switches_hex_str, 16):0>8b}"

        temp_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, TEMP_IN, "")

        digital_inputs = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DIN, "")
        digital_inputs = f"0x{digital_inputs}"
        digital_inputs = f"{int(digital_inputs, 16):0>8b}"
        din = [digital_inputs[7] == "1"]
        prox = digital_inputs[6] == "1"

        light_in = trim_inels_status_values(device_value.inels_status_value, cls.DATA, LIGHT_IN, "")
        ain = trim_inels_status_values(device_value.inels_status_value, cls.DATA, AIN, "")
        humidity = trim_inels_status_values(device_value.inels_status_value, cls.DATA, HUMIDITY, "")
        dewpoint = trim_inels_status_values(device_value.inels_status_value, cls.DATA, DEW_POINT, "")

        return new_object(
            din=din,
            prox=prox,
            interface=[
                switches_bin_str[7] == "1",
                switches_bin_str[6] == "1",
                switches_bin_str[5] == "1",
                switches_bin_str[4] == "1",
                switches_bin_str[3] == "1",
                switches_bin_str[2] == "1",
                switches_bin_str[1] == "1",
            ],
            temp_in=temp_in,
            light_in=light_in,
            ain=ain,
            humidity=humidity,
            dewpoint=dewpoint,
            backlit=False,
        )


class DT_BITS:
    INELS_TYPE = BITS
    HA_TYPE = SWITCH
    TYPE_ID = "bits"

    @staticmethod
    def create_command_payload(cmd: Dict[str, int]) -> str:
        return json.dumps({"cmd": cmd})

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        bit: list[Bit] = []
        for addr, val in parse_formated_json(device_value.inels_status_value):
            bit.append(Bit(is_on=bool(val), addr=addr))

        return new_object(
            bit=bit,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        set_val = {}
        for bit in device_value.ha_value.bit:
            set_val[bit.addr] = int(bit.is_on)
        return cls.create_command_payload(set_val)


class DT_INTEGERS:
    INELS_TYPE = INTEGERS
    HA_TYPE = NUMBER
    TYPE_ID = "integers"

    @staticmethod
    def create_command_payload(cmd: Dict[str, int]) -> str:
        return json.dumps({"cmd": cmd})

    @classmethod
    def create_ha_value_object(cls, device_value: DeviceValue) -> Any:
        number: list[Number] = []
        for addr, val in parse_formated_json(device_value.inels_status_value):
            number.append(Number(value=val, addr=addr))

        return new_object(
            number=number,
        )

    @classmethod
    def create_inels_set_value(cls, device_value: DeviceValue) -> str:
        set_val = {}
        for number in device_value.ha_value.number:
            set_val[number.addr] = int(number.value)

        return cls.create_command_payload(set_val)
