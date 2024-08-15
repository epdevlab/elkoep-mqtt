import functools
import time
from enum import Enum
from typing import Any, Callable, List, Tuple

from inelsmqtt import InelsMqtt
from inelsmqtt.devices import Device
from inelsmqtt.utils.common import SettableAttribute, new_object

# logging.basicConfig(
#     level=logging.DEBUG,
#     # level=logging.INFO,
#     format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#     handlers=[
#         logging.StreamHandler()
#     ]
# )


def print_centered(text: str, width: int = 80) -> None:
    print(f"\n{text.upper():*^{width}}\n")


def centered_function_name(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print_centered(f" {func.__name__} ")
        result = func(*args, **kwargs)
        print_centered("")
        return result

    return wrapper


class AttributeRoute:
    def __init__(self, route: List[str], attr_type: type):
        self.route = route
        self.attr_type = attr_type

    def get_value(self, obj: Any) -> Any:
        for attr in self.route:
            if isinstance(obj, list) and attr.isdigit():
                obj = obj[int(attr)]
            else:
                obj = getattr(obj, attr)
        return obj

    def set_value(self, obj: Any, value: Any) -> None:
        for attr in self.route[:-1]:
            if isinstance(obj, list) and attr.isdigit():
                obj = obj[int(attr)]
            else:
                obj = getattr(obj, attr)

        if isinstance(obj, list) and self.route[-1].isdigit():
            obj[int(self.route[-1])] = value
        else:
            setattr(obj, self.route[-1], value)


class IntegrationDeviceTester:
    def __init__(self, config: dict[str, Any], device_topic: str) -> None:
        self.config = config
        self.mqtt = None
        self.device = None

        self.device_topic = device_topic.split("/")
        self.gateway = self.device_topic[2]
        self.device_class = self.device_topic[3]
        self.device_id = self.device_topic[4]

        self.settable_options: List[Tuple[str, SettableAttribute]] = []

    def setup(self) -> None:
        self.mqtt = InelsMqtt(self.config)
        self.mqtt.client.on_message = self.mqtt._InelsMqtt__on_message

        self.device = Device(
            self.mqtt,
            state_topic=f"inels/status/{self.gateway}/{self.device_class}/{self.device_id}",
            title=self.device_id,
        )

        topics = [self.device.gw_connected_topic, self.device.connected_topic, self.device.state_topic]

        self.mqtt.subscribe(topics, qos=0)
        self.mqtt.subscribe_listener(self.device.state_topic, self.device.unique_id, self.callback)

        # Wait for initial state
        for _ in range(3):
            time.sleep(0.5)
            if self.device.state:
                break

        self.initialize_settable_options()

    def teardown(self) -> None:
        if self.mqtt:
            self.mqtt.disconnect()

    def callback(self, availability_update: bool) -> None:
        self.device.callback(availability_update)
        # if not availability_update:
        #     self.current_device_state()

    def initialize_settable_options(self) -> None:
        self.settable_options = []
        if self.device.state:
            settable_attrs = self.device.get_settable_attributes()
            for attr_name, attr_info in settable_attrs.items():
                self.settable_options.append((attr_name, attr_info))

    @centered_function_name
    def current_device_state(self) -> None:
        anonymous_type = type(new_object())

        def print_object(obj, indent=""):
            for attr, val in vars(obj).items():
                if not attr.startswith("_"):
                    if isinstance(val, anonymous_type):
                        print(f"{indent}{attr}:")
                        print_object(val, indent + "  ")
                    elif isinstance(val, list):
                        print(f"{indent}{attr}:")
                        for i, item in enumerate(val):
                            if isinstance(item, anonymous_type):
                                print(f"{indent}  [{i}]:")
                                print_object(item, indent + "    ")
                            else:
                                print(f"{indent}  [{i}]: {item}")
                    else:
                        print(f"{indent}{attr}: {val}")

        if not self.device.state:
            print("No state available")
            return

        print_object(self.device.state)

    def set_state(self, option_index: int, value: str) -> str:
        attr_name, attr_info = self.settable_options[option_index]

        ha_value = self.device.state

        # Convert the value to the correct type
        if issubclass(attr_info.attr_type, Enum):
            try:
                enum_value = next(v for v in attr_info.attr_type if v.value == int(value))
                typed_value = enum_value
            except (ValueError, StopIteration):
                return f"Invalid value for {attr_name}. Please enter a valid integer corresponding to the enum value."
        elif attr_info.attr_type == bool:
            typed_value = value.lower() in ["true", "1"]
        else:
            try:
                typed_value = attr_info.attr_type(value)
            except ValueError:
                return f"Invalid value for {attr_name}. Please enter a value of type {attr_info.attr_type.__name__}."

        # Hack for DT21: Set 'set_pos' to True when setting 'position'
        if attr_name == "position":
            ha_value.shutters_with_pos[0].set_pos = True

        route = AttributeRoute(attr_info.route.split("."), attr_info.attr_type)
        route.set_value(ha_value, typed_value)

        try:
            self.device.set_ha_value(ha_value)
            return f"\nSuccessfully set {attr_name} to {typed_value}"
        except Exception as e:
            return f"Error setting {attr_name}: {str(e)}"

    def print_settable_options(self) -> None:
        print("\nSettable options:")
        for i, (attr, attr_info) in enumerate(self.settable_options):
            print(f"{i + 1}. {attr} ({attr_info.attr_type.__name__})")
            route = AttributeRoute(attr_info.route.split("."), attr_info.attr_type)
            current_value = route.get_value(self.device.state)
            print(f"   Current value: {current_value}")
            print(f"   {attr_info.get_value_description()}")

    def run_test(self) -> None:
        self.setup()
        while True:
            print("\nAvailable commands:")
            print("1. Get current state")
            print("2. Set state")
            print("3. Exit")

            command = input("Enter command number: ").strip()

            if command == "1":
                self.current_device_state()
            elif command == "2":
                self.print_settable_options()
                if not self.settable_options:
                    print("No settable options available for this device.")
                    continue

                while True:
                    option = input("Enter option number to set: ").strip().lower()
                    try:
                        option_index = int(option) - 1
                        if 0 <= option_index < len(self.settable_options):
                            while True:
                                value = input(f"Enter new value for option {option}: ").strip()
                                result = self.set_state(option_index, value)
                                print(result)
                                if not result.startswith("Invalid value"):
                                    break
                            break
                        else:
                            if len(self.settable_options) == 1:
                                print("Invalid option. Please enter 1.")
                            else:
                                print(
                                    f"Invalid option. Please enter a number between 1 and {len(self.settable_options)}."
                                )
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            elif command == "3":
                break
            else:
                print("Invalid command. Please enter 1, 2, or 3.")

        self.teardown()


if __name__ == "__main__":
    # python -m tests.device_tester

    config = {
        "host": "10.10.3.237",
        "port": 1883,
        "username": "dbranik",
        "password": "Elkoep123.",
        "protocol": 5,
        "keepalive": 60,
    }

    # device_topic = "inels/status/2C6A6F10328C/01/00D002"
    # device_topic = "inels/connected/2C6A6F10328C/02/00286C"
    # device_topic = "inels/connected/2C6A6F10328C/03/003C5B"
    # device_topic = "inels/connected/2C6A6F10328C/04/00F300"
    # device_topic = "inels/connected/2C6A6F10328C/05/00F6D2"
    # device_topic = "inels/connected/2C6A6F10328C/06/00A87E"
    # device_topic = "inels/connected/2C6A6F10328C/07/00326A"
    # device_topic = "inels/status/2C6A6F10328C/09/0507A6"
    # device_topic = "inels/connected/2C6A6F10328C/10/001B35"
    # device_topic = "inels/connected/2C6A6F10328C/12/03A5E6"
    # device_topic = "inels/connected/2C6A6F10328C/13/016550"
    # device_topic = "inels/connected/2C6A6F10328C/15/01C227"
    # device_topic = "inels/connected/2C6A6F10328C/16/02BEAF"
    # device_topic = "inels/connected/2C6A6F10328C/17/039A53"
    # device_topic = "inels/connected/2C6A6F10328C/18/053445"
    # device_topic = "inels/connected/2C6A6F10328C/19/053444"
    device_topic = "inels/connected/2C6A6F10328C/21/03DF55"
    # device_topic = "inels/connected/2C6A6F10328C/30/059A3B"

    tester = IntegrationDeviceTester(config, device_topic)
    tester.run_test()
