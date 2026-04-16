from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Channel:
    """Represents a Buda.com WebSocket channel subscription."""

    name: str
    param: str
    private: bool
    
    @staticmethod
    def book(market_id: str) -> Channel:
        """
        Order book updates for a market (e.g. ``btcclp``).
        
        Parameters
        ----------
        market_id : str
            Market identifier, e.g. "btcclp".
        
        Returns
        -------
        Channel
            Channel instance for the specified market's order book updates.
        """
        ...
    
    @staticmethod
    def trades(market_id: str) -> Channel:
        """
        Trade events for a market (e.g. ``btcclp``).
        
        Parameters
        ----------
        market_id : str
            Market identifier, e.g. "btcclp".
        
        Returns
        -------
        Channel
            Channel instance for the specified market's trade events.
        """
        ...
    
    @staticmethod
    def balances() -> Channel:
        """
        Balance updates (requires ``pubsub_key``).
        
        Returns
        -------
        Channel
            Channel instance for balance updates.
        """
        ...
    
    @staticmethod
    def orders() -> Channel:
        """
        Order updates (requires ``pubsub_key``).
        
        Returns
        -------
        Channel
            Channel instance for order updates.
        """
        ...
    
    @staticmethod
    def deposits() -> Channel:
        """
        Deposit confirmations (requires ``pubsub_key``).
        
        Returns
        -------
        Channel
            Channel instance for deposit confirmations.
        """
        ...

    def resolve(self, pubsub_key: str | None = ...) -> str:
        """Build the channel string for the WebSocket URL.

        Public channels resolve to ``name@param`` (e.g. ``book@btcclp``).
        Private channels resolve to ``name@pubsub_key`` and raise
        :class:`ValueError` when *pubsub_key* is not provided.
        
        Parameters
        ----------
        pubsub_key : str | None
            Public subscription key for private channels.
        
        Returns
        -------
        str
            Resolved channel string for the WebSocket URL.
        """
        ...
