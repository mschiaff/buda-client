from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Channel:
    """Represents a Buda.com WebSocket channel subscription."""

    name: str
    param: str
    private: bool

    @staticmethod
    def book(market_id: str) -> Channel:
        """Order book updates for a market (e.g. ``btcclp``)."""
        return Channel(name="book", param=market_id, private=False)

    @staticmethod
    def trades(market_id: str) -> Channel:
        """Trade events for a market (e.g. ``btcclp``)."""
        return Channel(name="trades", param=market_id, private=False)

    @staticmethod
    def balances() -> Channel:
        """Balance updates (requires ``pubsub_key``)."""
        return Channel(name="balances", param="", private=True)

    @staticmethod
    def orders() -> Channel:
        """Order updates (requires ``pubsub_key``)."""
        return Channel(name="orders", param="", private=True)

    @staticmethod
    def deposits() -> Channel:
        """Deposit confirmations (requires ``pubsub_key``)."""
        return Channel(name="deposits", param="", private=True)

    def resolve(self, pubsub_key: str | None = None) -> str:
        """Build the channel string for the WebSocket URL.

        Public channels resolve to ``name@param`` (e.g. ``book@btcclp``).
        Private channels resolve to ``name@pubsub_key`` and raise
        :class:`ValueError` when *pubsub_key* is not provided.
        """
        if self.private:
            if not pubsub_key:
                raise ValueError(f"Channel '{self.name}' is private and requires a pubsub_key.")
            return f"{self.name}@{pubsub_key}"
        return f"{self.name}@{self.param}"
