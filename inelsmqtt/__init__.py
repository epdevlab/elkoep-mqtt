"""Library specified for inels-mqtt."""
from collections import defaultdict
import logging
import time
import uuid
import copy

from datetime import datetime
from typing import Any, Callable

import paho.mqtt.client as mqtt

from .const import (
    MQTT_CLIENT_ID,
    MQTT_HOST,
    MQTT_PASSWORD,
    MQTT_PORT,
    MQTT_TIMEOUT,
    MQTT_TRANSPORT,
    MQTT_USERNAME,
    MQTT_PROTOCOL,
    MQTT_TRANSPORTS,
    VERSION,
    DEVICE_TYPE_DICT,
    FRAGMENT_DEVICE_TYPE,
    FRAGMENT_STATE,
    TOPIC_FRAGMENTS,
    DISCOVERY_TIMEOUT_IN_SEC,
    MQTT_DISCOVER_TOPIC,
)

__version__ = VERSION

_LOGGER = logging.getLogger(__name__)

# when no topic were detected, then stop discovery
__DISCOVERY_TIMEOUT__ = DISCOVERY_TIMEOUT_IN_SEC


class InelsMqtt:
    """Wrapper for mqtt client."""

    def __init__(
        self,
        config: dict[str, Any],
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
        proto = (
            config.get(MQTT_PROTOCOL) if config.get(MQTT_PROTOCOL) else mqtt.MQTTv311
        )

        _t: str = (
            config.get(MQTT_TRANSPORT) if config.get(MQTT_TRANSPORT) else "tcp"
        ).lower()

        if _t not in MQTT_TRANSPORTS:
            raise Exception

        if (client_id := config.get(MQTT_CLIENT_ID)) is None:
            client_id = mqtt.base62(uuid.uuid4().int, padding=22)

        self.__client = mqtt.Client(client_id, protocol=proto, transport=_t)

        self.__client.on_connect = self.__on_connect
        self.client.on_publish = self.__on_publish
        self.client.on_subscribe = self.__on_subscribe
        self.client.on_disconnect = self.__on_disconnect

        self.__client.enable_logger()

        u_name = config.get(MQTT_USERNAME)
        u_pwd = config.get(MQTT_PASSWORD)

        if u_name is not None:
            self.__client.username_pw_set(u_name, u_pwd)

        self.__host = config[MQTT_HOST]
        self.__port = config[MQTT_PORT]

        _t = config.get(MQTT_TIMEOUT)
        self.__timeout = _t if _t is not None else __DISCOVERY_TIMEOUT__

        self.__listeners : dict[str, dict[str, Callable[[Any], Any]]] = defaultdict(lambda: dict())
        self.__is_subscribed_list = dict[str, bool]()
        self.__last_values = dict[str, str]()
        self.__try_connect = False
        self.__message_readed = False
        self.__messages = dict[str, str]()
        self.__discovered = dict[str, str]()
        self.__is_available = False
        self.__discover_start_time = None
        self.__published = False

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

    def is_subscribed(self, topic) -> bool:
        """Get info if the topic is subscribed in device

        Returns:
            bool: state
        """
        is_subscribed = self.__is_subscribed_list.get(topic)
        return False if is_subscribed is None else is_subscribed

    def last_value(self, topic) -> str:
        """Get last value of the selected topic

        Args:
            topic (str): topic name

        Returns:
            str: last value of the topic
        """
        return self.__last_values.get(topic)

    def messages(self) -> dict[str, str]:
        """List of all messages

        Returns:
            dist[str, str]: List of all messages (topics)
            from broker subscribed.
            It is key-value dictionary. Key is topic and value
            is payload of topic
        """
        return self.__messages

    def test_connection(self) -> bool:
        """Test connection. It's used only for connection
            testing. After that is disconnected
        Returns:
            bool: Is broker available or not
        """
        self.__connect()
        self.disconnect()

        return self.__is_available

    def subscribe_listener(self, topic: str, unique_id: str, fnc: Callable[[Any], Any]) -> None:
        """Append new item into the datachange listener."""
        #if topic not in self.__listeners:
        #    self.__listeners[topic] = dict[str, Callable[[Any], Any]]()
        self.__listeners[topic][unique_id] = fnc

    def unsubscribe_listeners(self) -> bool:
        """Unsubscribe listeners."""
        self.__listeners.clear()

    def __connect(self) -> None:
        """Create connection and register callback function to neccessary
        purposes.
        """
        if self.__client.is_connected() is False:
            _LOGGER.warning("Host: %s, Port: %s\n", self.__host, self.__port)
            
            self.__client.connect(self.__host, self.__port)
            self.__client.loop_start()

        start_time = datetime.now()

        while self.__try_connect is False:
            # there should be timeout to discover all topics
            time_delta = datetime.now() - start_time
            if time_delta.total_seconds() > self.__timeout:
                self.__try_connect = self.__is_available = False
                break

            time.sleep(0.1)

    def __on_disconnect(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata,  # pylint: disable=unused-argument
        reason_code,
    ) -> None:
        """On disconnect callback function

        Args:
            client (mqtt.Client): instance of the mqtt client
            userdata (Any): users data
            reason_code (number): reason code
        """
        _LOGGER.info("%s - disconnecting reason [%s]", self.__host, reason_code)

        for item in self.__is_subscribed_list.keys():
            self.__is_subscribed_list[item] = False
            _LOGGER.info("Disconnected %s", item)

    def __on_connect(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata,  # pylint: disable=unused-argument
        flag,  # pylint: disable=unused-argument
        reason_code,
        properties=None,  # pylint: disable=unused-argument
    ) -> None:
        """On connection callback function

        Args:
            client (MqttClient): instance of mqtt client
            properties (_type_, optional): Props from mqtt sets. Defaults None
        """
        self.__try_connect = True
        self.__is_available = reason_code == mqtt.CONNACK_ACCEPTED
        _LOGGER.info(
            "Mqtt broker %s:%s %s",
            self.__host,
            self.__port,
            "is connected" if self.__is_available else "is not connected",
        )

    def publish(self, topic, payload, qos=0, retain=True, properties=None) -> bool:
        """Publish to mqtt broker. Will automatically connect
        establish all neccessary callback functions. Made
        publishing and disconnect from broker

        Args:
            topic (str): topic string where to publish
            payload (str): data content
            qos (int, optional): quality of service
              https://mosquitto.org/man/mqtt-7.html. Defaults to 0.
            retain (bool, optional): Broke will keep message after sending it
              to all subscribers. Defaults to True.
            properties (_type_, optional): Props from mqtt sets.
              Defaults to None.
        """
        self.__published = False
        self.__connect()
        self.client.publish(topic, payload, qos, retain, properties)

        start_time = datetime.now()

        while self.__published is False:
            # there should be timeout to discover all topics
            time_delta = datetime.now() - start_time
            if time_delta.total_seconds() > self.__timeout:
                self.__published = False
                break

            time.sleep(0.1)

        return self.__published

    def __on_publish(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata,  # pylint: disable=unused-argument
        mid,  # pylint: disable=unused-argument
    ) -> None:
        """Callback function called after publish
          has been created. Will log it.

        Args:
            client (MqttClient): Instance of mqtt broker
            userdata (object): Published data
            mid (_type_): MID
        """
        self.__published = True

    def subscribe(self, topic, qos=0, options=None, properties=None) -> Any:
        """Subscribe to selected topic. Will connect, set all
        callback function and subscribe to the topic. After that
        will automatically disconnect from broker.

        Args:
            topic (str): Topic string representation
            qos (_type_): Quality of service.
            options (_type_): Options is not used, but callback must
              have implemented
            properties (_type_, optional): Props from mqtt set.
              Defaults to None.
        """
        self.__message_readed = False
        self.client.on_message = self.__on_message

        self.__connect()
        self.client.subscribe(topic, qos, options, properties)

        start_time = datetime.now()

        while self.__message_readed is False:
            # there should be timeout to discover all topics
            time_delta = datetime.now() - start_time
            if time_delta.total_seconds() > self.__timeout:
                self.__message_readed = False
                break

            time.sleep(0.1)

        return self.__messages.get(topic)

    def discovery_all(self) -> "dict[str, str]":
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
        self.client.subscribe(MQTT_DISCOVER_TOPIC, 0, None, None)

        self.__discover_start_time = datetime.now()

        while True:
            # there should be timeout to discover all topics
            time_delta = datetime.now() - self.__discover_start_time
            if time_delta.total_seconds() > self.__timeout:
                break

            time.sleep(0.1)

        self.__messages = self.__discovered.copy()

        #_LOGGER.info("Found %s devices", self.__discovered.__len__)
        return self.__discovered

    def __on_discover(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata,  # pylint: disable=unused-argument
        msg,
    ) -> None:
        """Special callback function used only in discover_all function
        placed in on_message. It is the same as on_message callback func,
        but does different things
        
        Args:
            client (MqttClient): Mqtt broker instance
            msg (object): Topic with payload from broker
        """
        _LOGGER.info("Found device from topic %s\n", msg.topic)
        # set discovery_start_time to now every message was returned
        # will be doing till messages will rising
        #if self.__discovered.get(msg.topic) is None:
            #_LOGGER.info("Message: %s", str(self.__discovered[msg.topic]))
            #_LOGGER.info("First time getting topic %s", msg.topic)
            #self.__discover_start_time = datetime.now()

        # pass only those who belongs to known device types
        fragments = msg.topic.split("/")
        device_type = fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]
        status = fragments[TOPIC_FRAGMENTS[FRAGMENT_STATE]]

        if device_type in DEVICE_TYPE_DICT and status == "status":
            self.__discovered[msg.topic] = msg.payload
            self.__last_values[msg.topic] = msg.payload
            self.__is_subscribed_list[msg.topic] = True
            _LOGGER.info("Device of type %s found.\n", device_type)
            
    def __on_message(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata,  # pylint: disable=unused-argument
        msg,
    ) -> None:
        """Callback function which is used for subscription

        Args:
            client (MqttClient): Instance of mqtt broker
            userdata (_type_): Date about user
            msg (object): Topic with payload from broker
        """
        self.__message_readed = True
        device_type = msg.topic.split("/")[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]

        if device_type in DEVICE_TYPE_DICT:
            # keep last value
            self.__last_values[msg.topic] = (
                copy.copy(self.__messages[msg.topic])
                if msg.topic in self.__messages
                else msg.payload
            )
            self.__messages[msg.topic] = msg.payload
            # update info that the topic is subscribed
            self.__is_subscribed_list[msg.topic] = True

        if len(self.__listeners) > 0 and msg.topic in self.__listeners:
            # This pass data change directely into the device.
            if len(self.__listeners[msg.topic]) > 0:
                for unique_id in list(self.__listeners[msg.topic]): #prevents the dictionary increased in size during iteration exception
                    self.__listeners[msg.topic][unique_id](msg.payload)
            

    def __on_subscribe(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata,  # pylint: disable=unused-argument
        mid,  # pylint: disable=unused-argument
        granted_qos,  # pylint: disable=unused-argument
        properties=None,  # pylint: disable=unused-argument
    ):
        """Callback for subscribe function. Is called after subscribe to
        the topic. Will handle disconnection from mqtt broker loop

        Args:
            client (MqttClient): Instance of mqtt broker
            userdata (_type_): Data about user
            mid (_type_): MID
            granted_qos (_type_): Quality of service is granted
            properties (_type_, optional): Props from broker set.
                Defaults to None.
        """
        _LOGGER.info(mid)

    def __disconnect(self) -> None:
        """Disconnecting from broker and stopping broker's loop"""
        self.close()
        self.client.disconnect()

    def close(self) -> None:
        """Close loop."""
        self.client.loop_stop()

    def disconnect(self) -> None:
        """Disconnect mqtt client."""
        return self.__disconnect()
