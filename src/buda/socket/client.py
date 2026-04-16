from __future__ import annotations

import json
import logging
import urllib.parse
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from websockets import ConnectionClosed, connect

from buda.socket.channels import Channel

if TYPE_CHECKING:
    from buda.core.settings import BudaSettings

logger = logging.getLogger(__name__)

type EventHandler = Callable[[dict[str, Any]], Awaitable[None]]


async def default_handler(data: dict[str, Any]) -> None:
    print(data)


class BudaWebSocketClient:
    __slots__ = ("_pubsub_key", "_settings")

    def __init__(
            self,
            *,
            pubsub_key: str | None = None,
            settings: BudaSettings | None = None,
    ) -> None:
        from buda.core.settings import BudaSettings

        self._pubsub_key: str | None = pubsub_key
        self._settings: BudaSettings = settings or BudaSettings()

    def _build_url(
            self,
            *channels: Channel
    ) -> str:
        if not channels:
            raise ValueError("At least one channel is required.")

        parts = [ch.resolve(self._pubsub_key) for ch in channels]
        joined = ",".join(parts)
        base = self._settings.base_uri.encoded_string()
        url = f"{base}sub?channel={joined}"
        return urllib.parse.quote(url, safe=":/?=,")

    async def subscribe(
            self,
            *channels: Channel,
            handler: EventHandler = default_handler,
            events: set[str] | None = None,
    ) -> None:
        url = self._build_url(*channels)
        channel_names = ", ".join(ch.name for ch in channels)
        logger.info("Subscribing to [%s] at %s", channel_names, url)

        async for ws in connect(
                url,
                ping_interval=self._settings.ping_interval,
                ping_timeout=self._settings.ping_timeout,
                close_timeout=self._settings.close_timeout,
                open_timeout=self._settings.open_timeout,
                user_agent_header=self._settings.user_agent,
        ):
            try:
                logger.info("Connected to %s", url)
                async for raw in ws:
                    try:
                        data: dict[str, Any] = json.loads(raw)
                    except (json.JSONDecodeError, TypeError):
                        logger.warning("Non-JSON message received: %s", raw)
                        continue

                    if events is not None and data.get("ev") not in events:
                        continue

                    await handler(data)
            except ConnectionClosed as exc:
                logger.warning(
                    "Connection closed (code=%s reason=%s), reconnecting…",
                    exc.rcvd.code if exc.rcvd else "?",
                    exc.rcvd.reason if exc.rcvd else "?",
                )
                continue

    # ── Convenience methods ────────────────────────────────────────────

    async def book(
        self,
        market_id: str,
        *,
        handler: EventHandler = default_handler,
        events: set[str] | None = None,
    ) -> None:
        """Subscribe to order book updates for *market_id*."""
        await self.subscribe(Channel.book(market_id), handler=handler, events=events)

    async def trades(
        self,
        market_id: str,
        *,
        handler: EventHandler = default_handler,
        events: set[str] | None = None,
    ) -> None:
        """Subscribe to trade events for *market_id*."""
        await self.subscribe(Channel.trades(market_id), handler=handler, events=events)

    async def balances(
        self,
        *,
        handler: EventHandler = default_handler,
        events: set[str] | None = None,
    ) -> None:
        """Subscribe to balance updates (requires ``pubsub_key``)."""
        await self.subscribe(Channel.balances(), handler=handler, events=events)

    async def orders(
        self,
        *,
        handler: EventHandler = default_handler,
        events: set[str] | None = None,
    ) -> None:
        """Subscribe to order updates (requires ``pubsub_key``)."""
        await self.subscribe(Channel.orders(), handler=handler, events=events)

    async def deposits(
        self,
        *,
        handler: EventHandler = default_handler,
        events: set[str] | None = None,
    ) -> None:
        """Subscribe to deposit confirmations (requires ``pubsub_key``)."""
        await self.subscribe(Channel.deposits(), handler=handler, events=events)
