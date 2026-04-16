from collections.abc import Awaitable, Callable
from logging import Logger
from typing import Any

from buda.core.settings import BudaSettings
from buda.socket.channels import Channel

logger: Logger = ...
type EventHandler = Callable[[dict[str, Any]], Awaitable[None]]

async def default_handler(data: dict[str, Any]) -> None:
    """Print received WebSocket event data."""
    ...

class BudaWebSocketClient:
    """Async WebSocket client for the Buda.com realtime API.

    Public channels (order book, trades) require no authentication.
    Private channels (balances, orders, deposits) require a ``pubsub_key``
    obtained from the ``GET /me`` REST endpoint.

    Example::

        client = BudaWebSocketClient()
        await client.book("btcclp")                       # prints live events

        client = BudaWebSocketClient(pubsub_key="xxx")
        await client.subscribe(
            Channel.book("btcclp"),
            Channel.balances(),
            handler=my_handler,
            events={"book-changed", "balance-updated"},
        )
    """

    __slots__ = ("_pubsub_key", "_settings")

    _pubsub_key: str | None
    """Pub/Sub key for private channels, or ``None`` if not set."""
    _settings: BudaSettings
    """Buda API settings, including the base URI."""

    def __init__(
        self, *, pubsub_key: str | None = ..., settings: BudaSettings | None = ...
    ) -> None:
        """
        Initialize a new BudaWebSocketClient instance.

        Parameters
        ----------
        pubsub_key : str | None, optional
            Pub/Sub key for private channels, or ``None`` if not set.
        settings : BudaSettings | None, optional
            Buda API settings, including the base URI. If not provided,
            defaults to a new BudaSettings instance.
        """
        ...

    async def subscribe(
        self, *channels: Channel, handler: EventHandler = ..., events: set[str] | None = ...
    ) -> None:
        """Connect to one or more channels and stream events to *handler*.

        This coroutine blocks until cancelled.  It automatically reconnects
        on connection drops using ``websockets``' built-in retry logic.

        Parameters
        ----------
        channels : Channel
            One or more :class:`Channel` instances to subscribe to.
        handler : EventHandler, optional
            Async callable receiving each event as a ``dict``.
                Defaults to :func:`default_handler` which prints the data.
        events : set[str] | None, optional
            Optional set of event names (the ``ev`` field) to forward.
            When *None*, every event is forwarded.
        """
        ...

    async def book(
        self, market_id: str, *, handler: EventHandler = ..., events: set[str] | None = ...
    ) -> None:
        """
        Subscribe to order book updates for *market_id*.

        Parameters
        ----------
        market_id : str
            Market identifier, e.g. "btcclp".
        handler : EventHandler, optional
            Async callable receiving each event as a ``dict``.
            Defaults to :func:`default_handler` which prints the data.
        events : set[str] | None, optional
            Optional set of event names (the ``ev`` field) to forward.
            When *None*, every event is forwarded.
        """
        ...

    async def trades(
        self, market_id: str, *, handler: EventHandler = ..., events: set[str] | None = ...
    ) -> None:
        """
        Subscribe to trade events for *market_id*.

        Parameters
        ----------
        market_id : str
            Market identifier, e.g. "btcclp".
        handler : EventHandler, optional
            Async callable receiving each event as a ``dict``.
            Defaults to :func:`default_handler` which prints the data.
        events : set[str] | None, optional
            Optional set of event names (the ``ev`` field) to forward.
            When *None*, every event is forwarded.
        """
        ...

    async def balances(self, *, handler: EventHandler = ..., events: set[str] | None = ...) -> None:
        """
        Subscribe to balance updates (requires ``pubsub_key``).

        Parameters
        ----------
        handler : EventHandler, optional
            Async callable receiving each event as a ``dict``.
            Defaults to :func:`default_handler` which prints the data.
        events : set[str] | None, optional
            Optional set of event names (the ``ev`` field) to forward.
            When *None*, every event is forwarded.
        """
        ...

    async def orders(self, *, handler: EventHandler = ..., events: set[str] | None = ...) -> None:
        """
        Subscribe to order updates (requires ``pubsub_key``).

        Parameters
        ----------
        handler : EventHandler, optional
            Async callable receiving each event as a ``dict``.
            Defaults to :func:`default_handler` which prints the data.
        events : set[str] | None, optional
            Optional set of event names (the ``ev`` field) to forward.
            When *None*, every event is forwarded.
        """
        ...

    async def deposits(self, *, handler: EventHandler = ..., events: set[str] | None = ...) -> None:
        """
        Subscribe to deposit confirmations (requires ``pubsub_key``).

        Parameters
        ----------
        handler : EventHandler, optional
            Async callable receiving each event as a ``dict``.
            Defaults to :func:`default_handler` which prints the data.
        events : set[str] | None, optional
            Optional set of event names (the ``ev`` field) to forward.
            When *None*, every event is forwarded.
        """
        ...

    def _build_url(self, *channels: Channel) -> str:
        """
        Resolve channels and build the full WebSocket URL.

        Parameters
        ----------
        channels : Channel
            Channels to include in the WebSocket URL.

        Returns
        -------
        str
            The full WebSocket URL.
        """
