"""Switch device."""
from __future__ import annotations

from typing import Any
import attr

from inelsmqtt.config import (
    AvailabilityConfig,
    EntityConfig,
    InelsEntity,
    InelsAvailability,
)
from inelsmqtt.mqtt_client import GetMessage
from inelsmqtt.util import get_name, get_set_topic, get_state_topic, get_value


@attr.s(slots=True, frozen=True)
class InelsSwitchConfig(AvailabilityConfig, EntityConfig):
    """Inels configuration for switch."""

    @classmethod
    def discovery_message(
        cls, cfg: dict, uid: int, platform: str
    ) -> InelsSwitchConfig | None:
        """Data from discovery."""

        return cls(
            uid=uid,
            platform=platform,
            set_topic=get_set_topic(cfg),
            state_topic=get_state_topic(cfg),
            name=get_name(cfg),
        )


class InelsSwitch(InelsAvailability, InelsEntity):
    """Inels switch."""

    _cfg: InelsSwitchConfig

    def __init__(self, **kwards: Any) -> None:
        """Initilize switch."""
        self._state: dict | None = None
        super().__init__(**kwards)

    async def subscribe(self) -> None:
        """Subscribe."""

        def message(msg: GetMessage) -> None:
            """Mqtt message."""
            if not self._state_callback:
                return

            state: bool | None = None
            if msg.topic == self._cfg.state_topic:
                state = get_value(msg.payload, self._cfg.platform)

            if state is not None:
                self._state_callback(state)

        availability = self.get_availability_topic()

        topics = {
            "state_topic": {
                "event_loop_safe": True,
                "topic": self._cfg.state_topic,
                "msg_callback": message,
            }
        }

        topics = {**topics, **availability}

        self._state = await self._mqtt.subscribe(self._state, topics)

    async def unsubscribe(self) -> None:
        """Unsubscribe."""
        self._state = await self._mqtt.unsubscribe(self._state)
