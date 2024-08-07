from unittest.mock import MagicMock

import pytest

from inelsmqtt import InelsMqtt
from inelsmqtt.const import (
    MANUFACTURER,
    VERSION,
)
from inelsmqtt.devices import Device, DeviceInfo
from inelsmqtt.utils.common import SimpleRelay, WarmLight, new_object
from inelsmqtt.utils.core import DUMMY_VAL

TEST_STATE_TOPIC = "inels/status/10e97f8b7d30/02/02E8"


@pytest.fixture
def mqtt_mock():
    mqtt = MagicMock(spec=InelsMqtt)
    mqtt.last_value.return_value = b"02\n00\n"
    return mqtt


@pytest.fixture
def device(mqtt_mock):
    return Device(mqtt=mqtt_mock, state_topic=TEST_STATE_TOPIC, title="Test Device")


def test_device_initialization(device, mqtt_mock):
    assert device.unique_id == "10e97f8b7d30_02E8"
    assert device.device_class == "02"
    assert device.device_type == "switch"
    assert device.inels_type == "Switching unit"
    assert device.parent_id == "10e97f8b7d30_02E8"
    assert device.title == "Test Device"
    assert device.domain == "inels"
    assert device.connected_topic == "inels/connected/10e97f8b7d30/02/02E8"
    assert device.gw_connected_topic == "inels/connected/10e97f8b7d30/gw"
    assert device.state_topic == "inels/status/10e97f8b7d30/02/02E8"
    assert device.set_topic == "inels/set/10e97f8b7d30/02/02E8"
    assert device.is_available == False
    assert device.mqtt == mqtt_mock


def test_device_availability(device):
    # Simulate an update to the device value
    device.update_value(b"02\n01\n")

    # Simulate different gateway and device statuses
    device.mqtt.messages.return_value.get.side_effect = [
        b'{"status": true}',
        "on\n",
        b'{"status": true}',
        "off\n",
        b'{"status": false}',
        "on\n",
        b'{"status": false}',
        "off\n",
    ]

    # Gateway on, device on
    assert device.is_available
    # Gateway on, device off
    assert not device.is_available
    # Gateway off, device on
    assert not device.is_available
    # Gateway off, device off
    assert not device.is_available


def test_device_last_values(device, mqtt_mock):
    last_values = device.last_values

    assert last_values is not None
    assert not last_values.ha_value.simple_relay[0].is_on


def test_update_value(device):
    device.update_value(b"02\n01\n")
    assert device.state.simple_relay[0].is_on

    device.update_value(b"02\n00\n")
    assert not device.state.simple_relay[0].is_on


def test_device_set_ha_value(device):
    simple_relay = new_object(simple_relay=[SimpleRelay(is_on=True)])
    device.set_ha_value(simple_relay)
    device.mqtt.publish.assert_called_once_with("inels/set/10e97f8b7d30/02/02E8", "01\n00\n00\n")


def test_info_serialized(device):
    info = device.info_serialized()
    assert (
        info
        == '{"name": "Test Device", "device_type": "switch", "id": "10e97f8b7d30_02E8", "via_device": "10e97f8b7d30_02E8"}'
    )


def test_device_callbacks(device):
    callback = MagicMock()
    device.add_ha_callback("simple_relay", 0, callback)

    last_val = new_object(simple_relay=[SimpleRelay(is_on=False)])

    curr_val = new_object(simple_relay=[SimpleRelay(is_on=True)])

    device.ha_diff(last_val, curr_val)
    callback.assert_called_once()

    device.complete_callback()
    assert callback.call_count == 2


def test_device_callback_availability(device):
    device.mqtt.messages.return_value.get.side_effect = [b"02\n01\n", b"02\n01\n"]

    callback = MagicMock()
    device.add_ha_callback("simple_relay", 0, callback)

    device.callback(availability_update=True)
    assert callback.call_count == 1

    device.callback(availability_update=False)
    assert callback.call_count == 2


def test_device_info(device):
    info = device.info()
    assert isinstance(info, DeviceInfo)
    assert info.manufacturer == MANUFACTURER
    assert info.sw_version == VERSION
    assert info.model_number == device.inels_type
    assert info.serial_number == device.unique_id


def test_ha_diff_list(device):
    callback_warm_light = MagicMock()

    device.add_ha_callback("warm_light", 0, callback_warm_light)

    last_val = new_object(warm_light=[WarmLight(brightness=50, relative_ct=3000)])

    curr_val = new_object(warm_light=[WarmLight(brightness=75, relative_ct=3500)])

    device.ha_diff(last_val, curr_val)
    callback_warm_light.assert_called_once()

    # Test no change scenario
    callback_warm_light.reset_mock()

    device.ha_diff(curr_val, curr_val)
    callback_warm_light.assert_not_called()

    # Test partial change scenario
    new_val = new_object(warm_light=[WarmLight(brightness=75, relative_ct=4000)])

    device.ha_diff(curr_val, new_val)
    callback_warm_light.assert_called_once()


def test_ha_diff_plain(device):
    callback_low_battery = MagicMock()
    callback_temp_in = MagicMock()
    callback_temp_out = MagicMock()

    device.add_ha_callback("low_battery", -1, callback_low_battery)
    device.add_ha_callback("temp_in", -1, callback_temp_in)
    device.add_ha_callback("temp_out", -1, callback_temp_out)

    last_val = new_object(
        low_battery=False,
        temp_in=2000,
        temp_out=1800,
    )

    curr_val = new_object(
        low_battery=True,
        temp_in=2250,
        temp_out=2000,
    )

    device.ha_diff(last_val, curr_val)
    callback_low_battery.assert_called_once()
    callback_temp_in.assert_called_once()
    callback_temp_out.assert_called_once()

    # Test no change scenario
    callback_low_battery.reset_mock()
    callback_temp_in.reset_mock()
    callback_temp_out.reset_mock()

    device.ha_diff(curr_val, curr_val)
    callback_low_battery.assert_not_called()
    callback_temp_in.assert_not_called()
    callback_temp_out.assert_not_called()

    # Test partial change scenario
    new_val = new_object(
        low_battery=True,
        temp_in=2300,
        temp_out=2000,
    )

    device.ha_diff(curr_val, new_val)
    callback_low_battery.assert_not_called()
    callback_temp_in.assert_called_once()
    callback_temp_out.assert_not_called()


def test_ha_diff_dummy_val(device):
    callback_low_battery = MagicMock()
    callback_temp_in = MagicMock()
    callback_temp_out = MagicMock()

    device.add_ha_callback("low_battery", -1, callback_low_battery)
    device.add_ha_callback("temp_in", -1, callback_temp_in)
    device.add_ha_callback("temp_out", -1, callback_temp_out)

    curr_val = new_object(
        low_battery=True,
        temp_in=2250,
        temp_out=2000,
    )

    # Test when last_val is DUMMY_VAL
    device.ha_diff(DUMMY_VAL, curr_val)
    callback_low_battery.assert_not_called()
    callback_temp_in.assert_not_called()
    callback_temp_out.assert_not_called()

    # Test when curr_val is DUMMY_VAL
    device.ha_diff(curr_val, DUMMY_VAL)
    callback_low_battery.assert_not_called()
    callback_temp_in.assert_not_called()
    callback_temp_out.assert_not_called()

    # Test when both values are DUMMY_VAL
    device.ha_diff(DUMMY_VAL, DUMMY_VAL)
    callback_low_battery.assert_not_called()
    callback_temp_in.assert_not_called()
    callback_temp_out.assert_not_called()
