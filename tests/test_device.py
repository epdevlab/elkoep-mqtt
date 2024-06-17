import pytest
from unittest.mock import MagicMock
from inelsmqtt.devices import Device, DeviceInfo
from inelsmqtt import InelsMqtt
from inelsmqtt.utils.common import SimpleRelay, new_object

from inelsmqtt.const import (
    MANUFACTURER,
    VERSION,
)

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

    mqtt_mock.subscribe.assert_any_call(device.state_topic)
    mqtt_mock.subscribe.assert_any_call(device.connected_topic, 0, None, None)


def test_device_availability(device):
    # Simulate an update to the device value
    device.update_value(b"02\n01\n")

    # Simulate different gateway and device statuses
    device.mqtt.messages.return_value.get.side_effect = [
        b"{\"status\": true}",
        "on\n",
        b"{\"status\": true}",
        "off\n",
        b"{\"status\": false}",
        "on\n",
        b"{\"status\": false}",
        "off\n"
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
    simple_relay = new_object(
        simple_relay=[SimpleRelay(is_on=True)]
    )
    device.set_ha_value(simple_relay)
    device.mqtt.publish.assert_called_once_with('inels/set/10e97f8b7d30/02/02E8', '01\n00\n00\n')
                                                

def test_info_serialized(device):
    info = device.info_serialized()
    assert info == '{"name": "Test Device", "device_type": "switch", "id": "10e97f8b7d30_02E8", "via_device": "10e97f8b7d30_02E8"}'


def test_device_callbacks(device):
    callback = MagicMock()
    device.add_ha_callback("simple_relay", 0, callback)

    last_val = new_object(
        simple_relay=[SimpleRelay(is_on=False)]
    )

    curr_val = new_object(
        simple_relay=[SimpleRelay(is_on=True)]
    )

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