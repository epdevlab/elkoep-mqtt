"""Library specified for inels-mqtt."""

import copy
import logging
import threading
import time
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

import paho.mqtt.client as mqtt
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from inelsmqtt.const import GATEWAY
from inelsmqtt.utils.core import ProtocolHandlerMapper

from .const import (
    DISCOVERY_TIMEOUT_IN_SEC,
    FRAGMENT_DEVICE_TYPE,
    FRAGMENT_STATE,
    MQTT_CLIENT_ID,
    MQTT_HOST,
    MQTT_PASSWORD,
    MQTT_PORT,
    MQTT_PROTOCOL,
    MQTT_STATUS_TOPIC_PREFIX,
    MQTT_TIMEOUT,
    MQTT_TOTAL_CONNECTED_TOPIC,
    MQTT_TOTAL_STATUS_TOPIC,
    MQTT_TRANSPORT,
    MQTT_TRANSPORTS,
    MQTT_USERNAME,
    TOPIC_FRAGMENTS,
    VERSION,
)

__version__ = VERSION

_LOGGER = logging.getLogger(__name__)

# when no topic were detected, then stop discovery
__DISCOVERY_TIMEOUT__ = DISCOVERY_TIMEOUT_IN_SEC


class InelsMqtt:
    """Wrapper for mqtt client."""

    def __init__(
        self,
        config: dict,
    ) -> None:
        """InelsMqtt instance initialization.

        Args:
            config dict[str, Any]: config for mqtt connection
            host (str): mqtt broker host. Can be IP address
            port (int): broker port on which listening
            protocol (int): mqtt version of protocol whitch will be used
            transport (str): transportation protocol. Can be used tcp or websockets, defaltut tcp
            debug (bool): flag for debuging mqtt comunication. Default False
        """
        self.__proto = config.get(MQTT_PROTOCOL) if config.get(MQTT_PROTOCOL) else mqtt.MQTTv311

        _t: str = (config.get(MQTT_TRANSPORT) or "tcp").lower()

        if _t not in MQTT_TRANSPORTS:
            raise Exception

        if (client_id := config.get(MQTT_CLIENT_ID)) is None:
            client_id = mqtt.base62(uuid.uuid4().int, padding=22)

        self.__client = mqtt.Client(client_id, protocol=self.__proto, transport=_t)

        self.__client.on_connect = self.__on_connect
        self.__client.on_subscribe = self.__on_subscribe
        self.__client.on_unsubscribe = self.__on_unsubscribe
        self.__client.on_disconnect = self.__on_disconnect
        self.__connection_error: Optional[int] = None
        self.__client.enable_logger()

        u_name = config.get(MQTT_USERNAME)
        u_pwd = config.get(MQTT_PASSWORD)

        if u_name is not None:
            self.__client.username_pw_set(u_name, u_pwd)

        self.__host = config[MQTT_HOST]
        self.__port = config[MQTT_PORT]

        self.__timeout: int = config.get(MQTT_TIMEOUT, __DISCOVERY_TIMEOUT__)

        self.__listeners: dict[str, dict[str, Callable[[Any], Any]]] = defaultdict(lambda: dict())
        self.__is_subscribed_list = dict[str, bool]()
        self.__last_values = dict[str, str]()
        self.__try_connect = False
        self.__messages = dict[str, Optional[str]]()
        self.__discovered = dict[str, Optional[str]]()
        self.__is_available = False
        self.__discover_start_time: Optional[datetime] = None

        self.__expected_mid = dict[str, int]()
        self.__subscription_condition = threading.Condition()
        self.__lock = threading.Lock()

    @property
    def client(self) -> mqtt.Client:
        """Paho mqtt client."""
        return self.__client

    @property
    def is_available(self) -> bool:
        """Is broker available

        Returns:
            bool: Get information of mqtt broker availability
        """
        return self.__is_available

    @property
    def list_of_listeners(self) -> dict[str, dict[str, Callable[[Any], Any]]]:
        """List of listeners."""
        return self.__listeners

    @property
    def subscribed_topics_status(self) -> dict[str, bool]:
        """Get all subscribed topics and their subscription status.

        Returns:
            dict[str, bool]: Dictionary with topics as keys and subscription status as values.
        """
        return self.__is_subscribed_list

    @property
    def expected_mid(self) -> dict[str, int]:
        """Get the expected message IDs for subscribed topics.

        Returns:
            dict[str, int]: Dictionary with topics as keys and expected message IDs as values.
        """
        return self.__expected_mid

    @property
    def connection_error(self) -> Optional[int]:
        return self.__connection_error

    def is_subscribed(self, topic: str) -> bool:
        """Get info if the topic is subscribed in device

        Returns:
            bool: state
        """
        is_subscribed = self.__is_subscribed_list.get(topic)
        return False if is_subscribed is None else is_subscribed

    def last_value(self, topic: str) -> Optional[str]:
        """Get last value of the selected topic

        Args:
            topic (str): topic name

        Returns:
            Optional[str]: last value of the topic, or None if not found
        """
        return self.__last_values.get(topic)

    def messages(self) -> dict[str, Optional[str]]:
        """List of all messages

        Returns:
            dict[str, Optional[str]]: List of all messages (topics)
            from broker subscribed.
            It is key-value dictionary. Key is topic and value
            is payload of topic
        """
        return self.__messages

    def test_connection(self) -> Optional[int]:
        """Test connection. It's used only for connection
            testing. After that is disconnected
        Returns:
            bool: Is broker available or not
        """
        try:
            self.__connect()
            self.disconnect()
        except Exception as e:
            if isinstance(e, ConnectionRefusedError):
                self.__connection_error = 3  # cannot connect
            else:
                self.__connection_error = 6  # unknown

        return self.__connection_error

    def subscribe_listener(self, topic: str, unique_id: str, fnc: Callable[[Any], Any]) -> None:
        """Append new item into the datachange listener."""
        # if topic not in self.__listeners:
        #    self.__listeners[topic] = dict[str, Callable[[Any], Any]]()

        stripped_topic = "/".join(topic.split("/")[2:])
        self.__listeners[stripped_topic][unique_id] = fnc

    def unsubscribe_listeners(self) -> None:
        """Unsubscribe listeners."""
        self.__listeners.clear()

    def __connect(self) -> None:
        """Create connection and register callback function to necessary
        purposes.
        """
        if not self.__client.is_connected():
            try:
                if self.__proto == 5:
                    properties = Properties(PacketTypes.CONNECT)
                    properties.SessionExpiryInterval = 3600  # in seconds
                    self.__client.connect(
                        self.__host,
                        self.__port,
                        clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                        properties=properties,
                        keepalive=60,
                    )
                else:
                    self.__client.connect(self.__host, self.__port, keepalive=60)
                self.__client.loop_start()
            except Exception as e:
                _LOGGER.error("Failed to connect to MQTT broker: %s", e)
                raise

        start_time = datetime.now()

        while self.__try_connect is False:
            time_delta = datetime.now() - start_time
            if time_delta.total_seconds() > self.__timeout:
                _LOGGER.error("Connection attempt timed out")
                self.__try_connect = self.__is_available = False
                break

            time.sleep(0.1)

    def __on_disconnect(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata: Any,  # pylint: disable=unused-argument
        reason_code: int,
        properties: Optional[Properties] = None,
    ) -> None:
        """On disconnect callback function

        Args:
            client (mqtt.Client): instance of the mqtt client
            userdata (Any): user's data
            reason_code (int): reason code for disconnection
            properties (Optional[Properties]): MQTT v5 properties
        """
        _LOGGER.warning("%s - disconnecting reason [%s]", self.__host, reason_code)

        self.__is_available = False
        self.__try_connect = False

        for item in self.__is_subscribed_list.keys():
            self.__is_subscribed_list[item] = False
            _LOGGER.info("Disconnected %s", item)

        # Notify any condition variables waiting on __expected_mid
        with self.__subscription_condition:
            self.__subscription_condition.notify_all()

    def __on_connect(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata: Any,  # pylint: disable=unused-argument
        flags: dict,
        reason_code: int,
        properties: Optional[Properties] = None,  # pylint: disable=unused-argument
    ) -> None:
        """On connection callback function

        Args:
            client (mqtt.Client): instance of mqtt client
            userdata (Any): user data as set in Client() or user_data_set()
            flags (dict): response flags sent by the broker
            reason_code (int): the connection result
            properties (Optional[Properties]): the MQTT v5 properties returned from the broker
        """
        self.__try_connect = True
        if reason_code == mqtt.CONNACK_ACCEPTED:
            self.__is_available = True
            self.__connection_error = None
        else:
            self.__is_available = False
            self.__connection_error = reason_code

        _LOGGER.info(
            "Mqtt broker %s:%s %s",
            self.__host,
            self.__port,
            "is connected" if self.__is_available else "is not connected",
        )

    def publish(
        self, topic: str, payload: Any, qos: int = 0, retain: bool = True, properties: Optional[Properties] = None
    ) -> bool:
        """
        Publish a message to a specified MQTT topic.

        Args:
            topic (str): The topic to publish to.
            payload (Any): The message payload.
            qos (int, optional): The Quality of Service level. Defaults to 0.
            retain (bool, optional): If True, the message will be retained. Defaults to True.
            properties (Any, optional): Additional properties for the message. Defaults to None.

        Returns:
            bool: True if the message was published successfully, False otherwise.
        """
        self.__connect()
        info = self.client.publish(topic, payload, qos, retain, properties)

        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            _LOGGER.error("Could not publish message to topic %s, error code: %d", topic, info.rc)
            return False

        try:
            # Wait for the message to be published if it hasn't been already
            if not info.is_published():
                info.wait_for_publish(timeout=self.__timeout)
        except Exception as e:
            _LOGGER.error("Exception occurred while waiting for publish to topic %s: %s", topic, e)
            return False
        else:
            return True

    def subscribe(
        self,
        topics: Union[str, List[str], List[Tuple[str, int]]],
        qos: int = 0,
        options: Optional[Any] = None,
        properties: Optional[Any] = None,
    ) -> Dict[str, Optional[str]]:
        """Subscribe to selected topics.

        Args:
            topics (Union[str, List[str], List[Tuple[str, int]]]): Topic string representation, list of topics, or list of (topic, qos) tuples.
            qos (int, optional): Quality of service. Defaults to 0.
            options (Optional[Any], optional): Options is not used, but callback must
              have implemented. Defaults to None.
            properties (Optional[Any], optional): Props from mqtt set. Defaults to None.

        Returns:
            Dict[str, Optional[str]]: Dictionary of messages for the subscribed topics.
        """
        with self.__lock:
            if isinstance(topics, str):
                topics = [(topics, qos)]
            elif isinstance(topics, list) and all(isinstance(t, str) for t in topics):
                topics = [(t, qos) for t in topics]  # type: ignore

            # Ensure topics is now List[Tuple[str, int]]
            topics = cast(List[Tuple[str, int]], topics)

            self.__connect()

            filtered_topics = []
            for t, q in topics:
                if not self.__is_subscribed_list.get(t, False):
                    self.__is_subscribed_list[t] = False
                    filtered_topics.append((t, q))

            if filtered_topics:
                r, mid = self.__client.subscribe(filtered_topics, options, properties)
                if r != mqtt.MQTT_ERR_SUCCESS:
                    _LOGGER.error("Failed to subscribe to topics: %s", filtered_topics)
                    # Clean up the state for failed subscriptions
                    for topic, _ in filtered_topics:
                        self.__is_subscribed_list.pop(topic, None)
                    return {}

                for topic, _ in filtered_topics:
                    self.__expected_mid[topic] = mid

                with self.__subscription_condition:
                    self.__subscription_condition.wait_for(
                        lambda: not self.__expected_mid.get(topic), timeout=self.__timeout
                    )

        for topic, _ in filtered_topics:
            if not self.__is_subscribed_list[topic]:
                _LOGGER.error("Subscription to topic %s failed", topic)
                self.__expected_mid.pop(topic, None)
                self.__is_subscribed_list.pop(topic, None)

        return {topic: self.__messages.get(topic) for topic, _ in topics}

    def __on_subscribe(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata: Any,  # pylint: disable=unused-argument
        mid: int,  # pylint: disable=unused-argument
        granted_qos: List[int],  # pylint: disable=unused-argument
        properties: Optional[Any] = None,  # pylint: disable=unused-argument
    ) -> None:
        """Callback for subscribe function."""
        topics_to_delete = []
        for topic, expected_mid in self.__expected_mid.items():
            if mid == expected_mid:
                topics_to_delete.append(topic)
                self.__is_subscribed_list[topic] = True
                _LOGGER.info("Successfully subscribed to topic: %s", topic)

        for topic in topics_to_delete:
            del self.__expected_mid[topic]

        with self.__subscription_condition:
            self.__subscription_condition.notify_all()

    def __on_unsubscribe(
        self,
        client: mqtt.Client,
        userdata: Any,
        mid: int,
        properties: Optional[Any] = None,
        reasoncodes: Optional[List[int]] = None,
    ) -> None:
        """Callback for when the client receives an UNSUBACK response from the broker."""
        topic_to_remove = None
        for topic, expected_mid in self.__expected_mid.items():
            if expected_mid == mid:
                self.__is_subscribed_list.pop(topic, None)
                self.__messages.pop(topic, None)
                topic_to_remove = topic
                break

        if topic_to_remove:
            del self.__expected_mid[topic_to_remove]
            _LOGGER.info("Successfully unsubscribed from topic %s", topic_to_remove)

        with self.__subscription_condition:
            self.__subscription_condition.notify_all()

    def unsubscribe(self, topic: str) -> None:
        """Unsubscribe from a selected topic.

        Args:
            topic (str): Topic string representation.
        """
        with self.__lock:
            self.__connect()
            if self.__is_subscribed_list.get(topic, False):
                r, mid = self.client.unsubscribe(topic)
                if r != mqtt.MQTT_ERR_SUCCESS:
                    _LOGGER.error("Failed to unsubscribe from topic: %s", topic)
                    return

                self.__expected_mid[topic] = mid

                with self.__subscription_condition:
                    self.__subscription_condition.wait_for(
                        lambda: not self.__expected_mid.get(topic), timeout=self.__timeout
                    )

        if self.__is_subscribed_list.get(topic):
            _LOGGER.error("Unsubscription from topic %s failed", topic)

    def discovery_all(self) -> dict[str, Optional[str]]:
        """Subscribe to selected topic. This method is primary used for
        subscribing with wild-card (#,+).
        When wild-card is used, then all topic matching this will
        be subscribed and collected therir payloads and topic representation.

        e.g.: prefix/status/groundfloor/# - will match all groundfloor topics
                    prefix/status/groundfloor/kitchen/temp - yes
                    prefix/status/groundfloor/livingroom/temp - yes
                    prefix/status/firstfloor/bathroom/temp - no
                    prefix/status/groundfloor/kitchen/fridge/temp - yes

              prefix/status/groundfoor/+/temp - will get all groundfloor temp
                    prefix/status/groundfloor/kitchen/temp - yes
                    prefix/status/groundfloor/kitchen/lamp - no
                    prefix/status/groundfloor/livingroom/temp - yes
                    prefix/status/groundfloor/kitchen/fridge/temp - no

        Returns:
            dict[str, str]: Dictionary of all topics with their payloads
        """
        self.client.on_message = self.__on_discover
        self.__connect()

        topics_to_subscribe = [MQTT_TOTAL_CONNECTED_TOPIC, MQTT_TOTAL_STATUS_TOPIC]
        self.subscribe(topics_to_subscribe, qos=0)

        self.__discover_start_time = datetime.now()

        while (datetime.now() - self.__discover_start_time).total_seconds() <= self.__timeout:
            time.sleep(0.1)

        for t in self.__discovered:
            self.__messages[MQTT_STATUS_TOPIC_PREFIX + t] = self.__discovered[t]

        self.unsubscribe(MQTT_TOTAL_CONNECTED_TOPIC)
        self.unsubscribe(MQTT_TOTAL_STATUS_TOPIC)
        self.client.on_message = self.__on_message

        return self.__discovered

    def __on_discover(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata: Any,  # pylint: disable=unused-argument
        msg: mqtt.MQTTMessage,
    ) -> None:
        """Special callback function used only in discover_all function
        placed in on_message. It is the same as on_message callback func,
        but does different things

        Args:
            client (mqtt.Client): Mqtt broker instance
            userdata (Any): User data (unused)
            msg (mqtt.MQTTMessage): Message received from broker
        """
        _LOGGER.info("Found device from topic %s\n", msg.topic)

        # pass only those who belong to known device types
        fragments = msg.topic.split("/")
        device_type = fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]
        action = fragments[TOPIC_FRAGMENTS[FRAGMENT_STATE]]

        topic = msg.topic.split("/")[2:]
        topic = "/".join(topic)

        if device_type in ProtocolHandlerMapper.DEVICE_TYPE_MAP:
            if action == "status":
                self.__discovered[topic] = msg.payload
                self.__last_values[msg.topic] = msg.payload
                _LOGGER.info("Device of type %s found [status].\n", device_type)
            elif action == "connected":
                if topic not in self.__discovered:
                    # Setting to None ensures that it is tracked even if its status message is not received. It will be used for COM_TEST.
                    self.__discovered[topic] = None
                    self.__last_values[msg.topic] = msg.payload
                _LOGGER.info("Device of type %s found [connected].\n", device_type)
        else:
            if device_type == "gw" and action == "connected":
                if msg.topic not in self.__discovered:
                    self.__discovered[msg.topic] = GATEWAY
                    self.__last_values[msg.topic] = msg.payload
                    _LOGGER.info("Device of type %s found [gw].\n", device_type)
            elif device_type != "gw":
                _LOGGER.error("No handler found for device_type: %s", device_type)

    def __on_message(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata: Any,  # pylint: disable=unused-argument
        msg: mqtt.MQTTMessage,
    ) -> None:
        """Callback function which is used for subscription

        Args:
            client (mqtt.Client): Instance of mqtt broker
            userdata (Any): Data about user
            msg (mqtt.MQTTMessage): Topic with payload from broker
        """
        message_parts = msg.topic.split("/")
        device_type = message_parts[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]

        message_type = message_parts[TOPIC_FRAGMENTS[FRAGMENT_STATE]]

        if device_type in ProtocolHandlerMapper.DEVICE_TYPE_MAP or device_type == "gw":
            # keep last value
            self.__last_values[msg.topic] = (
                copy.copy(self.__messages[msg.topic]) if msg.topic in self.__messages else msg.payload
            )
            self.__messages[msg.topic] = msg.payload

        if device_type == "gw" and message_type == "connected":
            mac = message_parts[2]
            for stripped_topic in self.__listeners:
                if stripped_topic.startswith(mac):
                    self.__notify_listeners(stripped_topic, True)
            return

        stripped_topic = "/".join(message_parts[2:])

        is_connected_message = message_type == "connected"

        if len(self.__listeners) > 0 and stripped_topic in self.__listeners:
            # This pass data change directely into the device.
            self.__notify_listeners(stripped_topic, is_connected_message)

    def __notify_listeners(self, stripped_topic: str, is_connected_message: bool) -> None:
        """Notify listeners for a specific topic."""
        if len(self.__listeners[stripped_topic]) > 0:
            for unique_id in list(
                self.__listeners[stripped_topic]
            ):  # prevents the dictionary increased in size during iteration exception
                self.__listeners[stripped_topic][unique_id](is_connected_message)

    def __disconnect(self) -> None:
        """Disconnecting from broker and stopping broker's loop"""
        self.client.disconnect()
        self.close()

    def close(self) -> None:
        """Close loop."""
        _LOGGER.warning("Close called from HA")

        self.__is_available = False

        # Notify any condition variables waiting on __expected_mid
        with self.__subscription_condition:
            self.__subscription_condition.notify_all()

        self.client.loop_stop()

    def disconnect(self) -> None:
        """Disconnect mqtt client."""
        return self.__disconnect()
