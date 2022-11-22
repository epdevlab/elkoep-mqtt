"""Inels configurations."""
from __future__ import annotations
from typing import Awaitable, Callable, Any

import attr

from .mqtt_client import InelsMqttClient, GetMessage


@attr.s(slots=True, frozen=True)
class EntityConfig:
    """It is base config for all entities."""

    name: str = attr.ib()
    uid: str = attr.ib()
    pid: str = attr.ib()
    type: str = attr.ib()
    payload: str = attr.ib()
    state_topic: str = attr.ib()
    set_topic: str = attr.ib()
    platform: str = attr.ib()

    @property
    def unique_id(self) -> str:
        """Generate unique id from default properties."""
        return f"{self.pid}_{self.type}_{self.uid}"


@attr.s(slots=True, frozen=True)
class AvailabilityConfig(EntityConfig):
    """Availability configuration setup."""

    available_state_topic: str = attr.ib()


class InelsEntity:
    """Base class."""

    def __init__(self, cfg: EntityConfig, mqtt: InelsMqttClient) -> None:
        """Initialize entity."""
        self._cfg = cfg
        self._mqtt = mqtt
        self._state_callback: Callable | None = None
        super().__init__()

    @property
    def name(self) -> str:
        """Entity name."""
        return self._cfg.name

    @property
    def unique_id(self) -> str:
        """Entity unique id."""
        return self._cfg.unique_id

    @property
    def parent_id(self) -> str | None:
        """Parent id if exists."""
        return self._cfg.pid

    @property
    def platform(self) -> str:
        """Platform."""
        return self._cfg.platform

    def set_state_callback(self, callback: Callable) -> None:
        """Callback state change."""
        self._state_callback = callback

    def is_config_same(self, cfg: EntityConfig) -> bool:
        """Check if config is same as updated one."""
        return self._cfg == cfg

    def set_config(self, cfg: EntityConfig) -> None:
        """Update config to new one."""
        self._cfg = cfg

    async def poll_status(self) -> None:
        """Send status."""
        await self._mqtt.publish_with_delay(self._cfg.set_topic, self._cfg.payload)

    async def subscribe(self) -> None:
        """Subscribe."""

    async def unsubscribe(self) -> None:
        """Unsubscribe."""


class InelsAvailability(InelsEntity):
    """Availability class for Inels entities."""

    _config: AvailabilityConfig

    def __init__(self, **kwargs: Any) -> None:
        """Initialize available class."""
        self._availability_callback: Awaitable | None = None
        super().__init__(**kwargs)

    def set_availability_callback(self, callback: Callable) -> None:
        """Set callback for availablity."""
        self._availability_callback = callback

    def get_availability_topic(self) -> str:
        """Get all available topic for entity."""

        async def message_received(msg: GetMessage) -> None:
            """Get a mqtt message."""

            if msg.payload == self._config.available_state_topic:
                await self.poll_status()
            if not self._availability_callback:
                return
            if msg.payload == self._config.available_state_topic:
                await self._availability_callback(True)
            else:
                await self._availability_callback(False)

        # determine dictionary but send only one topic
        # this is neccessary because of mqtt library subscribing fnc
        topics = {
            "availability_topic": {
                "evnet_loop_safe": True,
                "callback": message_received,
                "topic": self._config.available_state_topic,
            }
        }

        return topics
