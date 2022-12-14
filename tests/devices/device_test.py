"""Unit tests for Device class
    handling device operations
"""
from operator import itemgetter

from unittest.mock import Mock, patch
from unittest import TestCase
from inelsmqttnew import InelsMqtt
from inelsmqttnew.util import DeviceValue
from inelsmqttnew.devices import Device, DeviceInfo
from inelsmqttnew.const import (
    BATTERY,
    COVER,
    MANUFACTURER,
    RFATV_2,
    RFJA_12,
    STATE_CLOSED,
    STATE_OPEN,
    STOP_UP,
    SWITCH,
    TEMP_IN,
    TEMP_OUT,
    DEVICE_TYPE_DICT,
    FRAGMENT_DEVICE_TYPE,
    FRAGMENT_DOMAIN,
    FRAGMENT_SERIAL_NUMBER,
    FRAGMENT_UNIQUE_ID,
    SWITCH_OFF_SET,
    SWITCH_ON_SET,
    SWITCH_ON_STATE,
    SWITCH_OFF_STATE,
    TEMP_SENSOR_DATA,
    TOPIC_FRAGMENTS,
    MQTT_HOST,
    MQTT_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
    MQTT_PROTOCOL,
    PROTO_5,
    VERSION,
    CLIMATE,
    BUTTON,
    RFGB_40,
    RFSTI_11B,
)

from tests.const import (
    TEST_COVER_RFJA_12_INELS_STATE_CLOSED,
    TEST_COVER_RFJA_12_INELS_STATE_OPEN,
    TEST_COVER_RFJA_12_SET_CLOSE,
    TEST_COVER_RFJA_12_SET_OPEN,
    TEST_COVER_RFJA_12_SET_STOP_UP,
    TEST_COVER_RFJA_12_TOPIC_CONNECTED,
    TEST_COVER_RFJA_12_TOPIC_STATE,
    TEST_LIGH_STATE_HA_VALUE,
    TEST_LIGH_STATE_INELS_VALUE,
    TEST_LIGHT_DIMMABLE_TOPIC_STATE,
    TEST_LIGHT_SET_INELS_VALUE,
    TEST_CLIMATE_RFATV_2_OPEN_TO_40_STATE_VALUE,
    TEST_CLIMATE_RFATV_2_TOPIC_CONNECTED,
    TEST_CLIMATE_RFATV_2_TOPIC_STATE,
    TEST_SENSOR_TOPIC_STATE,
    TEST_AVAILABILITY_OFF,
    TEST_AVAILABILITY_ON,
    TEST_SWITCH_WITH_TEMP_STATE_OFF_VALUE,
    TEST_SWITCH_WITH_TEMP_STATE_ON_VALUE,
    TEST_SWITCH_WITH_TEMP_TOPIC_CONNECTED,
    TEST_SWITCH_WITH_TEMP_TOPIC_STATE,
    TEST_TEMPERATURE_DATA,
    TEST_SWITCH_TOPIC_CONNECTED,
    TEST_SWITCH_TOPIC_STATE,
    TEST_INELS_MQTT_NAMESPACE,
    TEST_INELS_MQTT_CLASS_NAMESPACE,
    TEST_HOST,
    TEST_PORT,
    TEST_USER_NAME,
    TEST_PASSWORD,
    TEST_BUTTON_RFGB_40_TOPIC_STATE,
    TEST_BUTTON_RFGB_40_TOPIC_CONNECTED,
    TEST_BUTTON_RFGB_40_STATE_VALUE,

    TEST_RELAY_SA3_01B_TOPIC_STATE,
    TEST_RELAY_SA3_01B_CONNECTED,
    TEST_RELAY_SA3_01B_STATE_VALUE,

    TEST_TWOCHANNELDIMMER_DA3_22M_TOPIC_STATE,
    TEST_TWOCHANNELDIMMER_DA3_22M_CONNECTED,
    TEST_TWOCHANNELDIMMER_DA3_22M_STATE_VALUE,

    TEST_THERMOSTAT_GTR3_50_TOPIC_STATE,
    TEST_THERMOSTAT_GTR3_50_CONNECTED,
    TEST_THERMOSTAT_GTR3_50_STATE_VALUE,

    TEST_BUTTONARRAY_GSB3_90X_TOPIC_STATE,
    TEST_BUTTONARRAY_GSB3_90X_CONNECTED,
    TEST_BUTTONARRAY_GSB3_90X_STATE_VALUE,
)


class DeviceTest(TestCase):
    """Device class tests

    Args:
        TestCase (_type_): Base class of unit testing
    """

    def setUp(self) -> None:
        """Setup all patches and instances for device testing"""
        self.patches = [
            patch(f"{TEST_INELS_MQTT_NAMESPACE}.mqtt.Client", return_value=Mock()),
            patch(
                f"{TEST_INELS_MQTT_NAMESPACE}.mqtt.Client.username_pw_set",
                return_value=Mock(),
            ),
            patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.subscribe", return_value=Mock()),
            patch(
                f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.is_subscribed", return_value=Mock()
            ),
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

        self.switch = Device(InelsMqtt(config), TEST_SWITCH_TOPIC_STATE, "Switch")
        self.sensor = Device(InelsMqtt(config), TEST_SENSOR_TOPIC_STATE, "Sensor")
        self.light = Device(InelsMqtt(config), TEST_LIGHT_DIMMABLE_TOPIC_STATE, "Light")
        self.shutter = Device(
            InelsMqtt(config), TEST_COVER_RFJA_12_TOPIC_STATE, "Shutter"
        )
        self.valve = Device(
            InelsMqtt(config), TEST_CLIMATE_RFATV_2_TOPIC_STATE, CLIMATE
        )
        self.button = Device(InelsMqtt(config), TEST_BUTTON_RFGB_40_TOPIC_STATE, BUTTON)
        self.relay = Device(
            InelsMqtt(config), TEST_RELAY_SA3_01B_TOPIC_STATE, "Relay")
        self.twochanneldimmer = Device(
            InelsMqtt(config), TEST_TWOCHANNELDIMMER_DA3_22M_TOPIC_STATE, "Two Channel Dimmer")
        self.thermostat = Device(
            InelsMqtt(config), TEST_THERMOSTAT_GTR3_50_TOPIC_STATE, "Thermostat")
        self.buttonarray = Device(
            InelsMqtt(config), TEST_BUTTONARRAY_GSB3_90X_TOPIC_STATE, "Button Array")

    def tearDown(self) -> None:
        """Destroy all instances and stop patches"""
        self.switch = None
        self.sensor = None
        self.light = None
        self.shutter = None
        self.valve = None
        self.button = None
        self.relay = None
        self.twochanneldimmer = None
        self.thermostat = None
        self.buttonarray = None

    def test_initialize_device(self) -> None:
        """Test initialization of device object"""
        title = "Device 1"

        # device without title
        dev_no_title = Device(Mock(), TEST_SWITCH_TOPIC_STATE)
        # device with title
        dev_with_title = Device(Mock(), TEST_SWITCH_TOPIC_STATE, title)

        self.assertIsNotNone(dev_no_title)
        self.assertIsNotNone(dev_with_title)

        self.assertIsInstance(dev_no_title, Device)
        self.assertIsInstance(dev_with_title, Device)

        self.assertEqual(dev_no_title.title, dev_no_title.unique_id)
        self.assertEqual(dev_with_title.title, title)

        fragments = TEST_SWITCH_TOPIC_STATE.split("/")

        set_topic = f"{fragments[TOPIC_FRAGMENTS[FRAGMENT_DOMAIN]]}/set/{fragments[TOPIC_FRAGMENTS[FRAGMENT_SERIAL_NUMBER]]}/{fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]}/{fragments[TOPIC_FRAGMENTS[FRAGMENT_UNIQUE_ID]]}"  # noqa: 501

        self.assertEqual(
            dev_no_title.unique_id, fragments[TOPIC_FRAGMENTS[FRAGMENT_UNIQUE_ID]]
        )
        self.assertEqual(
            dev_no_title.device_type,
            DEVICE_TYPE_DICT[fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]],
        )
        self.assertEqual(
            dev_no_title.parent_id, fragments[TOPIC_FRAGMENTS[FRAGMENT_SERIAL_NUMBER]]
        )

        self.assertEqual(dev_no_title.set_topic, set_topic)
        self.assertEqual(dev_with_title.set_topic, set_topic)

    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.publish")
    @patch("inelsmqtt.InelsMqtt.messages")
    def test_info_serialized(self) -> None:
        """Test of the serialized info."""
        self.assertIsInstance(self.switch.info_serialized(), str)

    def test_switch_info(self) -> None:
        """Test of the info."""
        info = self.switch.info()

        self.assertIsInstance(info, DeviceInfo)
        self.assertEqual(info.manufacturer, MANUFACTURER)
        self.assertEqual(info.model_number, self.switch.inels_type)
        self.assertEqual(info.sw_version, VERSION)

    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.messages")
    def test_is_available(self, mock_messages) -> None:
        """Test of the device availability."""

        mock_messages.return_value = {
            TEST_SWITCH_TOPIC_CONNECTED: TEST_AVAILABILITY_ON
        }
        is_available = self.switch.is_available

        self.assertTrue(is_available)

    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.messages")
    def test_is_not_available(self, mock_messages) -> None:
        """Test of the dvice availability wit result false."""

        mock_messages.return_value = {
            TEST_SWITCH_TOPIC_CONNECTED: TEST_AVAILABILITY_OFF
        }
        is_avilable = self.switch.is_available

        self.assertFalse(is_avilable)

    # PAYLOAD TEST (could've been any device, but this one is the simplest by far)
    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.messages")
    def test_temperature_parsing(self, mock_message) -> None:
        """Test parsing temperature data to relevant format."""
        mock_message.return_value = {TEST_SENSOR_TOPIC_STATE: TEST_TEMPERATURE_DATA}

        temp_in_decimal_result = 27.4
        temp_out_decimal_result = 26.7
        batter_decimal_result = 100

        # split by new line and remove last element because is empty
        data = self.sensor.state.split("\n")[:-1]

        self.assertEqual(len(data), 5)

        battery = itemgetter(*TEMP_SENSOR_DATA[BATTERY])(data)
        temp_in = itemgetter(*TEMP_SENSOR_DATA[TEMP_IN])(data)
        temp_out = itemgetter(*TEMP_SENSOR_DATA[TEMP_OUT])(data)

        self.assertEqual(battery, data[0])
        self.assertEqual("".join(temp_in), f"{data[2]}{data[1]}")
        self.assertEqual("".join(temp_out), f"{data[4]}{data[3]}")

        temp_in_joined = "".join(temp_in)
        temp_out_joined = "".join(temp_out)

        temp_in_hex = f"0x{temp_in_joined}"
        temp_out_hex = f"0x{temp_out_joined}"
        battery_hex = f"0x{battery}"

        temp_in_dec = int(temp_in_hex, 16) / 100
        temp_out_dec = int(temp_out_hex, 16) / 100
        battery_dec = 100 if int(battery_hex, 16) == 0 else 0

        self.assertEqual(temp_in_dec, temp_in_decimal_result)
        self.assertEqual(temp_out_dec, temp_out_decimal_result)
        self.assertEqual(battery_dec, batter_decimal_result)

    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.messages")
    def test_device_dimmable_light_test_values(self, mock_message) -> None:
        """Test if the light is on."""
        mock_message.return_value = {
            TEST_LIGHT_DIMMABLE_TOPIC_STATE: TEST_LIGH_STATE_INELS_VALUE
        }

        values = self.light.get_value()

        self.assertEqual(self.light.state, TEST_LIGH_STATE_HA_VALUE)
        self.assertEqual(values.ha_value, TEST_LIGH_STATE_HA_VALUE)
        self.assertEqual(
            values.inels_status_value, TEST_LIGH_STATE_INELS_VALUE.decode()
        )
        self.assertEqual(values.inels_set_value, TEST_LIGHT_SET_INELS_VALUE)

    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.publish")
    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.messages")
    def test_device_set_not_support_dimmable_light_value(
        self, mock_message, mock_publish
    ) -> None:
        """Test result ha and inels value when ha value is not supported in inels."""
        mock_message.return_value = {
            TEST_LIGHT_DIMMABLE_TOPIC_STATE: TEST_LIGH_STATE_INELS_VALUE
        }
        mock_publish.return_value = True

        self.light.set_ha_value(24)

        self.assertEqual(self.light.state, TEST_LIGH_STATE_HA_VALUE)

    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.messages")
    def test_device_support_cover_initialized(self, mock_message) -> None:
        """Test covers all props. initialization."""
        mock_message.return_value = {
            TEST_COVER_RFJA_12_TOPIC_STATE: TEST_COVER_RFJA_12_INELS_STATE_OPEN,
            TEST_COVER_RFJA_12_TOPIC_CONNECTED: TEST_AVAILABILITY_ON,
        }

        self.assertTrue(self.shutter.is_available)
        self.assertEqual(self.shutter.device_type, COVER)
        self.assertEqual(self.shutter.inels_type, RFJA_12)
        self.assertEqual(self.shutter.state, STATE_OPEN)

    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.publish")
    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.messages")
    def test_device_support_cover_open_stop_and_close(
        self, mock_message, mock_publish
    ) -> None:
        """Test open the shutter."""
        mock_message.return_value = {
            TEST_COVER_RFJA_12_TOPIC_STATE: TEST_COVER_RFJA_12_INELS_STATE_CLOSED,
        }
        mock_publish.return_value = True

        self.assertNotEqual(self.shutter.state, STATE_OPEN)
        self.assertEqual(self.shutter.state, STATE_CLOSED)

        values: DeviceValue = self.shutter.get_value()

        self.assertIsInstance(values, DeviceValue)
        self.assertEqual(
            values.inels_status_value, TEST_COVER_RFJA_12_INELS_STATE_CLOSED.decode()
        )
        self.assertEqual(values.inels_set_value, TEST_COVER_RFJA_12_SET_CLOSE)

        self.shutter.set_ha_value(STATE_OPEN)

        mock_message.return_value = {
            TEST_COVER_RFJA_12_TOPIC_STATE: TEST_COVER_RFJA_12_INELS_STATE_OPEN,
        }

        values: DeviceValue = self.shutter.get_value()

        self.assertIsInstance(values, DeviceValue)
        self.assertEqual(
            values.inels_status_value, TEST_COVER_RFJA_12_INELS_STATE_OPEN.decode()
        )
        self.assertEqual(values.inels_set_value, TEST_COVER_RFJA_12_SET_OPEN)
        self.assertEqual(self.shutter.state, STATE_OPEN)
        self.assertNotEqual(self.shutter.state, STATE_CLOSED)

        self.shutter.set_ha_value(STOP_UP)
        self.assertEqual(
            self.shutter.values.inels_set_value, TEST_COVER_RFJA_12_SET_STOP_UP
        )
        self.assertEqual(
            self.shutter.values.inels_status_value,
            TEST_COVER_RFJA_12_INELS_STATE_OPEN.decode(),
        )
        self.assertEqual(self.shutter.state, STATE_OPEN)

    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.messages")
    def test_device_support_climate_initialized(self, mock_message) -> None:
        """Test climate all props. initialization."""
        mock_message.return_value = {
            TEST_CLIMATE_RFATV_2_TOPIC_STATE: TEST_CLIMATE_RFATV_2_OPEN_TO_40_STATE_VALUE,
            TEST_CLIMATE_RFATV_2_TOPIC_CONNECTED: TEST_AVAILABILITY_ON,
        }

        self.valve.get_value()

        self.assertTrue(self.valve.is_available)
        self.assertEqual(self.valve.device_type, CLIMATE)
        self.assertEqual(self.valve.inels_type, RFATV_2)
        self.assertEqual(self.valve.state.current, 26.0)
        self.assertEqual(self.valve.state.required, 32.0)
        self.assertEqual(self.valve.state.open_in_percentage, 40.0)

    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.publish")
    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.messages")
    def test_device_set_climate_valve_value(self, mock_message, mock_publish) -> None:
        """Test valve value."""
        mock_message.return_value = {
            TEST_CLIMATE_RFATV_2_TOPIC_STATE: TEST_CLIMATE_RFATV_2_OPEN_TO_40_STATE_VALUE
        }
        mock_publish.return_value = True

        state = self.valve.state
        state.required = 30.0

        self.valve.set_ha_value(state)

        self.assertEqual(self.valve.values.inels_set_value, "00 3C 00")

    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.messages")
    def test_device_support_button_initialized(self, mock_message) -> None:
        """Test button all props. initialization."""
        mock_message.return_value = {
            TEST_BUTTON_RFGB_40_TOPIC_STATE: TEST_BUTTON_RFGB_40_STATE_VALUE,
            TEST_BUTTON_RFGB_40_TOPIC_CONNECTED: TEST_AVAILABILITY_ON,
        }

        self.button.get_value()

        self.assertTrue(self.button.is_available)
        self.assertEqual(self.button.device_type, BUTTON)
        self.assertEqual(self.button.inels_type, RFGB_40)
        self.assertTrue(self.button.state)

    @patch(f"{TEST_INELS_MQTT_CLASS_NAMESPACE}.messages")
    def test_device_switch_with_temp(self, mock_message) -> None:
        """Test switch with temperature."""
        mock_message.return_value = {
            TEST_SWITCH_WITH_TEMP_TOPIC_CONNECTED: TEST_AVAILABILITY_ON,
            TEST_SWITCH_WITH_TEMP_TOPIC_STATE: TEST_SWITCH_WITH_TEMP_STATE_ON_VALUE,
        }

        self.switch_with_temp.get_value()

        self.assertTrue(self.switch_with_temp.is_available)
        self.assertEqual(self.switch_with_temp.device_type, SWITCH)
        self.assertEqual(self.switch_with_temp.inels_type, RFSTI_11B)
        self.assertTrue(self.switch_with_temp.state.on)
        self.assertIsNotNone(self.switch_with_temp.state.temperature)
        self.assertEqual(self.switch_with_temp.state.temperature, 24.5)

        mock_message.return_value = {
            TEST_SWITCH_WITH_TEMP_TOPIC_CONNECTED: TEST_AVAILABILITY_ON,
            TEST_SWITCH_WITH_TEMP_TOPIC_STATE: TEST_SWITCH_WITH_TEMP_STATE_OFF_VALUE,
        }

        self.switch_with_temp.get_value()

        self.assertFalse(self.switch_with_temp.state.on)
        self.assertEqual(self.switch_with_temp.state.temperature, 21.0)
