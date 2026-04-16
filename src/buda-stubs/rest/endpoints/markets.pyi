from typing import overload

from buda.rest.endpoints.base import Endpoint
from buda.rest.models.markets import Market, MarketList, MarketTicker, TickerList

@overload
def markets_endpoint(market_id: str) -> Endpoint[Market]: ...
@overload
def markets_endpoint(market_id: None = ...) -> Endpoint[MarketList]: ...

def markets_endpoint(market_id: str | None = ...) -> Endpoint[Market] | Endpoint[MarketList]:
    """Get an endpoint for fetching market information."""
    ...

@overload
def tickers_endpoint(market_id: str) -> Endpoint[MarketTicker]: ...
@overload
def tickers_endpoint(market_id: None = ...) -> Endpoint[TickerList]: ...

def tickers_endpoint(market_id: str | None = ...) -> Endpoint[MarketTicker] | Endpoint[TickerList]:
    """Get an endpoint for fetching ticker information."""
    ...
