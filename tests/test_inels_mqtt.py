import pytest
from unittest.mock import MagicMock, Mock, patch
from inelsmqtt import InelsMqtt
import paho.mqtt.client as mqtt

@pytest.fixture
def mqtt_config():
    return {
        'host': 'localhost',
        'port': 1883,
        'username': 'user',
        'password': 'pass',
        'client_id': 'testclient',
        'timeout': 0
    }

@pytest.fixture
def mqtt_client_mock():
    with patch('paho.mqtt.client.Client') as mock:
        yield mock()

@pytest.fixture
def inels_mqtt(mqtt_config, mqtt_client_mock):
    with patch('paho.mqtt.client.Client', return_value=mqtt_client_mock):
        return InelsMqtt(config=mqtt_config)


def test_instance_initialization_pytest_style(inels_mqtt, mqtt_config):
    """Testing initialization of all props. InelsMqtt class."""    
    assert inels_mqtt._InelsMqtt__host == mqtt_config['host']  # pylint: disable=protected-access
    assert inels_mqtt._InelsMqtt__port == mqtt_config['port']  # pylint: disable=protected-access


def test_publish_pytest_style(mqtt_client_mock, inels_mqtt):
    """Test publishing a message using pytest."""
    mqtt_client_mock.publish.return_value = (mqtt.MQTT_ERR_SUCCESS, 1)
    
    inels_mqtt.publish('inels/status/10e97f8b7d30/01/01E8', 'data')
    
    # Assert that the publish method was called with the correct parameters
    mqtt_client_mock.publish.assert_called_once_with('inels/status/10e97f8b7d30/01/01E8', 'data', 0, True, None)
    

def test_is_available_true_false_based_on__on_connect_function(mqtt_client_mock, inels_mqtt):
    """Testing if the broker is available with result True or False based on the on_connect function."""

    # Simulate successful connection
    inels_mqtt.client.on_connect(None, None, None, mqtt.CONNACK_ACCEPTED)
    assert inels_mqtt.is_available == True

    # Simulate connection refused
    inels_mqtt.client.on_connect(None, None, None, mqtt.CONNACK_REFUSED_NOT_AUTHORIZED)
    assert inels_mqtt.is_available == False


def test_discovery_all_with_tree_messages(mqtt_client_mock, inels_mqtt):
    """Test discovery function to find and register all interested topics."""

    # Initialize three topics with status
    items = {
        "inels/status/45464654/02/457544": "rrqeraad",
        "inels/status/45464654/02/74544": "eeeqqq",
        "inels/status/45464654/02/8887": "adfadfefe",
        "some/kind/of/different/topic/in/broker": "adfadf",  # should be filtered out
    }

    for item in items.items():
        msg = type("msg", (object,), {"topic": item[0], "payload": item[1]})
        inels_mqtt._InelsMqtt__on_discover(  # pylint: disable=protected-access
            inels_mqtt, Mock(), msg
        )

    devices = inels_mqtt.discovery_all()
    assert len(devices) == 3


def test_subscribe(mqtt_client_mock, inels_mqtt):
    """Test subscribing to a topic."""

    topic = 'inels/status/10e97f8b7d30/01/01E8'
    msg = type(
        "msg",
        (object,),
        {"topic": topic, "payload": "02\n01\n"},
    )

    inels_mqtt._InelsMqtt__on_message(
        inels_mqtt, Mock(), msg
    )

    # mqtt_client_mock.is_connected.return_value = True
    # mqtt_client_mock.subscribe.return_value = (mqtt.MQTT_ERR_SUCCESS, 1)

    last_messages = inels_mqtt.subscribe(topic)

    mqtt_client_mock.subscribe.assert_called_once_with(topic, 0, None, None)
    assert inels_mqtt._InelsMqtt__is_subscribed_list[topic] == True
    assert msg.payload == last_messages


def test_message_property(inels_mqtt):
    """Test if message property returns right data using pytest."""
    dictionary = {
        "inels/status/555555/02/3423452435": "first",
        "inels/status/555555/02/3424524222": "second",
        "inels/status/555555/03/452435234": "third",
        "inels/status/222222/02/85034495": "fourth",
    }

    # fill up __message prop
    inels_mqtt._InelsMqtt__messages = dictionary  # pylint: disable=protected-access

    assert inels_mqtt.messages() is not None
    assert len(inels_mqtt.messages()) == 4
    assert inels_mqtt.messages() == dictionary


def test_subscribe_listeners(mqtt_client_mock, inels_mqtt):
    """Test listerner subscription."""

    def dummy_callback(prm):
        """Dummy callback function"""
        return prm

    # Subscribe listeners with dummy callback
    inels_mqtt.subscribe_listener("inels/status/10e97f8b7d30/01/01E8", "uid_1", dummy_callback)
    inels_mqtt.subscribe_listener("inels/status/10e97f8b7d30/03/03E8", "uid_2", dummy_callback)

    # Assert that two listeners are subscribed
    assert len(inels_mqtt.list_of_listeners) == 2
    assert "uid_1" in inels_mqtt.list_of_listeners["10e97f8b7d30/01/01E8"]
    assert "uid_2" in inels_mqtt.list_of_listeners["10e97f8b7d30/03/03E8"]


def test_unsubscribe_listeners(inels_mqtt):
    """Test unsubscribe all listeners."""

    def dummy_callback(prm):
        """Dummy callback function"""
        return prm

    # Subscribe listeners
    inels_mqtt.subscribe_listener("inels/status/10e97f8b7d30/01/01E8", "uid_1", dummy_callback)
    inels_mqtt.subscribe_listener("inels/status/10e97f8b7d30/03/03E8", "uid_2", dummy_callback)

    # Check if two listeners are subscribed
    assert len(inels_mqtt.list_of_listeners) == 2

    # Unsubscribe all listeners
    inels_mqtt.unsubscribe_listeners()

    # Check if no listeners are left
    assert len(inels_mqtt.list_of_listeners) == 0