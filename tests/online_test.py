"""Online tests."""
# from unittest import TestCase
# from inelsmqtt import InelsMqtt
# from inelsmqtt.devices import Device


# class OnlineTest(TestCase):
#     """Discovery class tests

#     Args:
#         TestCase (_type_): Base class of unit testing
#     """

#     def setUp(self) -> None:
#         """Setup."""
#         config = {
#             "host": "192.168.2.5",
#             "port": 2883,
#             "username": "ufo",
#             "password": "ufoufoufo",
#             "protocol": 5,
#         }

#         self.mqtt = InelsMqtt(config)

#     def tearDown(self) -> None:
#         """Tear down."""
#         self.mqtt = None

#     def test_connect(self) -> None:
#         """Connect test."""

#         result = self.mqtt.test_connection()
#         self.assertTrue(result)

#     def test_publish(self) -> None:
#         """Publish data to the borker."""
#         device = Device(self.mqtt, "inels/002C6A6F10/set/01/040707FF")
#         device.set_ha_value(False)

#         device.set_ha_value(True)
