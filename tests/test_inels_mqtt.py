from unittest.mock import Mock, patch

import paho.mqtt.client as mqtt
import pytest

from inelsmqtt import InelsMqtt


@pytest.fixture
def mqtt_config():
    return {
        "host": "localhost",
        "port": 1883,
        "username": "user",
        "password": "pass",
        "client_id": "testclient",
        "timeout": 0,
    }


@pytest.fixture
def mqtt_client_mock():
    with patch("paho.mqtt.client.Client") as mock:
        yield mock()


@pytest.fixture
def inels_mqtt(mqtt_config, mqtt_client_mock):
    with patch("paho.mqtt.client.Client", return_value=mqtt_client_mock):
        return InelsMqtt(config=mqtt_config)


def test_instance_initialization_pytest_style(inels_mqtt, mqtt_config):
    """Testing initialization of all props. InelsMqtt class."""
    assert inels_mqtt._InelsMqtt__host == mqtt_config["host"]  # pylint: disable=protected-access
    assert inels_mqtt._InelsMqtt__port == mqtt_config["port"]  # pylint: disable=protected-access


def test_publish_successful(mqtt_client_mock, inels_mqtt):
    """Test successful publishing of a message."""
    info = Mock()
    info.rc = mqtt.MQTT_ERR_SUCCESS
    info.is_published.return_value = True

    mqtt_client_mock.publish.return_value = info

    result = inels_mqtt.publish("inels/status/10e97f8b7d30/01/01E8", "data")

    mqtt_client_mock.publish.assert_called_once_with("inels/status/10e97f8b7d30/01/01E8", "data", 0, True, None)

    assert result == True


def test_publish_unsuccessful(mqtt_client_mock, inels_mqtt):
    """Test unsuccessful publishing of a message."""
    info = Mock()
    info.rc = mqtt.MQTT_ERR_NO_CONN

    mqtt_client_mock.publish.return_value = info

    result = inels_mqtt.publish("inels/status/10e97f8b7d30/01/01E8", "data")

    mqtt_client_mock.publish.assert_called_once_with("inels/status/10e97f8b7d30/01/01E8", "data", 0, True, None)

    assert result == False


def test_publish_exception(mqtt_client_mock, inels_mqtt):
    """Test publishing a message with an exception during wait_for_publish."""
    info = Mock()
    info.rc = mqtt.MQTT_ERR_SUCCESS
    info.is_published.return_value = False
    info.wait_for_publish.side_effect = Exception("Timeout")

    mqtt_client_mock.publish.return_value = info

    result = inels_mqtt.publish("inels/status/10e97f8b7d30/01/01E8", "data")

    mqtt_client_mock.publish.assert_called_once_with("inels/status/10e97f8b7d30/01/01E8", "data", 0, True, None)

    assert result == False


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

    mqtt_client_mock.subscribe.return_value = (mqtt.MQTT_ERR_SUCCESS, 1)

    devices = inels_mqtt.discovery_all()
    assert len(devices) == 3


def test_subscribe_successful(mqtt_client_mock, inels_mqtt):
    """Test successful subscription to topics."""
    topics = [("inels/status/10e97f8b7d30/01/01E8", 0), ("inels/status/10e97f8b7d30/01/01E9", 0)]

    mqtt_client_mock.subscribe.return_value = (mqtt.MQTT_ERR_SUCCESS, 1)

    # Simulate the behavior of __on_subscribe
    def wait_for_side_effect(condition_func, timeout):
        for topic, _ in topics:
            inels_mqtt._InelsMqtt__is_subscribed_list[topic] = True
            inels_mqtt._InelsMqtt__expected_mid.pop(topic, None)

    inels_mqtt._InelsMqtt__subscription_condition.wait_for = wait_for_side_effect
    inels_mqtt._InelsMqtt__timeout = 0.1
    result = inels_mqtt.subscribe(topics)

    mqtt_client_mock.subscribe.assert_called_once_with(topics, None, None)
    assert result == {topic: None for topic, _ in topics}

    for topic, _ in topics:
        assert inels_mqtt._InelsMqtt__is_subscribed_list[topic] == True
        assert topic not in inels_mqtt._InelsMqtt__expected_mid


def test_subscribe_unsuccessful(mqtt_client_mock, inels_mqtt):
    """Test unsuccessful subscription to a topic."""
    topics = [("inels/status/10e97f8b7d30/01/01E8", 0), ("inels/status/10e97f8b7d30/01/01E9", 0)]

    mqtt_client_mock.subscribe.return_value = (mqtt.MQTT_ERR_NO_CONN, 0)

    result = inels_mqtt.subscribe(topics)

    mqtt_client_mock.subscribe.assert_called_once_with(topics, None, None)
    assert result == {}

    # Check that failed topics are removed
    for topic, _ in topics:
        assert topic not in inels_mqtt._InelsMqtt__is_subscribed_list
        assert topic not in inels_mqtt._InelsMqtt__expected_mid


def test_subscribe_unsuccessful_wait_for(mqtt_client_mock, inels_mqtt):
    """Test unsuccessful subscription to a topic with wait_for."""
    topics = [("inels/status/10e97f8b7d30/01/01E8", 0), ("inels/status/10e97f8b7d30/01/01E9", 0)]

    mqtt_client_mock.subscribe.return_value = (mqtt.MQTT_ERR_SUCCESS, 1)

    # Simulate initial state
    for i, (topic, _) in enumerate(topics):
        inels_mqtt._InelsMqtt__is_subscribed_list[topic] = False
        inels_mqtt._InelsMqtt__expected_mid[topic] = i

    inels_mqtt._InelsMqtt__timeout = 0.01
    result = inels_mqtt.subscribe(topics)

    mqtt_client_mock.subscribe.assert_called_once_with(topics, None, None)
    assert result == {"inels/status/10e97f8b7d30/01/01E8": None, "inels/status/10e97f8b7d30/01/01E9": None}

    # Check that failed topics are removed
    for topic, _ in topics:
        assert topic not in inels_mqtt._InelsMqtt__is_subscribed_list
        assert topic not in inels_mqtt._InelsMqtt__expected_mid


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


def test_unsubscribe_success(mqtt_client_mock, inels_mqtt):
    """Test successful unsubscribe."""
    topic = "inels/status/10e97f8b7d30/01/01E8"
    inels_mqtt._InelsMqtt__is_subscribed_list = {topic: True}
    inels_mqtt._InelsMqtt__expected_mid = {topic: 1}
    inels_mqtt._InelsMqtt__timeout = 0.01

    mqtt_client_mock.unsubscribe.return_value = (mqtt.MQTT_ERR_SUCCESS, 1)

    # Simulate the behavior of __on_unsubscribe
    def wait_for_side_effect(condition_func, timeout):
        inels_mqtt._InelsMqtt__is_subscribed_list.pop(topic, None)
        inels_mqtt._InelsMqtt__expected_mid.pop(topic, None)

    inels_mqtt._InelsMqtt__subscription_condition.wait_for = wait_for_side_effect

    inels_mqtt.unsubscribe(topic)

    mqtt_client_mock.unsubscribe.assert_called_once_with(topic)

    assert topic not in inels_mqtt._InelsMqtt__is_subscribed_list
    assert topic not in inels_mqtt._InelsMqtt__expected_mid


def test_unsubscribe_nonexistent_topic(mqtt_client_mock, inels_mqtt):
    """Test unsubscribe edge cases."""
    inels_mqtt._InelsMqtt__is_subscribed_list = {}

    inels_mqtt.unsubscribe("non_existent_topic")

    mqtt_client_mock.unsubscribe.assert_not_called()
