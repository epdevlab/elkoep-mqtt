"""Unit test for Discovery class
    handling device discovering
"""

from unittest.mock import patch, Mock
from unittest import TestCase

from inelsmqtt.const import (
    MQTT_HOST,
    MQTT_PASSWORD,
    MQTT_PORT,
    MQTT_USERNAME,
    PROTO_5,
    MQTT_PROTOCOL,
)
from inelsmqtt.discovery import InelsDiscovery
from inelsmqtt import InelsMqtt

from tests.const import (
    TEST_HOST,
    TEST_INELS_MQTT_CLASS_NAMESPACE,
    TEST_INELS_MQTT_NAMESPACE,
    TEST_PASSWORD,
    TEST_PORT,
    TEST_SWITCH_TOPIC_STATE,
    TEST_USER_NAME,
)


class DiscoveryTest(TestCase):
    """Discovery class tests

    Args:
        TestCase (_type_): Base class of unit testing
    """

    def setUp(self) -> None:
        """Setup all patches and instances for Discovery testing"""
        # mocking mqtt broker client
        self.patches = [
            patch(f"{TEST_INELS_MQTT_NAMESPACE}.mqtt.Client", return_value=Mock()),
            patch(
                f"{TEST_INELS_MQTT_NAMESPACE}.mqtt.Client.username_pw_set",
                return_value=Mock(),
            ),
            patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.subscribe", return_value=Mock()),
            patch(f"{TEST_INELS_MQTT_NAMESPACE}._LOGGER", return_value=Mock()),
        ]

        for item in self.patches:
            item.start()

        config = {
            MQTT_HOST: TEST_HOST,
            MQTT_PORT: TEST_PORT,
            MQTT_USERNAME: TEST_USER_NAME,
            MQTT_PASSWORD: TEST_PASSWORD,
            MQTT_PROTOCOL: PROTO_5,
        }

        mqtt = InelsMqtt(config)

        self.i_dis = InelsDiscovery(mqtt)

    def tearDown(self) -> None:
        """Destroy all instances and stop patches"""
        patch.stopall()
        self.patches = None
        self.i_dis = None

    def test_init_discovery(self) -> None:
        """Initialize test instance of the InelsDiscovery"""
        self.assertIsInstance(self.i_dis, InelsDiscovery)
        self.assertIsInstance(self.i_dis.devices, list)
        self.assertEqual(len(self.i_dis.devices), 0)

    @patch(
        f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.discovery_all",
        return_value={TEST_SWITCH_TOPIC_STATE: "data"},
    )
    def test_discovery(self, mock_discovery_all) -> None:
        """Test get list of devices"""

        coordinators_with_devices = self.i_dis.discovery()

        devices = self.i_dis.devices

        self.assertGreater(len(devices), 0)
        self.assertGreater(len(self.i_dis.coordinators), 0)
        self.assertGreater(len(coordinators_with_devices), 0)

        mock_discovery_all.assert_called()
        mock_discovery_all.assert_called_once()
