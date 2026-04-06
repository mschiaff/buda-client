from __future__ import annotations

from typing import overload

from buda_client.rest.endpoints.base import Endpoint
from buda_client.rest.models.markets import Market, MarketList, MarketTicker, TickerList


@overload
def markets_endpoint(market_id: str) -> Endpoint[Market]: ...
@overload
def markets_endpoint(market_id: None = ...) -> Endpoint[MarketList]: ...

def markets_endpoint(market_id: str | None = None) -> Endpoint[Market] | Endpoint[MarketList]:
    if market_id:
        return Endpoint(model=Market, method="GET", path=f"/markets/{market_id}")
    return Endpoint(model=MarketList, method="GET", path="/markets")


@overload
def tickers_endpoint(market_id: str) -> Endpoint[MarketTicker]: ...
@overload
def tickers_endpoint(market_id: None = ...) -> Endpoint[TickerList]: ...

def tickers_endpoint(market_id: str | None = None) -> Endpoint[MarketTicker] | Endpoint[TickerList]:
    if market_id:
        return Endpoint(model=MarketTicker, method="GET", path=f"/markets/{market_id}/ticker")
    return Endpoint(model=TickerList, method="GET", path="/tickers")