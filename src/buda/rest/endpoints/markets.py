from __future__ import annotations

from buda.rest.endpoints.base import Endpoint
from buda.rest.models.markets import Market, MarketList, MarketTicker, TickerList


def markets_endpoint(market_id: str | None = None) -> Endpoint[Market] | Endpoint[MarketList]:
    if market_id:
        return Endpoint(model=Market, method="GET", path=f"/markets/{market_id}")
    return Endpoint(model=MarketList, method="GET", path="/markets")


def tickers_endpoint(market_id: str | None = None) -> Endpoint[MarketTicker] | Endpoint[TickerList]:
    if market_id:
        return Endpoint(model=MarketTicker, method="GET", path=f"/markets/{market_id}/ticker")
    return Endpoint(model=TickerList, method="GET", path="/tickers")
