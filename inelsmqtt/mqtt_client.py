"""Inels MQTT client."""
from __future__ import annotations

import logging
from typing import Union, Callable, Awaitable
import asyncio
import attr

_LOGGER = logging.getLogger(__name__)

SendMessageType = Union[str, bytes, int, float, None]
GetMessageType = Union[str, bytes]


@attr.s(slots=True, frozen=True)
class SendMessage:
    """Class with definition of sending message."""

    payload: SendMessageType = attr.ib()
    topic: str = attr.ib()
    retain: bool | None = attr.ib()
    qos: int | None = attr.ib()


@attr.s(slots=True, frozen=True)
class GetMessage:
    """Class with definition of geting message."""

    payload: GetMessageType = attr.ib()
    topic: str = attr.ib()
    retain: bool | None = attr.ib()
    qos: int | None = attr.ib()


class InelsTimer:
    """Timing messages."""

    def __init__(self, tout: float, callback: Callable[[], None]) -> None:
        """Initializing timer."""
        self._tout = tout
        self._callback = callback
        self._t = asyncio.ensure_future(self._task())

    async def _task(self) -> None:
        """Call callback fnc as a task."""
        await asyncio.sleep(self._tout)
        await self._callback()

    def stop(self) -> None:
        """Stop the timer."""
        self._t.cancel()


class InelsMqttClient:
    """Wrapp external mqtt client."""

    def __init__(
        self,
        sub: Callable[[dict | None, dict], Awaitable[dict]],
        un_sub: Callable[[dict | None], Awaitable[dict]],
        pub: Callable[[str, SendMessageType, int | None, bool | None], None],
    ) -> None:
        """Initialize client"""
        self._pub = pub
        self._sub = sub
        self._un_sub = un_sub
        self._pending_msg: dict[SendMessage, InelsTimer] = {}
        _LOGGER.debug("Initialize MQTT client.")

    async def subscribe(self, state: dict | None, topics: dict) -> dict:
        """Subscribe topics."""
        return await self._sub(state, topics)

    async def publish(
        self,
        payload: SendMessageType,
        topic: str,
        retain: bool | None = False,
        qos: int | None = 0,
    ) -> None:
        """Publish to the broker."""
        return await self._pub(topic, payload, qos, retain)

    async def unsubscribe(self, state: dict | None) -> dict:
        """Unsubscribe topic."""
        return await self._un_sub(state)

    async def publish_with_delay(
        self,
        payload: SendMessageType,
        topic: str,
        retain: bool | None = False,
        qos: int | None = 0,
    ) -> None:
        """Publish with little delay."""
        msg = SendMessage(payload, topic, retain, qos)

        async def callback() -> None:
            """Callback which is calling publish fnc."""
            self._pending_msg.pop(msg)
            await self.publish(msg.payload, msg.topic, msg.retain, msg.qos)

        if msg in self._pending_msg:
            _t = self._pending_msg.pop(msg)
            _t.stop()

        _t = InelsTimer(1, callback)
        self._pending_msg[msg] = _t
