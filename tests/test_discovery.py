from unittest.mock import MagicMock

import pytest

from inelsmqtt import InelsMqtt
from inelsmqtt.devices import Device
from inelsmqtt.discovery import InelsDiscovery


@pytest.fixture
def mqtt_mock():
    """Fixture to mock InelsMqtt class."""
    mock = MagicMock(spec=InelsMqtt)
    return mock


@pytest.fixture
def discovery(mqtt_mock):
    """Fixture to create an InelsDiscovery instance with a mocked mqtt."""
    return InelsDiscovery(mqtt=mqtt_mock)


def test_discovery_successful(mqtt_mock, discovery):
    """Test successful discovery of devices."""
    mqtt_mock.discovery_all.return_value = {"10e97f8b7d30/01/01E8": "data", "10e97f8b7d30/03/03E8": "data"}
    expected_devices = [
        Device(mqtt_mock, "inels/status/10e97f8b7d30/01/01E8"),
        Device(mqtt_mock, "inels/status/10e97f8b7d30/03/03E8"),
    ]

    discovered_devices = discovery.discovery()
    assert len(discovered_devices) == len(expected_devices)
    assert all(d.state_topic == e.state_topic for d, e in zip(discovered_devices, expected_devices, strict=True))
    mqtt_mock.discovery_all.assert_called_once()


def test_discovery_with_retry(mqtt_mock, discovery):
    """Test discovery with retry logic when initial discovery fails."""
    mqtt_mock.discovery_all.side_effect = [
        {"10e97f8b7d30/01/01E8": None},  # First call returns None, triggers retry
        {"10e97f8b7d30/03/03E8": "data"},  # Second call successful
    ]

    discovered_devices = discovery.discovery()
    assert len(discovered_devices) == 1
    assert mqtt_mock.discovery_all.call_count == 2


def test_discovery_with_assumed_state_devices(mqtt_mock, discovery):
    """Test discovery where devices are assumed to be in a certain state."""
    mqtt_mock.discovery_all.return_value = {
        "10e97f8b7d30/01/01E8": None,  # disregard
        "10e97f8b7d30/03/03E8": None,  # disregard
        "10e97f8b7d30/18/18E8": None,  # Device is in assumed state list
    }

    discovered_devices = discovery.discovery()
    assert len(discovered_devices) == 1


def test_discovery_no_devices_found(mqtt_mock, discovery):
    """Test discovery with no devices found."""
    mqtt_mock.discovery_all.return_value = {}
    assert discovery.discovery() == []
    assert len(discovery.devices) == 0
