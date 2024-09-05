import pytest

from inelsmqtt.const import Shutter_state
from inelsmqtt.utils.common import (
    LightCoaToa,
    Relay,
    RGBLight,
    Shutter,
    Shutter_pos,
    SimpleLight,
    SimpleRelay,
    WarmLight,
)
from inelsmqtt.utils.core import DeviceValue, ProtocolHandlerMapper


class BaseDeviceTestClass:
    DEVICE_TYPE_ID = None  # To be defined in subclasses

    def create_device_value(self, inels_value=None, ha_value=None, last_value=None):
        if self.DEVICE_TYPE_ID is None:
            raise ValueError("DEVICE_TYPE_ID must be defined in the subclass.")

        cls = ProtocolHandlerMapper.get_handler(self.DEVICE_TYPE_ID)
        return DeviceValue(
            device_type=cls.HA_TYPE,
            inels_type=cls.INELS_TYPE,
            device_class=cls,
            inels_value=inels_value,
            ha_value=ha_value,
            last_value=last_value,
        )


class Test_RF_DEVICE_TYPE_01(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "01"

    @pytest.fixture
    def device_value_on(self):
        """Fixture to provide a device value with the relay ON."""
        return self.create_device_value(inels_value="02\n01\n")

    @pytest.fixture
    def device_value_off(self):
        """Fixture to provide a device value with the relay OFF."""
        return self.create_device_value(inels_value="02\n00\n")

    def test_create_ha_value_object(self, device_value_on):
        """Test creation of HA value object."""
        assert isinstance(device_value_on.ha_value.simple_relay[0], SimpleRelay)

    def test_create_ha_value_object_on(self, device_value_on):
        """Test HA value object creation with relay ON."""
        assert device_value_on.ha_value.simple_relay[0].is_on == True

    def test_create_ha_value_object_off(self, device_value_off):
        """Test HA value object creation with relay OFF."""
        assert device_value_off.ha_value.simple_relay[0].is_on == False

    def test_format_inels_set_value_on(self, device_value_on):
        """Test command string format for turning the relay ON."""
        assert device_value_on.inels_set_value == "01\n00\n"

    def test_format_inels_set_value_off(self, device_value_off):
        """Test command string format for turning the relay OFF."""
        assert device_value_off.inels_set_value == "02\n00\n"

    def test_creating_device_without_inels_value(self):
        device_value = self.create_device_value()

        # If the device does not have an inels_value set, then comm_test must be set
        assert device_value.inels_set_value == "08\n00\n"

        # If inels_value is not set, then the ha_value object cannot exist
        assert device_value.ha_value is None


class Test_RF_DEVICE_TYPE_02(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "02"

    @pytest.fixture
    def device_value_on(self):
        """Fixture to provide a device value with the relay ON."""
        return self.create_device_value(inels_value="02\n01\n")

    @pytest.fixture
    def device_value_off(self):
        """Fixture to provide a device value with the relay OFF."""
        return self.create_device_value(inels_value="02\n00\n")

    def test_create_ha_value_object(self, device_value_on):
        """Test creation of HA value object."""
        assert isinstance(device_value_on.ha_value.simple_relay[0], SimpleRelay)

    def test_create_ha_value_object_on(self, device_value_on):
        """Test HA value object creation with relay ON."""
        assert device_value_on.ha_value.simple_relay[0].is_on == True

    def test_create_ha_value_object_off(self, device_value_off):
        """Test HA value object creation with relay OFF."""
        assert device_value_off.ha_value.simple_relay[0].is_on == False

    def test_format_inels_set_value_on(self, device_value_on):
        """Test command string format for turning the relay ON."""
        assert device_value_on.inels_set_value == "01\n00\n00\n"

    def test_format_inels_set_value_off(self, device_value_off):
        """Test command string format for turning the relay OFF."""
        assert device_value_off.inels_set_value == "02\n00\n00\n"

    def test_creating_device_without_inels_value(self):
        device_value = self.create_device_value()

        # If the device does not have an inels_value set, then comm_test must be set
        assert device_value.inels_set_value == "08\n00\n00\n"

        # If inels_value is not set, then the ha_value object cannot exist
        assert device_value.ha_value is None


class Test_RF_DEVICE_TYPE_03(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "03"

    @pytest.fixture
    def device_value_open(self):
        return self.create_device_value(inels_value="03\n00\n")

    @pytest.fixture
    def device_value_closed(self):
        return self.create_device_value(inels_value="03\n01\n")

    def test_create_ha_value_object_open(self, device_value_open):
        assert isinstance(device_value_open.ha_value.shutters[0], Shutter)
        assert not device_value_open.ha_value.shutters[0].is_closed

    def test_create_ha_value_object_closed(self, device_value_closed):
        assert isinstance(device_value_closed.ha_value.shutters[0], Shutter)
        assert device_value_closed.ha_value.shutters[0].is_closed

    def test_format_inels_set_value_open(self, device_value_closed):
        device_value_closed.ha_value.shutters[0].state = Shutter_state.Open
        device_value = self.create_device_value(
            ha_value=device_value_closed.ha_value,
        )
        assert device_value.inels_set_value == "01\n00\n00\n"

    def test_format_inels_set_value_closed(self, device_value_open):
        device_value_open.ha_value.shutters[0].state = Shutter_state.Closed
        device_value = self.create_device_value(
            ha_value=device_value_open.ha_value,
        )
        assert device_value.inels_set_value == "02\n00\n00\n"

    def test_format_inels_set_value_stop_up(self, device_value_closed):
        device_value_closed.ha_value.shutters[0].state = Shutter_state.Stop_up
        device_value = self.create_device_value(
            ha_value=device_value_closed.ha_value,
        )
        assert device_value.inels_set_value == "04\n00\n00\n"

    def test_format_inels_set_value_stop_down(self, device_value_open):
        device_value_open.ha_value.shutters[0].state = Shutter_state.Stop_down
        device_value = self.create_device_value(
            ha_value=device_value_open.ha_value,
        )
        assert device_value.inels_set_value == "06\n00\n00\n"

    def test_comm_test(self):
        device_value = self.create_device_value()
        assert device_value.inels_set_value == "09\n00\n00\n"
        assert device_value.ha_value is None


class Test_RF_DEVICE_TYPE_04(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "04"

    @pytest.fixture
    def device_value_low_brightness(self):
        """Fixture to provide a device value with lowest brightness."""
        return self.create_device_value(inels_value="D8\nEF\n")

    @pytest.fixture
    def device_value_high_brightness(self):
        """Fixture to provide a device value with highest brightness."""
        return self.create_device_value(inels_value="8A\nCF\n")

    def test_create_ha_value_object(self, device_value_low_brightness):
        """Test creation of HA value object."""
        assert isinstance(device_value_low_brightness.ha_value.simple_light[0], SimpleLight)

    def test_create_ha_value_object_low_brightness(self, device_value_low_brightness):
        """Test HA value object creation with low brightness."""
        assert device_value_low_brightness.ha_value.simple_light[0].brightness == 0

    def test_create_ha_value_object_high_brightness(self, device_value_high_brightness):
        """Test HA value object creation with high brightness."""
        assert device_value_high_brightness.ha_value.simple_light[0].brightness == 100

    def test_format_inels_set_value_low_brightness(self, device_value_low_brightness):
        """Test command string format for setting low brightness."""
        device_value = self.create_device_value(
            ha_value=device_value_low_brightness.ha_value,
        )
        assert device_value.inels_set_value == "01\nD8\nEF\n"

    def test_format_inels_set_value_high_brightness(self, device_value_high_brightness):
        """Test command string format for setting high brightness."""
        device_value = self.create_device_value(
            ha_value=device_value_high_brightness.ha_value,
        )
        assert device_value.inels_set_value == "01\n8A\nCF\n"

    def test_creating_device_without_inels_value(self):
        device_value = self.create_device_value()

        # If the device does not have an inels_value set, then comm_test must be set
        assert device_value.inels_set_value == "07\n00\n00\n"

        # If inels_value is not set, then the ha_value object cannot exist
        assert device_value.ha_value is None


class Test_RF_DEVICE_TYPE_05(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "05"

    @pytest.fixture
    def device_value_low_brightness(self):
        """Fixture to provide a device value with lowest brightness."""
        return self.create_device_value(inels_value="D8\nEF\n")

    @pytest.fixture
    def device_value_high_brightness(self):
        """Fixture to provide a device value with highest brightness."""
        return self.create_device_value(inels_value="8A\nCF\n")

    def test_create_ha_value_object(self, device_value_low_brightness):
        """Test creation of HA value object."""
        assert isinstance(device_value_low_brightness.ha_value.simple_light[0], SimpleLight)

    def test_create_ha_value_object_low_brightness(self, device_value_low_brightness):
        """Test HA value object creation with low brightness."""
        assert device_value_low_brightness.ha_value.simple_light[0].brightness == 0

    def test_create_ha_value_object_high_brightness(self, device_value_high_brightness):
        """Test HA value object creation with high brightness."""
        assert device_value_high_brightness.ha_value.simple_light[0].brightness == 100

    def test_format_inels_set_value_low_brightness(self, device_value_low_brightness):
        """Test command string format for setting low brightness."""
        device_value = self.create_device_value(
            ha_value=device_value_low_brightness.ha_value,
        )
        assert device_value.inels_set_value == "01\nD8\nEF\n"

    def test_format_inels_set_value_high_brightness(self, device_value_high_brightness):
        """Test command string format for setting high brightness."""
        device_value = self.create_device_value(
            ha_value=device_value_high_brightness.ha_value,
        )
        assert device_value.inels_set_value == "01\n8A\nCF\n"

    def test_creating_device_without_inels_value(self):
        device_value = self.create_device_value()

        # If the device does not have an inels_value set, then comm_test must be set
        assert device_value.inels_set_value == "07\n00\n00\n"

        # If inels_value is not set, then the ha_value object cannot exist
        assert device_value.ha_value is None


class Test_RF_DEVICE_TYPE_06(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "06"

    @pytest.fixture
    def device_value_rgba_all_min(self):
        """Fixture for creating a device value with RGB settings."""
        device_value = self.create_device_value(inels_value="01\n00\n00\n00\n00\n00\n")
        return device_value

    @pytest.fixture
    def device_value_rgba_all_max(self):
        """Fixture for creating a device value with RGB settings."""
        device_value = self.create_device_value(inels_value="01\nFF\nFF\nFF\nFF\n00\n")
        return device_value

    def test_create_ha_value_object(self, device_value_rgba_all_max):
        """Test HA value object creation for RGB light."""
        assert isinstance(device_value_rgba_all_max.ha_value.rgb[0], RGBLight)

    def test_create_ha_value_object_rgba_all_min(self, device_value_rgba_all_min):
        assert device_value_rgba_all_min.ha_value.rgb[0].r == 0
        assert device_value_rgba_all_min.ha_value.rgb[0].g == 0
        assert device_value_rgba_all_min.ha_value.rgb[0].b == 0
        assert device_value_rgba_all_min.ha_value.rgb[0].brightness == 0

    def test_create_ha_value_object_rgba_all_max(self, device_value_rgba_all_max):
        assert device_value_rgba_all_max.ha_value.rgb[0].r == 255
        assert device_value_rgba_all_max.ha_value.rgb[0].g == 255
        assert device_value_rgba_all_max.ha_value.rgb[0].b == 255
        assert device_value_rgba_all_max.ha_value.rgb[0].brightness == 100

    def test_format_inels_set_value_rgba_all_min(self, device_value_rgba_all_min):
        """Test command string format for setting low brightness."""
        device_value = self.create_device_value(
            ha_value=device_value_rgba_all_min.ha_value,
        )
        assert device_value.inels_set_value == "01\n00\n00\n00\n00\n00\n"

    def test_format_inels_set_value_rgba_all_max(self, device_value_rgba_all_max):
        """Test command string format for setting low brightness."""
        device_value = self.create_device_value(
            ha_value=device_value_rgba_all_max.ha_value,
        )
        # TODO: fix with rounding it should be "01\nFF\nFF\nFF\nFF\n00\n"
        assert device_value.inels_set_value == "01\nFF\nFF\nFF\nFE\n00\n"

    def test_comm_test(self):
        device_value = self.create_device_value()
        assert device_value.inels_set_value == "07\n00\n00\n00\n00\n00\n"
        assert device_value.ha_value is None


class Test_RF_DEVICE_TYPE_07(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "07"

    @pytest.fixture
    def device_value_on(self):
        """Fixture to provide a device value with the relay ON."""
        return self.create_device_value(inels_value="07\n01\n92\n09\n")

    @pytest.fixture
    def device_value_off(self):
        """Fixture to provide a device value with the relay OFF."""
        return self.create_device_value(inels_value="07\n00\n92\n09\n")

    def test_create_ha_value_object(self, device_value_on):
        """Test creation of HA value object."""
        assert isinstance(device_value_on.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_on.ha_value.temp_out == "0992"

    def test_create_ha_value_object_on(self, device_value_on):
        """Test HA value object creation with relay ON."""
        assert device_value_on.ha_value.simple_relay[0].is_on == True

    def test_create_ha_value_object_off(self, device_value_off):
        """Test HA value object creation with relay OFF."""
        assert device_value_off.ha_value.simple_relay[0].is_on == False

    def test_format_inels_set_value_on(self, device_value_on):
        """Test command string format for turning the relay ON."""
        assert device_value_on.inels_set_value == "01\n00\n"

    def test_format_inels_set_value_off(self, device_value_off):
        """Test command string format for turning the relay OFF."""
        assert device_value_off.inels_set_value == "02\n00\n"

    def test_creating_device_without_inels_value(self):
        device_value = self.create_device_value()

        # If the device does not have an inels_value set, then comm_test must be set
        assert device_value.inels_set_value == "08\n00\n"

        # If inels_value is not set, then the ha_value object cannot exist
        assert device_value.ha_value is None


class Test_RF_DEVICE_TYPE_09(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "09"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="64\n3C\n08\n40\n00\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.low_battery == True
        assert device_value.ha_value.thermovalve.current == 30
        assert device_value.ha_value.thermovalve.required == 32
        assert device_value.ha_value.thermovalve.climate_mode == 1
        assert device_value.ha_value.thermovalve.open_in_percentage == 50

    def test_format_inels_set_value(self, device_value):
        device_value.ha_value.thermovalve.required = 25
        device_value = self.create_device_value(
            ha_value=device_value.ha_value,
        )
        assert device_value.inels_set_value == "00\n32\n00\n"

    def test_comm_test(self):
        device_value = self.create_device_value()
        assert device_value.inels_set_value == ""
        assert device_value.ha_value is None


class Test_RF_DEVICE_TYPE_10(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "10"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="00\nEC\n09\n46\n0A\n")

    def test_create_ha_value_object(self, device_value):
        # TODO: add two complement and remove value calc from HA side
        assert device_value.ha_value.low_battery == False
        assert device_value.ha_value.temp_in == "09EC"
        assert device_value.ha_value.temp_out == "0A46"


class Test_RF_DEVICE_TYPE_12(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "12"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="30\n00\n81\n00\n00\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.low_battery == True
        assert device_value.ha_value.temp_in == 24.0


class Test_RF_DEVICE_TYPE_13(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "13"

    @pytest.fixture
    def device_value_lowest_brightness_highest_white(self):
        return self.create_device_value(inels_value="07\n00\n00\n00\n00\nFF\n")

    @pytest.fixture
    def device_value_highest_brightness_lowest_white(self):
        return self.create_device_value(inels_value="07\n00\n00\n00\nFF\n00\n")

    @pytest.fixture
    def device_value_all_min(self):
        return self.create_device_value(inels_value="07\n00\n00\n00\n00\n00\n")

    def test_create_ha_value_object_lowest_brightness_highest_white(self, device_value_lowest_brightness_highest_white):
        assert isinstance(device_value_lowest_brightness_highest_white.ha_value.warm_light[0], WarmLight)
        assert device_value_lowest_brightness_highest_white.ha_value.warm_light[0].brightness == 0
        assert device_value_lowest_brightness_highest_white.ha_value.warm_light[0].relative_ct == 100

    def test_create_ha_value_object_highest_brightness_lowest_white(self, device_value_highest_brightness_lowest_white):
        assert isinstance(device_value_highest_brightness_lowest_white.ha_value.warm_light[0], WarmLight)
        assert device_value_highest_brightness_lowest_white.ha_value.warm_light[0].brightness == 100
        assert device_value_highest_brightness_lowest_white.ha_value.warm_light[0].relative_ct == 0

    def test_create_ha_value_object_all_min(self, device_value_all_min):
        assert isinstance(device_value_all_min.ha_value.warm_light[0], WarmLight)
        assert device_value_all_min.ha_value.warm_light[0].brightness == 0
        assert device_value_all_min.ha_value.warm_light[0].relative_ct == 0

    def test_format_inels_set_value_lowest_brightness(self, device_value_lowest_brightness_highest_white):
        device_value = self.create_device_value(
            ha_value=device_value_lowest_brightness_highest_white.ha_value,
        )
        assert device_value.inels_set_value == "0F\n00\n00\n00\n00\nFF\n"

    def test_format_inels_set_value_lowest_white(self, device_value_highest_brightness_lowest_white):
        device_value = self.create_device_value(
            ha_value=device_value_highest_brightness_lowest_white.ha_value,
        )
        assert device_value.inels_set_value == "0F\n00\n00\n00\nFF\n00\n"

    def test_creating_device_without_inels_value(self):
        device_value = self.create_device_value()

        # If the device does not have an inels_value set, then comm_test must be set
        assert device_value.inels_set_value == "07\n00\n00\n00\n00\n00\n"

        # If inels_value is not set, then the ha_value object cannot exist
        assert device_value.ha_value is None


class Test_RF_DEVICE_TYPE_15(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "15"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="81\nFF\n00\n00\n00\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.low_battery == True
        assert device_value.ha_value.flooded == True
        assert device_value.ha_value.ains[0] == 2.55


class Test_RF_DEVICE_TYPE_16(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "16"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="79\n01\n62\nCC\nA1\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.low_battery == True
        assert device_value.ha_value.detected == True
        assert device_value.ha_value.tamper == True


class Test_RF_DEVICE_TYPE_17(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "17"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="7A\n01\n62\nCC\nA1")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.low_battery == True
        assert device_value.ha_value.motion == True
        assert device_value.ha_value.tamper == True


class Test_RF_DEVICE_TYPE_18(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "18"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="1C\n02\n73\n59\nC8\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.low_battery == True
        assert device_value.ha_value.btn == [False, True]


class Test_RF_DEVICE_TYPE_19(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "19"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="1C\n02\n32\nA7\n5A\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.low_battery == True
        assert device_value.ha_value.btn == [False, True, False, False]


class Test_RF_DEVICE_TYPE_21(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "21"

    @pytest.fixture
    def device_value_open(self):
        return self.create_device_value(inels_value="03\n00\n00\n")

    @pytest.fixture
    def device_value_closed(self):
        return self.create_device_value(inels_value="03\n02\n64\n")

    def test_create_ha_value_object_open(self, device_value_open):
        assert isinstance(device_value_open.ha_value.shutters_with_pos[0], Shutter_pos)
        assert not device_value_open.ha_value.shutters_with_pos[0].is_closed
        assert not device_value_open.ha_value.shutters_with_pos[0].set_pos
        assert device_value_open.ha_value.shutters_with_pos[0].position == 100
        assert device_value_open.ha_value.shutters_with_pos[0].state == 0

    def test_create_ha_value_object_closed(self, device_value_closed):
        assert isinstance(device_value_closed.ha_value.shutters_with_pos[0], Shutter_pos)
        assert not device_value_closed.ha_value.shutters_with_pos[0].set_pos
        assert device_value_closed.ha_value.shutters_with_pos[0].is_closed
        assert device_value_closed.ha_value.shutters_with_pos[0].position == 0
        assert device_value_closed.ha_value.shutters_with_pos[0].state == 1

    def test_create_ha_value_object_last_value(self, device_value_open):
        device_value = self.create_device_value(inels_value="03\n01\n64\n", last_value=device_value_open.ha_value)
        assert device_value.ha_value.shutters_with_pos[0].state == 0

    def test_format_inels_set_value_open(self, device_value_closed):
        device_value_closed.ha_value.shutters_with_pos[0].state = Shutter_state.Open
        device_value = self.create_device_value(
            ha_value=device_value_closed.ha_value,
        )
        assert device_value.inels_set_value == "01\n00\n00\n"

    def test_format_inels_set_value_closed(self, device_value_open):
        device_value_open.ha_value.shutters_with_pos[0].state = Shutter_state.Closed
        device_value = self.create_device_value(
            ha_value=device_value_open.ha_value,
        )
        assert device_value.inels_set_value == "02\n00\n00\n"

    def test_format_inels_set_value_stop_up(self, device_value_closed):
        device_value_closed.ha_value.shutters_with_pos[0].state = Shutter_state.Stop_up
        device_value = self.create_device_value(
            ha_value=device_value_closed.ha_value,
        )
        assert device_value.inels_set_value == "04\n00\n00\n"

    def test_format_inels_set_value_stop_down(self, device_value_open):
        device_value_open.ha_value.shutters_with_pos[0].state = Shutter_state.Stop_down
        device_value = self.create_device_value(
            ha_value=device_value_open.ha_value,
        )
        assert device_value.inels_set_value == "06\n00\n00\n"

    def test_format_inels_set_value_open_to_70_percent(self, device_value_closed):
        device_value_closed.ha_value.shutters_with_pos[0].set_pos = True
        device_value_closed.ha_value.shutters_with_pos[0].position = 30
        device_value_closed = self.create_device_value(
            ha_value=device_value_closed.ha_value,
        )
        assert device_value_closed.inels_set_value == "0A\n00\n46\n"

    def test_comm_test(self):
        device_value = self.create_device_value()
        assert device_value.inels_set_value == "09\n00\n00\n"
        assert device_value.ha_value is None


class Test_RF_DEVICE_TYPE_30(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "30"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="01\nD8\n09\n24\n00")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.low_battery
        assert device_value.ha_value.temp_in == "09D8"
        assert device_value.ha_value.humidity == 36


class Test_CU_DEVICE_TYPE_100(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "100"

    @pytest.fixture
    def device_value_on(self):
        return self.create_device_value(inels_value="07\n00\n0A\n28\n01\n")

    @pytest.fixture
    def device_value_off(self):
        return self.create_device_value(inels_value="06\n00\n0A\n28\n00\n")

    def test_create_ha_value_object_on(self, device_value_on):
        assert isinstance(device_value_on.ha_value.relay[0], Relay)
        assert device_value_on.ha_value.relay[0].is_on
        assert device_value_on.ha_value.relay[0].overflow

    def test_create_ha_value_object_off(self, device_value_off):
        assert isinstance(device_value_off.ha_value.relay[0], Relay)
        assert not device_value_off.ha_value.relay[0].is_on
        assert not device_value_off.ha_value.relay[0].overflow

    def test_format_inels_set_value_on(self, device_value_off):
        device_value_off.ha_value.relay[0].is_on = True
        device_value = self.create_device_value(
            ha_value=device_value_off.ha_value,
        )
        assert device_value.inels_set_value == "07\n"

    def test_format_inels_set_value_off(self, device_value_on):
        device_value_on.ha_value.relay[0].is_on = False
        device_value = self.create_device_value(
            ha_value=device_value_on.ha_value,
        )
        assert device_value.inels_set_value == "06\n"


class Test_CU_DEVICE_TYPE_101(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "101"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="7F\nFF\nFF\n03\n64\n64\n00\n1D\n00\n00")

    def test_create_ha_value_object(self, device_value):
        assert isinstance(device_value.ha_value.light_coa_toa[0], LightCoaToa)
        assert device_value.ha_value.temp_in == "7FFF"
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.sw == [True, True]
        for i in device_value.ha_value.light_coa_toa:
            assert i.brightness == 100
            assert i.toa == True
            assert i.coa == True

    def test_format_inels_set_value_all_max(self, device_value):
        for i in device_value.ha_value.light_coa_toa:
            i.brightness = 100

        device_value = self.create_device_value(
            ha_value=device_value.ha_value,
        )
        assert device_value.inels_set_value == "00\n00\n00\n00\n64\n64\n"

    def test_format_inels_set_value_all_min(self, device_value):
        for i in device_value.ha_value.light_coa_toa:
            i.brightness = 0

        device_value = self.create_device_value(
            ha_value=device_value.ha_value,
        )
        assert device_value.inels_set_value == "00\n00\n00\n00\n00\n00\n"


class Test_CU_DEVICE_TYPE_102(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "102"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(
            inels_value="00\n00\n0A\n1D\n00\n00\n00\n00\n00\n00\n04\n37\n7F\nFF\n16\n60\n06\n7B\n"
        )

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.din == [False, False]
        assert device_value.ha_value.interface == [False, False, False, False, False, False, False]
        assert device_value.ha_value.temp_in == "0A1D"
        assert device_value.ha_value.light_in == "00000437"
        assert device_value.ha_value.ain == "7FFF"
        assert device_value.ha_value.humidity == "1660"
        assert device_value.ha_value.dewpoint == "067B"
        assert device_value.ha_value.backlit == False


class Test_CU_DEVICE_TYPE_103(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "103"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="FF\n0F\n0A\n28\n00\n00\n00\n0F\n0A\n28\n16\n60\n06\n7B\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.interface == [True] * 9
        assert device_value.ha_value.temp_in == "0A28"
        assert device_value.ha_value.light_in == "0000000F"
        assert device_value.ha_value.ain == "0A28"
        assert device_value.ha_value.prox == True
        assert device_value.ha_value.humidity == "1660"
        assert device_value.ha_value.dewpoint == "067B"
        assert device_value.ha_value.backlit == False
        assert device_value.ha_value.disabled == False


class Test_CU_DEVICE_TYPE_104(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "104"

    @pytest.fixture
    def device_value_all_on(self):
        return self.create_device_value(inels_value="07\n07\n0A\n28\n03\n")

    @pytest.fixture
    def device_value_all_off(self):
        return self.create_device_value(inels_value="06\n06\n0A\n28\n03\n")

    def test_create_ha_value_object_all_on(self, device_value_all_on):
        assert isinstance(device_value_all_on.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_on.ha_value.temp_in == "0A28"
        for r in device_value_all_on.ha_value.simple_relay:
            assert r.is_on

    def test_create_ha_value_object_all_off(self, device_value_all_off):
        assert isinstance(device_value_all_off.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_off.ha_value.temp_in == "0A28"
        for r in device_value_all_off.ha_value.simple_relay:
            assert not r.is_on

    def test_format_inels_set_value_all_on(self, device_value_all_off):
        for r in device_value_all_off.ha_value.simple_relay:
            r.is_on = True

        device_value = self.create_device_value(
            ha_value=device_value_all_off.ha_value,
        )
        assert device_value.inels_set_value == "07\n07\n"

    def test_format_inels_set_value_all_off(self, device_value_all_on):
        for r in device_value_all_on.ha_value.simple_relay:
            r.is_on = False

        device_value = self.create_device_value(
            ha_value=device_value_all_on.ha_value,
        )
        assert device_value.inels_set_value == "06\n06\n"


class Test_CU_DEVICE_TYPE_105(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "105"

    @pytest.fixture
    def device_value_all_on(self):
        return self.create_device_value(inels_value="07\n07\n03\n00\n")

    @pytest.fixture
    def device_value_all_off(self):
        return self.create_device_value(inels_value="06\n06\n00\n00\n")

    def test_create_ha_value_object_all_on(self, device_value_all_on):
        assert isinstance(device_value_all_on.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_on.ha_value.sw == [True, True]
        for r in device_value_all_on.ha_value.simple_relay:
            assert r.is_on

    def test_create_ha_value_object_all_off(self, device_value_all_off):
        assert isinstance(device_value_all_off.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_off.ha_value.sw == [False, False]
        for r in device_value_all_off.ha_value.simple_relay:
            assert not r.is_on

    def test_format_inels_set_value_all_on(self, device_value_all_off):
        for r in device_value_all_off.ha_value.simple_relay:
            r.is_on = True

        device_value = self.create_device_value(
            ha_value=device_value_all_off.ha_value,
        )
        assert device_value.inels_set_value == "07\n07\n"

    def test_format_inels_set_value_all_off(self, device_value_all_on):
        for r in device_value_all_on.ha_value.simple_relay:
            r.is_on = False

        device_value = self.create_device_value(
            ha_value=device_value_all_on.ha_value,
        )
        assert device_value.inels_set_value == "06\n06\n"


class Test_CU_DEVICE_TYPE_106(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "106"

    @pytest.fixture
    def device_value_all_on(self):
        return self.create_device_value(inels_value="07\n07\n07\n07\n0F\n00\n")

    @pytest.fixture
    def device_value_all_off(self):
        return self.create_device_value(inels_value="06\n06\n06\n06\n00\n00\n")

    def test_create_ha_value_object_all_on(self, device_value_all_on):
        assert isinstance(device_value_all_on.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_on.ha_value.sw == [True, True, True, True]
        for r in device_value_all_on.ha_value.simple_relay:
            assert r.is_on

    def test_create_ha_value_object_all_off(self, device_value_all_off):
        assert isinstance(device_value_all_off.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_off.ha_value.sw == [False, False, False, False]
        for r in device_value_all_off.ha_value.simple_relay:
            assert not r.is_on

    def test_format_inels_set_value_all_on(self, device_value_all_off):
        for r in device_value_all_off.ha_value.simple_relay:
            r.is_on = True

        device_value = self.create_device_value(ha_value=device_value_all_off.ha_value)
        assert device_value.inels_set_value == "07\n07\n07\n07\n"

    def test_format_inels_set_value_all_off(self, device_value_all_on):
        for r in device_value_all_on.ha_value.simple_relay:
            r.is_on = False

        device_value = self.create_device_value(
            ha_value=device_value_all_on.ha_value,
        )
        assert device_value.inels_set_value == "06\n06\n06\n06\n"


class Test_CU_DEVICE_TYPE_107(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "107"

    @pytest.fixture
    def device_value_all_on(self):
        return self.create_device_value(inels_value="07\n07\n07\n07\n07\n07\n3F\n00\n")

    @pytest.fixture
    def device_value_all_off(self):
        return self.create_device_value(inels_value="06\n06\n06\n06\n06\n06\n00\n00\n")

    def test_create_ha_value_object_all_on(self, device_value_all_on):
        assert isinstance(device_value_all_on.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_on.ha_value.sw == [True, True, True, True, True, True]
        for r in device_value_all_on.ha_value.simple_relay:
            assert r.is_on

    def test_create_ha_value_object_all_off(self, device_value_all_off):
        assert isinstance(device_value_all_off.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_off.ha_value.sw == [False, False, False, False, False, False]
        for r in device_value_all_off.ha_value.simple_relay:
            assert not r.is_on

    def test_format_inels_set_value_all_on(self, device_value_all_off):
        for r in device_value_all_off.ha_value.simple_relay:
            r.is_on = True

        device_value = self.create_device_value(ha_value=device_value_all_off.ha_value)
        assert device_value.inels_set_value == "07\n07\n07\n07\n07\n07\n"

    def test_format_inels_set_value_all_off(self, device_value_all_on):
        for r in device_value_all_on.ha_value.simple_relay:
            r.is_on = False

        device_value = self.create_device_value(
            ha_value=device_value_all_on.ha_value,
        )
        assert device_value.inels_set_value == "06\n06\n06\n06\n06\n06\n"


class Test_CU_DEVICE_TYPE_108(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "108"

    @pytest.fixture
    def device_value_all_on(self):
        return self.create_device_value(inels_value="07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\nFF\n0F\n00\n00\n")

    @pytest.fixture
    def device_value_all_off(self):
        return self.create_device_value(inels_value="06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n00\n00\n00\n00\n")

    def test_create_ha_value_object_all_on(self, device_value_all_on):
        assert isinstance(device_value_all_on.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_on.ha_value.sw == [True] * 12
        for r in device_value_all_on.ha_value.simple_relay:
            assert r.is_on

    def test_create_ha_value_object_all_off(self, device_value_all_off):
        assert isinstance(device_value_all_off.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_off.ha_value.sw == [False] * 12
        for r in device_value_all_off.ha_value.simple_relay:
            assert not r.is_on

    def test_format_inels_set_value_all_on(self, device_value_all_off):
        for r in device_value_all_off.ha_value.simple_relay:
            r.is_on = True

        device_value = self.create_device_value(ha_value=device_value_all_off.ha_value)
        assert device_value.inels_set_value == "07\n" * 12

    def test_format_inels_set_value_all_off(self, device_value_all_on):
        for r in device_value_all_on.ha_value.simple_relay:
            r.is_on = False

        device_value = self.create_device_value(
            ha_value=device_value_all_on.ha_value,
        )
        assert device_value.inels_set_value == "06\n" * 12


class Test_CU_DEVICE_TYPE_109(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "109"

    @pytest.fixture
    def device_value_all_on(self):
        return self.create_device_value(
            inels_value="07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\nFF\nFF\nFF\nFF\nFF\nFF\nFF\n"
        )

    @pytest.fixture
    def device_value_all_off(self):
        return self.create_device_value(
            inels_value="06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n00\n00\n00\n00\n00\n00\n00\n"
        )

    def test_create_ha_value_object_all_on(self, device_value_all_on):
        assert isinstance(device_value_all_on.ha_value.relay[0], Relay)
        assert isinstance(device_value_all_on.ha_value.simple_shutters[0], Shutter)

        for r in device_value_all_on.ha_value.relay:
            assert r.is_on
            assert r.overflow

        for s in device_value_all_on.ha_value.simple_shutters:
            assert s.state == Shutter_state.Open

        assert device_value_all_on.ha_value.shutter_motors == [True, True]
        assert device_value_all_on.ha_value.sw == [True] * 16
        assert device_value_all_on.ha_value.valve == [True, True, True, True]

    def test_create_ha_value_object_all_off(self, device_value_all_off):
        assert isinstance(device_value_all_off.ha_value.relay[0], Relay)
        assert isinstance(device_value_all_off.ha_value.simple_shutters[0], Shutter)

        for r in device_value_all_off.ha_value.relay:
            assert not r.is_on
            assert not r.overflow

        for s in device_value_all_off.ha_value.simple_shutters:
            assert s.state == Shutter_state.Stop_down

        assert device_value_all_off.ha_value.shutter_motors == [False, False]
        assert device_value_all_off.ha_value.sw == [False] * 16
        assert device_value_all_off.ha_value.valve == [False, False, False, False]

    def test_format_inels_set_value_all_open(self, device_value_all_off):
        for r in device_value_all_off.ha_value.relay:
            r.is_on = True

        for s in device_value_all_off.ha_value.simple_shutters:
            s.state = Shutter_state.Open

        device_value_all_off.ha_value.valve = [True, True, True, True]

        device_value = self.create_device_value(
            ha_value=device_value_all_off.ha_value,
        )
        assert (
            device_value.inels_set_value
            == "07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n06\n07\n07\n07\n07\n"
        )

    def test_format_inels_set_value_all_closed(self, device_value_all_on):
        for r in device_value_all_on.ha_value.relay:
            r.is_on = False

        for s in device_value_all_on.ha_value.simple_shutters:
            s.state = Shutter_state.Closed

        device_value_all_on.ha_value.valve = [False, False, False, False]

        device_value = self.create_device_value(
            ha_value=device_value_all_on.ha_value,
        )
        assert (
            device_value.inels_set_value
            == "06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n07\n06\n06\n06\n06\n"
        )


class Test_CU_DEVICE_TYPE_111(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "111"

    @pytest.fixture
    def device_value_all_off(self):
        return self.create_device_value(
            inels_value="00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"
        )

    @pytest.fixture
    def device_value_all_on(self):
        return self.create_device_value(
            inels_value="FF\nFF\nFF\nFF\n64\n64\n64\n64\n07\n07\n07\n07\n07\n07\n07\n07\n00\n00\nFF\nFF\n00\n00\nFF\nFF\n00\n00\nFF\nFF\n"
        )

    def test_create_ha_value_object_all_off(self, device_value_all_off):
        assert device_value_all_off.ha_value.ains == ["00000000", "00000000", "00000000"]

        for aout in device_value_all_off.ha_value.aout:
            assert aout.brightness == 0
            assert aout.aout_coa == False

        assert device_value_all_off.ha_value.din == [False, False, False]
        assert device_value_all_off.ha_value.fan_speed == 0
        assert device_value_all_off.ha_value.heating_out == False
        assert device_value_all_off.ha_value.sw == [False, False, False, False, False, False, False, False, False]
        assert device_value_all_off.ha_value.valves == [[False, False], [False, False]]

    def test_create_ha_value_object_all_on(self, device_value_all_on):
        assert device_value_all_on.ha_value.ains == ["0000FFFF", "0000FFFF", "0000FFFF"]

        for aout in device_value_all_on.ha_value.aout:
            assert aout.brightness == 100
            assert aout.aout_coa == True

        assert device_value_all_on.ha_value.din == [True, True, True]
        assert device_value_all_on.ha_value.fan_speed == 3
        assert device_value_all_on.ha_value.heating_out == True
        assert device_value_all_on.ha_value.sw == [True, True, True, True, True, True, True, True, True]
        assert device_value_all_on.ha_value.valves == [[True, True], [True, True]]

    def test_format_inels_set_value(self, device_value_all_off):
        device_value_all_off.ha_value.fan_speed = 3
        device_value_all_off.ha_value.aout[0].brightness = 100
        device_value = self.create_device_value(
            ha_value=device_value_all_off.ha_value,
        )

        assert device_value.inels_set_value == "00\n00\n00\n00\n64\n00\n00\n00\n00\n00\n00\n00\n06\n06\n07\n00\n"


class Test_CU_DEVICE_TYPE_112(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "112"

    @pytest.fixture
    def device_value_all_on(self):
        return self.create_device_value(
            inels_value="07\n07\n07\n07\n07\n07\n07\n07\n7F\nFF\nFF\nFF\n7F\nFF\nFF\nFF\n00\n00\n00\n00\n00\n00\n00\n00\nFF\nFF\nFF\n"
        )

    @pytest.fixture
    def device_value_all_off(self):
        return self.create_device_value(
            inels_value="06\n06\n06\n06\n06\n06\n06\n06\n7F\nFF\nFF\nFF\n7F\nFF\nFF\nFF\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"
        )

    def test_create_ha_value_object_all_on(self, device_value_all_on):
        assert isinstance(device_value_all_on.ha_value.relay[0], Relay)
        assert device_value_all_on.ha_value.din == [True] * 8
        assert device_value_all_on.ha_value.temps == ["7FFFFFFF", "7FFFFFFF"]
        for r in device_value_all_on.ha_value.relay:
            assert r.is_on
            assert r.overflow

    def test_create_ha_value_object_all_off(self, device_value_all_off):
        assert isinstance(device_value_all_off.ha_value.relay[0], Relay)
        assert device_value_all_off.ha_value.din == [False] * 8
        assert device_value_all_off.ha_value.temps == ["7FFFFFFF", "7FFFFFFF"]
        for r in device_value_all_off.ha_value.relay:
            assert not r.is_on
            assert not r.overflow

    def test_format_inels_set_value_all_on(self, device_value_all_off):
        for r in device_value_all_off.ha_value.relay:
            r.is_on = True

        device_value = self.create_device_value(
            ha_value=device_value_all_off.ha_value,
        )
        assert device_value.inels_set_value == "07\n07\n07\n07\n07\n07\n07\n07\n"

    def test_format_inels_set_value_all_off(self, device_value_all_on):
        for r in device_value_all_on.ha_value.relay:
            r.is_on = False

        device_value = self.create_device_value(
            ha_value=device_value_all_on.ha_value,
        )
        assert device_value.inels_set_value == "06\n06\n06\n06\n06\n06\n06\n06\n"


class Test_CU_DEVICE_TYPE_114(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "114"

    @pytest.fixture
    def device_value_all_min(self):
        return self.create_device_value(
            inels_value="00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"
        )

    @pytest.fixture
    def device_value_all_max(self):
        return self.create_device_value(
            inels_value="00\n00\n0A\n28\n64\n64\n00\n00\n07\n07\n07\n07\n07\n07\n07\n07\n00\n00\n0A\n28\n64\n64\n64\n64\n3F\nFF\nFF\n00\n64\n64\n64\n64\n00\n00\n00\n00\n64\n64\n64\n64\n00\n00\n00\n00\n64\n64\n64\n64\n"
        )

    def test_create_ha_value_object_all_min(self, device_value_all_min):
        assert device_value_all_min.ha_value.temps == ["0000", "0000"]
        assert device_value_all_min.ha_value.din == [False, False, False, False, False, False]

        for r in device_value_all_min.ha_value.relay:
            assert not r.is_on
            assert not r.overflow

        for a in device_value_all_min.ha_value.aout:
            assert not a.brightness
            assert not a.aout_coa

        for b in device_value_all_min.ha_value.dali:
            assert not b.brightness
            assert not b.alert_dali_communication
            assert not b.alert_dali_power

    def test_create_ha_value_object_all_max(self, device_value_all_max):
        assert device_value_all_max.ha_value.temps == ["0A28", "0A28"]
        assert device_value_all_max.ha_value.din == [True, True, True, True, True, True]

        for r in device_value_all_max.ha_value.relay:
            assert r.is_on
            assert r.overflow

        for a in device_value_all_max.ha_value.aout:
            assert a.brightness == 100
            assert a.aout_coa

        for b in device_value_all_max.ha_value.dali:
            assert b.brightness == 100
            assert b.alert_dali_communication
            assert b.alert_dali_power

    def test_format_inels_set_value_all_max(self, device_value_all_min):
        for r in device_value_all_min.ha_value.relay:
            r.is_on = True

        for a in device_value_all_min.ha_value.aout:
            a.brightness = 100

        for b in device_value_all_min.ha_value.dali:
            b.brightness = 100

        device_value = self.create_device_value(
            ha_value=device_value_all_min.ha_value,
        )

        assert (
            device_value.inels_set_value
            == "00\n00\n00\n00\n64\n64\n00\n00\n07\n07\n07\n07\n07\n07\n07\n07\n00\n00\n00\n00\n64\n64\n64\n64\n00\n00\n00\n00\n64\n64\n64\n64\n00\n00\n00\n00\n64\n64\n64\n64\n00\n00\n00\n00\n64\n64\n64\n64\n"
        )

    def test_format_inels_set_value_all_min(self, device_value_all_max):
        for r in device_value_all_max.ha_value.relay:
            r.is_on = False

        for a in device_value_all_max.ha_value.aout:
            a.brightness = 0

        for b in device_value_all_max.ha_value.dali:
            b.brightness = 0

        device_value = self.create_device_value(
            ha_value=device_value_all_max.ha_value,
        )

        assert (
            device_value.inels_set_value
            == "00\n00\n00\n00\n00\n00\n00\n00\n06\n06\n06\n06\n06\n06\n06\n06\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"
        )


class Test_CU_DEVICE_TYPE_115(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "115"

    @pytest.fixture
    def device_value_off(self):
        return self.create_device_value(inels_value="00\n0A\n28\n")

    @pytest.fixture
    def device_value_on(self):
        return self.create_device_value(inels_value="05\n0A\n28\n")

    @pytest.fixture
    def device_value_alert(self):
        return self.create_device_value(inels_value="0A\n0A\n28\n")

    @pytest.fixture
    def device_value_tamper(self):
        return self.create_device_value(inels_value="0F\n0A\n28\n")

    def test_create_ha_value_object_off(self, device_value_off):
        assert device_value_off.ha_value.temp_in == "0A28"
        assert device_value_off.ha_value.input == [0] * 2

    def test_create_ha_value_object_on(self, device_value_on):
        assert device_value_on.ha_value.temp_in == "0A28"
        assert device_value_on.ha_value.input == [1] * 2

    def test_create_ha_value_object_alert(self, device_value_alert):
        assert device_value_alert.ha_value.temp_in == "0A28"
        assert device_value_alert.ha_value.input == [2] * 2

    def test_create_ha_value_object_tamper(self, device_value_tamper):
        assert device_value_tamper.ha_value.temp_in == "0A28"
        assert device_value_tamper.ha_value.input == [3] * 2


class Test_CU_DEVICE_TYPE_116(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "116"

    @pytest.fixture
    def device_value_off(self):
        return self.create_device_value(inels_value="00\n0A\n28\n")

    @pytest.fixture
    def device_value_on(self):
        return self.create_device_value(inels_value="55\n0A\n28\n")

    @pytest.fixture
    def device_value_alert(self):
        return self.create_device_value(inels_value="AA\n0A\n28\n")

    @pytest.fixture
    def device_value_tamper(self):
        return self.create_device_value(inels_value="FF\n0A\n28\n")

    def test_create_ha_value_object_off(self, device_value_off):
        assert device_value_off.ha_value.temp_in == "0A28"
        assert device_value_off.ha_value.input == [0] * 4

    def test_create_ha_value_object_on(self, device_value_on):
        assert device_value_on.ha_value.temp_in == "0A28"
        assert device_value_on.ha_value.input == [1] * 4

    def test_create_ha_value_object_alert(self, device_value_alert):
        assert device_value_alert.ha_value.temp_in == "0A28"
        assert device_value_alert.ha_value.input == [2] * 4

    def test_create_ha_value_object_tamper(self, device_value_tamper):
        assert device_value_tamper.ha_value.temp_in == "0A28"
        assert device_value_tamper.ha_value.input == [3] * 4


class Test_CU_DEVICE_TYPE_117(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "117"

    @pytest.fixture
    def device_value_off(self):
        return self.create_device_value(inels_value="00\n00\n0A\n28\n")

    @pytest.fixture
    def device_value_on(self):
        return self.create_device_value(inels_value="55\n55\n0A\n28\n")

    @pytest.fixture
    def device_value_alert(self):
        return self.create_device_value(inels_value="AA\nAA\n0A\n28\n")

    @pytest.fixture
    def device_value_tamper(self):
        return self.create_device_value(inels_value="FF\nFF\n0A\n28\n")

    def test_create_ha_value_object_off(self, device_value_off):
        assert device_value_off.ha_value.temp == "0A28"
        assert device_value_off.ha_value.input == [0] * 8

    def test_create_ha_value_object_on(self, device_value_on):
        assert device_value_on.ha_value.temp == "0A28"
        assert device_value_on.ha_value.input == [1] * 8

    def test_create_ha_value_object_alert(self, device_value_alert):
        assert device_value_alert.ha_value.temp == "0A28"
        assert device_value_alert.ha_value.input == [2] * 8

    def test_create_ha_value_object_tamper(self, device_value_tamper):
        assert device_value_tamper.ha_value.temp == "0A28"
        assert device_value_tamper.ha_value.input == [3] * 8


class Test_CU_DEVICE_TYPE_120(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "120"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="00\n00\n07\nE4\n0B\n07\n15\n0C\n01\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.humidity == "150C"
        assert device_value.ha_value.light_in == "000007E4"
        assert device_value.ha_value.motion == True
        assert device_value.ha_value.temp_in == "0B07"


class Test_CU_DEVICE_TYPE_121(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "121"

    @pytest.fixture
    def device_value_off(self):
        return self.create_device_value(inels_value="00\n00\n00\n00\n")

    @pytest.fixture
    def device_value_on(self):
        return self.create_device_value(inels_value="55\n55\n55\n05\n")

    @pytest.fixture
    def device_value_alert(self):
        return self.create_device_value(inels_value="AA\nAA\nAA\n0A\n")

    @pytest.fixture
    def device_value_tamper(self):
        return self.create_device_value(inels_value="FF\nFF\nFF\n0F\n")

    def test_create_ha_value_object_off(self, device_value_off):
        assert device_value_off.ha_value.input == [0] * 14

    def test_create_ha_value_object_on(self, device_value_on):
        assert device_value_on.ha_value.input == [1] * 14

    def test_create_ha_value_object_alert(self, device_value_alert):
        assert device_value_alert.ha_value.input == [2] * 14

    def test_create_ha_value_object_tamper(self, device_value_tamper):
        assert device_value_tamper.ha_value.input == [3] * 14


class Test_CU_DEVICE_TYPE_122(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "122"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="03\n03\n0A\n56\n7F\nFC\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.ain == "7FFC"
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.interface == [True, True]
        assert device_value.ha_value.temp_in == "0A56"


class Test_CU_DEVICE_TYPE_123(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "123"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="0F\n03\n0A\n52\n7F\nFC\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.ain == "7FFC"
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.interface == [True, True, True, True]
        assert device_value.ha_value.temp_in == "0A52"


class Test_CU_DEVICE_TYPE_124(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "124"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="03\n03\n09\nF9\n7F\nFF\n14\n25\n05\nB0\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.ain == "7FFF"
        assert device_value.ha_value.dewpoint == "05B0"
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.interface == [True, True]
        assert device_value.ha_value.temp_in == "09F9"


class Test_CU_DEVICE_TYPE_125(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "125"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="0F\n03\n09\nF9\n7F\nFF\n14\n25\n05\nB0\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.ain == "7FFF"
        assert device_value.ha_value.dewpoint == "05B0"
        assert device_value.ha_value.humidity == "1425"
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.interface == [True, True, True, True]
        assert device_value.ha_value.temp_in == "09F9"


class Test_CU_DEVICE_TYPE_128(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "128"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(
            inels_value="9F\n2B\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n1A\n55\n09\nF4\n"
        )

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.card_id == "0000000000000000"
        assert device_value.ha_value.simple_relay[0].is_on == True
        assert device_value.ha_value.card_present == True
        assert device_value.ha_value.interface == [True, True, True]
        assert device_value.ha_value.temp_in == "09F4"

    def test_format_inels_set_value_relay_on(self, device_value):
        device_value.ha_value.simple_relay[0].is_on = True
        device_value = self.create_device_value(
            ha_value=device_value.ha_value,
        )
        assert device_value.inels_set_value == "04\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"

    def test_format_inels_set_value_relay_off(self, device_value):
        device_value.ha_value.simple_relay[0].is_on = False
        device_value = self.create_device_value(
            ha_value=device_value.ha_value,
        )
        assert device_value.inels_set_value == "00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"


class Test_CU_DEVICE_TYPE_129(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "129"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(
            inels_value="9F\n2B\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n1A\n55\n09\nF4\n"
        )

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.card_id == "0000000000000000"
        assert device_value.ha_value.simple_relay[0].is_on == True
        assert device_value.ha_value.card_present == True
        assert device_value.ha_value.interface == [True, True, True]
        assert device_value.ha_value.temp_in == "09F4"

    def test_format_inels_set_value_relay_on(self, device_value):
        device_value.ha_value.simple_relay[0].is_on = True
        device_value = self.create_device_value(ha_value=device_value.ha_value)
        assert device_value.inels_set_value == "04\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"

    def test_format_inels_set_value_relay_off(self, device_value):
        device_value.ha_value.simple_relay[0].is_on = False
        device_value = self.create_device_value(ha_value=device_value.ha_value)
        assert device_value.inels_set_value == "00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"


class Test_CU_DEVICE_TYPE_136(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "136"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="FF\n0F\n09\nDA\n00\n00\n02\n5A\n7F\nFF\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.ain == "7FFF"
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.interface == [True, True, True, True, True, True, True, True, True, True]
        assert device_value.ha_value.light_in == "0000025A"
        assert device_value.ha_value.temp_in == "09DA"


class Test_CU_DEVICE_TYPE_137(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "137"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="2A\n03\n09\nA4\n00\n00\n00\n4C\n7F\nFF\n")

    def test_create_ha_value_object_all_on(self, device_value):
        assert device_value.ha_value.interface == [True, True, True]
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.temp_in == "09A4"
        assert device_value.ha_value.light_in == "0000004C"
        assert device_value.ha_value.ain == "7FFF"


class Test_CU_DEVICE_TYPE_138(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "138"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="0F\n03\n0A\n03\n00\n00\n2F\n63\n7F\nFF\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.ain == "7FFF"
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.interface == [True, True, True, True]
        assert device_value.ha_value.light_in == "00002F63"
        assert device_value.ha_value.temp_in == "0A03"


class Test_CU_DEVICE_TYPE_139(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "139"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="3F\n03\n0A\n03\n00\n00\n2F\n63\n7F\nFF\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.ain == "7FFF"
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.interface == [True, True, True, True, True, True]
        assert device_value.ha_value.light_in == "00002F63"
        assert device_value.ha_value.temp_in == "0A03"


class Test_CU_DEVICE_TYPE_140(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "140"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="03\n03\n0A\n03\n00\n00\n2F\n63\n7F\nFF\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.ain == "7FFF"
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.interface == [True, True]
        assert device_value.ha_value.light_in == "00002F63"
        assert device_value.ha_value.temp_in == "0A03"


class Test_CU_DEVICE_TYPE_141(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "141"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="3F\n03\n0A\n03\n00\n00\n2F\n63\n7F\nFF\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.ain == "7FFF"
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.interface == [True, True, True, True, True, True]
        assert device_value.ha_value.light_in == "00002F63"
        assert device_value.ha_value.temp_in == "0A03"


class Test_CU_DEVICE_TYPE_143(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "143"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="0F\n0A\n0A\n9E\n00\n00\n24\n14\n7F\nFE\n12\n20\n05\n9D\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.interface == [True, True, True, True]
        assert device_value.ha_value.din == [True]
        assert device_value.ha_value.prox == True
        assert device_value.ha_value.temp_in == "0A9E"
        assert device_value.ha_value.light_in == "00002414"
        assert device_value.ha_value.ain == "7FFE"
        assert device_value.ha_value.humidity == "1220"
        assert device_value.ha_value.dewpoint == "059D"


class Test_CU_DEVICE_TYPE_144(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "144"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="3F\n0A\n0A\n9E\n00\n00\n24\n14\n7F\nFE\n12\n20\n05\n9D\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.interface == [True] * 6
        assert device_value.ha_value.din == [True]
        assert device_value.ha_value.prox == True
        assert device_value.ha_value.temp_in == "0A9E"
        assert device_value.ha_value.light_in == "00002414"
        assert device_value.ha_value.ain == "7FFE"
        assert device_value.ha_value.humidity == "1220"
        assert device_value.ha_value.dewpoint == "059D"


class Test_CU_DEVICE_TYPE_146(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "146"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="FF\n0B\n0A\n9E\n00\n00\n24\n14\n7F\nFE\n12\n20\n05\n9D\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.interface == [True] * 9
        assert device_value.ha_value.din == [True]
        assert device_value.ha_value.prox == True
        assert device_value.ha_value.temp_in == "0A9E"
        assert device_value.ha_value.light_in == "00002414"
        assert device_value.ha_value.ain == "7FFE"
        assert device_value.ha_value.humidity == "1220"
        assert device_value.ha_value.dewpoint == "059D"


class Test_CU_DEVICE_TYPE_147(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "147"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="0A\n28\n01\n00\n32\n32\n32\n32\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.temp_out == "0A28"
        for aout in device_value.ha_value.aout:
            assert aout.brightness == 50
            assert aout.aout_coa == True

    def test_format_inels_set_value_all_to_max(self, device_value):
        for aout in device_value.ha_value.aout:
            aout.brightness = 100

        device_value = self.create_device_value(
            ha_value=device_value.ha_value,
        )
        assert device_value.inels_set_value == "00\n00\n00\n00\n64\n64\n64\n64\n"


class Test_CU_DEVICE_TYPE_148(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "148"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="0A\n28\nFF\n00\n32\n32\n32\n32\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.temp_out == "0A28"
        for aout in device_value.ha_value.aout:
            assert aout.brightness == 50
            assert aout.aout_coa == True

    def test_format_inels_set_value_all_to_max(self, device_value):
        for aout in device_value.ha_value.aout:
            aout.brightness = 100

        device_value = self.create_device_value(
            ha_value=device_value.ha_value,
        )
        assert device_value.inels_set_value == "00\n00\n00\n00\n64\n64\n64\n64\n"


class Test_CU_DEVICE_TYPE_150(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "150"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="00\n00\n07\n00\n32\n32\n32\n32\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.sw == [True, True, True]
        for aout in device_value.ha_value.aout:
            assert aout.brightness == 50
            assert aout.aout_coa == False

    def test_format_inels_set_value_all_to_max(self, device_value):
        for aout in device_value.ha_value.aout:
            aout.brightness = 100

        device_value = self.create_device_value(
            ha_value=device_value.ha_value,
        )
        assert device_value.inels_set_value == "00\n00\n00\n00\n64\n64\n64\n64\n"


class Test_CU_DEVICE_TYPE_151(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "151"

    @pytest.fixture
    def device_value_all_max(self):
        return self.create_device_value(
            inels_value="00\nFF\n0F\n7F\n64\n64\n64\n64\n7F\n00\n00\n00\n64\n64\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"
        )

    @pytest.fixture
    def device_value_all_min(self):
        return self.create_device_value(
            inels_value="00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"
        )

    def test_create_ha_value_object_all_max(self, device_value_all_max):
        assert isinstance(device_value_all_max.ha_value.light_coa_toa[0], LightCoaToa)
        assert device_value_all_max.ha_value.sw == [True, True, True, True, True, True]
        assert device_value_all_max.ha_value.din == [True, True, True, True, True, True]
        for x in device_value_all_max.ha_value.light_coa_toa:
            assert x.brightness == 100
            assert x.toa
            assert x.coa

    def test_create_ha_value_object_all_min(self, device_value_all_min):
        assert isinstance(device_value_all_min.ha_value.light_coa_toa[0], LightCoaToa)
        assert device_value_all_min.ha_value.sw == [False, False, False, False, False, False]
        assert device_value_all_min.ha_value.din == [False, False, False, False, False, False]
        for x in device_value_all_min.ha_value.light_coa_toa:
            assert not x.brightness
            assert not x.toa
            assert not x.coa

    def test_format_inels_set_value_all_to_max(self, device_value_all_min):
        for x in device_value_all_min.ha_value.light_coa_toa:
            x.brightness = 100

        device_value = self.create_device_value(
            ha_value=device_value_all_min.ha_value,
        )
        assert (
            device_value.inels_set_value
            == "00\n00\n00\n00\n64\n64\n64\n64\n00\n00\n00\n00\n64\n64\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"
        )

    def test_format_inels_set_value_all_to_min(self, device_value_all_max):
        for x in device_value_all_max.ha_value.light_coa_toa:
            x.brightness = 0

        device_value = self.create_device_value(
            ha_value=device_value_all_max.ha_value,
        )
        assert (
            device_value.inels_set_value
            == "00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"
        )


class Test_CU_DEVICE_TYPE_153(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "153"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(
            inels_value="00\n00\n00\n00\n01\n01\n01\n01\n0A\n28\n00\n00\n64\n01\n01\n01\n00\n00\n00\n00\n01\n64\n01\n01\n00\n00\n00\n00\n01\n01\n64\n"
        )

    @pytest.fixture
    def device_value_rgbw_all_max(self):
        return self.create_device_value(
            inels_value="00\n00\n00\n00\n64\n64\n64\n64\n0A\n28\n00\n00\n64\n64\n64\n64\n00\n00\n00\n00\n64\n64\n64\n64\n00\n00\n00\n00\n64\n64\n64\n"
        )

    @pytest.fixture
    def device_value_rgbw_all_min(self):
        return self.create_device_value(
            inels_value="00\n00\n00\n00\n00\n00\n00\n00\n0A\n28\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n00\n"
        )

    def test_create_ha_value_object_rgbw_all_max(self, device_value_rgbw_all_max):
        assert device_value_rgbw_all_max.ha_value.temp_in == "0A28"
        for led in device_value_rgbw_all_max.ha_value.rgbw:
            assert led.r == 100
            assert led.g == 100
            assert led.b == 100
            assert led.w == 100
            assert led.brightness == 100

    def test_create_ha_value_object_rgbw_all_min(self, device_value_rgbw_all_min):
        assert device_value_rgbw_all_min.ha_value.temp_in == "0A28"
        for led in device_value_rgbw_all_min.ha_value.rgbw:
            assert led.r == 0
            assert led.g == 0
            assert led.b == 0
            assert led.w == 0
            assert led.brightness == 0

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.temp_in == "0A28"
        for led in device_value.ha_value.rgbw:
            assert led.r == 1
            assert led.g == 1
            assert led.b == 1
            assert led.w == 1
            assert led.brightness == 100

    def test_format_inels_set_value_all_to_min(self, device_value):
        for led in device_value.ha_value.rgbw:
            led.r, led.g, led.b, led.w, led.brightness = [100] * 5

        device_value = self.create_device_value(
            ha_value=device_value.ha_value,
        )
        assert (
            device_value.inels_set_value
            == "00\n00\n00\n00\n64\n64\n64\n64\n00\n00\n00\n00\n64\n64\n64\n64\n00\n00\n00\n00\n64\n64\n64\n64\n00\n00\n00\n00\n64\n64\n64\n00\n"
        )


class Test_CU_DEVICE_TYPE_156(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "156"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(
            inels_value="00\n00\n00\n64\n00\n00\n00\n64\n00\n00\n00\n64\n00\n00\n00\n64\n00\n00\n00\n64\n00\n00\n00\n64\n00\n"
        )

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.ains == ["00000064", "00000064", "00000064", "00000064", "00000064", "00000064"]


class Test_CU_DEVICE_TYPE_157(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "157"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="7F\nFF\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.temps == ["7FFF"]


class Test_CU_DEVICE_TYPE_158(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "158"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="7F\nFF\n7F\nFF\n7F\nFF\n7F\nFF\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.temps == ["7FFF", "7FFF", "7FFF", "7FFF"]


class Test_CU_DEVICE_TYPE_159(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "159"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="7F\nFF\n7F\nFF\n7F\nFF\n7F\nFF\n7F\nFF\n7F\nFF\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.temps == ["7FFF", "7FFF", "7FFF", "7FFF", "7FFF", "7FFF"]


class Test_CU_DEVICE_TYPE_160(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "160"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="00\n0F\n0A\n28\n00\n00\n00\n00\n0A\n28\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.din == [True, True]
        assert device_value.ha_value.interface == [True, True]
        assert device_value.ha_value.temp_in == "0A28"
        assert device_value.ha_value.temp_out == "0A28"


class Test_CU_DEVICE_TYPE_163(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "163"

    @pytest.fixture
    def device_value_open(self):
        return self.create_device_value(
            inels_value="07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\nFF\nFF\nFF\nFF\n"
        )

    @pytest.fixture
    def device_value_closed(self):
        return self.create_device_value(
            inels_value="06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n00\n00\n00\n00\n"
        )

    def test_create_ha_value_object_open(self, device_value_open):
        assert device_value_open.ha_value.interface == [True] * 18
        for shutter in device_value_open.ha_value.simple_shutters:
            assert shutter.state == Shutter_state.Open
            assert shutter.is_closed is None

    def test_create_ha_value_object_closed(self, device_value_closed):
        assert device_value_closed.ha_value.interface == [False] * 18
        for shutter in device_value_closed.ha_value.simple_shutters:
            assert shutter.state == Shutter_state.Closed
            assert shutter.is_closed is None

    def test_format_inels_set_value_all_open(self, device_value_closed):
        for x in device_value_closed.ha_value.simple_shutters:
            x.state = Shutter_state.Open

        device_value = self.create_device_value(
            ha_value=device_value_closed.ha_value,
        )
        assert (
            device_value.inels_set_value == "07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n"
        )

    def test_format_inels_set_value_all_closed(self, device_value_closed):
        for x in device_value_closed.ha_value.simple_shutters:
            x.state = Shutter_state.Closed

        device_value = self.create_device_value(
            ha_value=device_value_closed.ha_value,
        )
        assert (
            device_value.inels_set_value == "06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n"
        )


class Test_CU_DEVICE_TYPE_164(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "164"

    @pytest.fixture
    def device_value_all_max(self):
        return self.create_device_value(inels_value="00\n00\n00\n00\n64\n64\n64\n64\n")

    @pytest.fixture
    def device_value_all_min(self):
        return self.create_device_value(inels_value="00\n00\n00\n00\n00\n00\n00\n00\n")

    def test_create_ha_value_object_all_max(self, device_value_all_max):
        assert isinstance(device_value_all_max.ha_value.simple_light[0], SimpleLight)
        for x in device_value_all_max.ha_value.simple_light:
            assert x.brightness == 100

    def test_create_ha_value_object_all_min(self, device_value_all_min):
        assert isinstance(device_value_all_min.ha_value.simple_light[0], SimpleLight)
        for x in device_value_all_min.ha_value.simple_light:
            assert not x.brightness

    def test_format_inels_set_value_all_max(self, device_value_all_min):
        for x in device_value_all_min.ha_value.simple_light:
            x.brightness = 100

        device_value = self.create_device_value(
            ha_value=device_value_all_min.ha_value,
        )
        assert device_value.inels_set_value == "00\n00\n00\n00\n64\n64\n64\n64\n"

    def test_format_inels_set_value_all_min(self, device_value_all_max):
        for x in device_value_all_max.ha_value.simple_light:
            x.brightness = 0

        device_value = self.create_device_value(
            ha_value=device_value_all_max.ha_value,
        )
        assert device_value.inels_set_value == "00\n00\n00\n00\n00\n00\n00\n00\n"


class Test_CU_DEVICE_TYPE_165(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "165"

    @pytest.fixture
    def device_value_all_max(self):
        return self.create_device_value(inels_value="00\n00\n00\n00\n64\n64\n64\n64\n")

    @pytest.fixture
    def device_value_all_min(self):
        return self.create_device_value(inels_value="00\n00\n00\n00\n00\n00\n00\n00\n")

    def test_create_ha_value_object_all_max(self, device_value_all_max):
        assert isinstance(device_value_all_max.ha_value.warm_light[0], WarmLight)
        for x in device_value_all_max.ha_value.warm_light:
            assert x.brightness == 100
            assert x.relative_ct == 100

    def test_create_ha_value_object_all_min(self, device_value_all_min):
        assert isinstance(device_value_all_min.ha_value.warm_light[0], WarmLight)
        for x in device_value_all_min.ha_value.warm_light:
            assert not x.brightness
            assert not x.relative_ct

    def test_format_inels_set_value_all_max(self, device_value_all_min):
        for x in device_value_all_min.ha_value.warm_light:
            x.brightness = 100

        device_value = self.create_device_value(
            ha_value=device_value_all_min.ha_value,
        )
        assert device_value.inels_set_value == "00\n00\n00\n00\n64\n00\n64\n00\n"

    def test_format_inels_set_value_all_min(self, device_value_all_max):
        for x in device_value_all_max.ha_value.warm_light:
            x.brightness = 0

        device_value = self.create_device_value(
            ha_value=device_value_all_max.ha_value,
        )
        assert device_value.inels_set_value == "00\n00\n00\n00\n00\n64\n00\n64\n"


class Test_CU_DEVICE_TYPE_166(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "166"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(
            inels_value="3F\n0A\n00\n00\nFB\nFF\nFF\n7F\nFB\nFF\nFF\n7F\n00\n00\n00\n00\n00\n00\n00\n00\nFB\nFF\nFF\n7F\n00\n00\n00\n00\n00\n00\n00\n"
        )

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.climate_controller.current == 26.23
        assert device_value.ha_value.climate_controller.required == 0
        assert device_value.ha_value.climate_controller.required_cool == 0
        assert device_value.ha_value.climate_controller.climate_mode == 0
        assert device_value.ha_value.climate_controller.current_action == 0
        assert device_value.ha_value.climate_controller.critical_temp == 21474836.43
        assert device_value.ha_value.climate_controller.correction_temp == 0.0
        assert device_value.ha_value.climate_controller.public_holiday == 0
        assert device_value.ha_value.climate_controller.vacation == False
        assert device_value.ha_value.climate_controller.control_mode == 0
        assert device_value.ha_value.climate_controller.current_preset == 5

    def test_format_inels_set_value_all_to_max(self, device_value):
        device_value = self.create_device_value(
            ha_value=device_value.ha_value,
        )
        assert (
            device_value.inels_set_value
            == "3F\n0A\n00\n00\nFB\nFF\nFF\n7F\n00\n00\n00\n00\n00\n00\n00\n00\n00\n07\n00\n"
        )


class Test_CU_DEVICE_TYPE_167(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "167"

    @pytest.fixture
    def device_value_on(self):
        return self.create_device_value(inels_value="00\n01\n")

    @pytest.fixture
    def device_value_off(self):
        return self.create_device_value(inels_value="00\n00\n")

    def test_create_ha_value_object_on(self, device_value_on):
        assert device_value_on.ha_value.heating_out == True

    def test_create_ha_value_object_off(self, device_value_off):
        assert device_value_off.ha_value.heating_out == False


class Test_CU_DEVICE_TYPE_168(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "168"

    @pytest.fixture
    def device_value_on(self):
        return self.create_device_value(inels_value="00\n01\n")

    @pytest.fixture
    def device_value_off(self):
        return self.create_device_value(inels_value="00\n00\n")

    def test_create_ha_value_object_on(self, device_value_on):
        assert device_value_on.ha_value.cooling_out == True

    def test_create_ha_value_object_off(self, device_value_off):
        assert device_value_off.ha_value.cooling_out == False


class Test_CU_DEVICE_TYPE_169(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "169"

    @pytest.fixture
    def device_value_all_on(self):
        return self.create_device_value(
            inels_value="07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n07\n00\n00\n00\nFF\n3F\n"
        )

    @pytest.fixture
    def device_value_all_off(self):
        return self.create_device_value(
            inels_value="06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n06\n00\n00\n00\n00\n00\n"
        )

    def test_create_ha_value_object_all_on(self, device_value_all_on):
        assert isinstance(device_value_all_on.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_on.ha_value.sw == [True] * 14
        for r in device_value_all_on.ha_value.simple_relay:
            assert r.is_on

    def test_create_ha_value_object_all_off(self, device_value_all_off):
        assert isinstance(device_value_all_off.ha_value.simple_relay[0], SimpleRelay)
        assert device_value_all_off.ha_value.sw == [False] * 14
        for r in device_value_all_off.ha_value.simple_relay:
            assert not r.is_on

    def test_format_inels_set_value_all_on(self, device_value_all_off):
        for r in device_value_all_off.ha_value.simple_relay:
            r.is_on = True

        device_value = self.create_device_value(ha_value=device_value_all_off.ha_value)
        assert device_value.inels_set_value == "07\n" * 14

    def test_format_inels_set_value_all_off(self, device_value_all_on):
        for r in device_value_all_on.ha_value.simple_relay:
            r.is_on = False

        device_value = self.create_device_value(
            ha_value=device_value_all_on.ha_value,
        )
        assert device_value.inels_set_value == "06\n" * 14


class Test_CU_DEVICE_TYPE_170(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "170"

    @pytest.fixture
    def device_value_open(self):
        return self.create_device_value(
            inels_value="07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\nFF\nFF\nFF\nFF\nFF\n"
        )

    @pytest.fixture
    def device_value_closed(self):
        return self.create_device_value(
            inels_value="06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n00\n00\n00\n00\n00\n"
        )

    def test_create_ha_value_object_open(self, device_value_open):
        assert device_value_open.ha_value.interface == [True] * 35
        for shutter in device_value_open.ha_value.simple_shutters:
            assert shutter.state == Shutter_state.Open
            assert shutter.is_closed is None

    def test_create_ha_value_object_closed(self, device_value_closed):
        assert device_value_closed.ha_value.interface == [False] * 35
        for shutter in device_value_closed.ha_value.simple_shutters:
            assert shutter.state == Shutter_state.Closed
            assert shutter.is_closed is None

    def test_format_inels_set_value(self, device_value_closed):
        device_value_closed.ha_value.simple_shutters[0].state = Shutter_state.Open
        device_value_closed.ha_value.simple_shutters[6].state = Shutter_state.Open
        device_value = self.create_device_value(
            ha_value=device_value_closed.ha_value,
        )
        assert device_value.inels_set_value == "07\n06\n06\n07\n06\n07\n06\n07\n06\n07\n06\n07\n07\n06\n"


class Test_CU_DEVICE_TYPE_171(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "171"

    @pytest.fixture
    def device_value_move_in_on(self):
        return self.create_device_value(inels_value="01\n")

    @pytest.fixture
    def device_value_move_in_off(self):
        return self.create_device_value(inels_value="00\n")

    def test_create_ha_value_object_on(self, device_value_move_in_on):
        assert device_value_move_in_on.ha_value.motion

    def test_create_ha_value_object_off(self, device_value_move_in_off):
        assert not device_value_move_in_off.ha_value.motion


class Test_CU_DEVICE_TYPE_172(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "172"

    @pytest.fixture
    def device_value_move_in_on(self):
        return self.create_device_value(inels_value="01\n")

    @pytest.fixture
    def device_value_move_in_off(self):
        return self.create_device_value(inels_value="00\n")

    def test_create_ha_value_object_on(self, device_value_move_in_on):
        assert device_value_move_in_on.ha_value.motion

    def test_create_ha_value_object_off(self, device_value_move_in_off):
        assert not device_value_move_in_off.ha_value.motion


class Test_CU_DEVICE_TYPE_174(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "174"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="0F\n0E\n0A\n9E\n00\n00\n24\n14\n7F\nFE\n12\n20\n05\n9D\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.interface == [True, True, True, True]
        assert device_value.ha_value.din == [True]
        assert device_value.ha_value.prox == True
        assert device_value.ha_value.temp_in == "0A9E"
        assert device_value.ha_value.light_in == "00002414"
        assert device_value.ha_value.ain == "7FFE"
        assert device_value.ha_value.humidity == "1220"
        assert device_value.ha_value.dewpoint == "059D"


class Test_CU_DEVICE_TYPE_175(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "175"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="3F\n0E\n0A\n9E\n00\n00\n24\n14\n7F\nFE\n12\n20\n05\n9D\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.interface == [True] * 6
        assert device_value.ha_value.din == [True]
        assert device_value.ha_value.prox == True
        assert device_value.ha_value.temp_in == "0A9E"
        assert device_value.ha_value.light_in == "00002414"
        assert device_value.ha_value.ain == "7FFE"
        assert device_value.ha_value.humidity == "1220"
        assert device_value.ha_value.dewpoint == "059D"


class Test_CU_DEVICE_TYPE_176(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "176"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="FF\n0F\n0A\n9E\n00\n00\n24\n14\n7F\nFE\n12\n20\n05\n9D\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.interface == [True] * 9
        assert device_value.ha_value.din == [True]
        assert device_value.ha_value.prox == True
        assert device_value.ha_value.temp_in == "0A9E"
        assert device_value.ha_value.light_in == "00002414"
        assert device_value.ha_value.ain == "7FFE"
        assert device_value.ha_value.humidity == "1220"
        assert device_value.ha_value.dewpoint == "059D"


class Test_CU_DEVICE_TYPE_177(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "177"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="0F\n0A\n0A\n9E\n00\n00\n24\n14\n7F\nFE\n12\n20\n05\n9D\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.interface == [True, True, True, True]
        assert device_value.ha_value.din == [True]
        assert device_value.ha_value.prox == True
        assert device_value.ha_value.temp_in == "0A9E"
        assert device_value.ha_value.light_in == "00002414"
        assert device_value.ha_value.ain == "7FFE"
        assert device_value.ha_value.humidity == "1220"
        assert device_value.ha_value.dewpoint == "059D"


class Test_CU_DEVICE_TYPE_178(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "178"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="3F\n0A\n0A\n9E\n00\n00\n24\n14\n7F\nFE\n12\n20\n05\n9D\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.interface == [True] * 6
        assert device_value.ha_value.din == [True]
        assert device_value.ha_value.prox == True
        assert device_value.ha_value.temp_in == "0A9E"
        assert device_value.ha_value.light_in == "00002414"
        assert device_value.ha_value.ain == "7FFE"
        assert device_value.ha_value.humidity == "1220"
        assert device_value.ha_value.dewpoint == "059D"


class Test_CU_DEVICE_TYPE_180(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "180"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(
            inels_value="00\n7F\n0A\n1D\n00\n00\n00\n03\n00\n00\n04\n37\n7F\nFF\n16\n60\n06\n7B\n"
        )

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.din == [True]
        assert device_value.ha_value.prox == True
        assert device_value.ha_value.interface == [True] * 7
        assert device_value.ha_value.temp_in == "0A1D"
        assert device_value.ha_value.light_in == "00000437"
        assert device_value.ha_value.ain == "7FFF"
        assert device_value.ha_value.humidity == "1660"
        assert device_value.ha_value.dewpoint == "067B"
        assert device_value.ha_value.backlit == False


class Test_CU_DEVICE_TYPE_179(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "179"

    @pytest.fixture
    def device_value(self):
        return self.create_device_value(inels_value="FF\n0B\n0A\n9E\n00\n00\n24\n14\n7F\nFE\n12\n20\n05\n9D\n")

    def test_create_ha_value_object(self, device_value):
        assert device_value.ha_value.interface == [True] * 9
        assert device_value.ha_value.din == [True]
        assert device_value.ha_value.prox == True
        assert device_value.ha_value.temp_in == "0A9E"
        assert device_value.ha_value.light_in == "00002414"
        assert device_value.ha_value.ain == "7FFE"
        assert device_value.ha_value.humidity == "1220"
        assert device_value.ha_value.dewpoint == "059D"


class Test_CU_DEVICE_TYPE_BITS(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "bits"

    @pytest.fixture
    def device_value_all_off(self):
        return self.create_device_value(
            inels_value='{"last_seen":"1970-01-02T02:18:15.+0100Z", "state":{"000":0,"001":0,"002":0,"003":0,"004":0,"005":0,"006":0,"007":0,"008":0,"009":0,"010":0,"011":0,"012":0,"013":0}}'
        )

    @pytest.fixture
    def device_value_all_on(self):
        return self.create_device_value(
            inels_value='{"last_seen":"1970-01-02T02:18:15.+0100Z", "state":{"000":1,"001":1,"002":1,"003":1,"004":1,"005":1,"006":1,"007":1,"008":1,"009":1,"010":1,"011":1,"012":1,"013":1}}'
        )

    def test_create_ha_value_object_all_on(self, device_value_all_on):
        for b in device_value_all_on.ha_value.bit:
            assert b.is_on

    def test_create_ha_value_object_all_off(self, device_value_all_off):
        for b in device_value_all_off.ha_value.bit:
            assert not b.is_on

    def test_format_inels_set_value_all_on(self, device_value_all_off):
        for b in device_value_all_off.ha_value.bit:
            b.is_on = True

        device_value = self.create_device_value(
            ha_value=device_value_all_off.ha_value,
        )
        assert (
            device_value.inels_set_value
            == '{"cmd": {"000": 1, "001": 1, "002": 1, "003": 1, "004": 1, "005": 1, "006": 1, "007": 1, "008": 1, "009": 1, "010": 1, "011": 1, "012": 1, "013": 1}}'
        )

    def test_format_inels_set_value_all_off(self, device_value_all_on):
        for b in device_value_all_on.ha_value.bit:
            b.is_on = False

        device_value = self.create_device_value(
            ha_value=device_value_all_on.ha_value,
        )
        assert (
            device_value.inels_set_value
            == '{"cmd": {"000": 0, "001": 0, "002": 0, "003": 0, "004": 0, "005": 0, "006": 0, "007": 0, "008": 0, "009": 0, "010": 0, "011": 0, "012": 0, "013": 0}}'
        )


class Test_CU_DEVICE_TYPE_INTEGERS(BaseDeviceTestClass):
    DEVICE_TYPE_ID = "integers"

    @pytest.fixture
    def device_value_all_off(self):
        return self.create_device_value(
            inels_value='{"last_seen":"1970-01-02T02:18:15.+0100Z", "state":{"000":0,"001":0,"002":0,"003":0,"004":0,"005":0,"006":0,"007":0,"008":0,"009":0,"010":0,"011":0,"012":0,"013":0}}'
        )

    @pytest.fixture
    def device_value_all_on(self):
        return self.create_device_value(
            inels_value='{"last_seen":"1970-01-02T02:18:15.+0100Z", "state":{"000":1000,"001":1000,"002":1000,"003":1000,"004":1000,"005":1000,"006":1000,"007":1000,"008":1000,"009":1000,"010":1000,"011":1000,"012":1000,"013":1000}}'
        )

    def test_create_ha_value_object_all_on(self, device_value_all_on):
        for n in device_value_all_on.ha_value.number:
            assert n.value == 1000

    def test_create_ha_value_object_all_off(self, device_value_all_off):
        for n in device_value_all_off.ha_value.number:
            assert not n.value

    def test_format_inels_set_value_all_on(self, device_value_all_off):
        for n in device_value_all_off.ha_value.number:
            n.value = 1

        device_value = self.create_device_value(
            ha_value=device_value_all_off.ha_value,
        )
        assert (
            device_value.inels_set_value
            == '{"cmd": {"000": 1, "001": 1, "002": 1, "003": 1, "004": 1, "005": 1, "006": 1, "007": 1, "008": 1, "009": 1, "010": 1, "011": 1, "012": 1, "013": 1}}'
        )

    def test_format_inels_set_value_all_off(self, device_value_all_on):
        for n in device_value_all_on.ha_value.number:
            n.value = 0

        device_value = self.create_device_value(
            ha_value=device_value_all_on.ha_value,
        )
        assert (
            device_value.inels_set_value
            == '{"cmd": {"000": 0, "001": 0, "002": 0, "003": 0, "004": 0, "005": 0, "006": 0, "007": 0, "008": 0, "009": 0, "010": 0, "011": 0, "012": 0, "013": 0}}'
        )


if __name__ == "__main__":
    pytest.main()
