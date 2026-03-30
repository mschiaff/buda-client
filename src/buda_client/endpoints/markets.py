from __future__ import annotations

from typing import Any, overload

from buda_client.endpoints.base import Endpoint
from buda_client.models.markets import Market, MarketList, MarketTicker, TickerList

class MarketEndpoints:
    """Mixin providing market-related endpoint definitions."""

    # Type hint so the mixin knows about _request
    _request: Any

    @overload
    def _markets_endpoint(self, market_id: str) -> Endpoint[Market]: ...
    @overload
    def _markets_endpoint(self, market_id: None = ...) -> Endpoint[MarketList]: ...

    def _markets_endpoint(self, market_id: str | None = None) -> Endpoint[Market | MarketList]:
        if market_id:
            return Endpoint(model=Market, method="GET", path=f"/markets/{market_id}")
        return Endpoint(model=MarketList, method="GET", path="/markets")

    @overload
    def _tickers_endpoint(self, market_id: str) -> Endpoint[MarketTicker]: ...
    @overload
    def _tickers_endpoint(self, market_id: None = ...) -> Endpoint[TickerList]: ...

    def _tickers_endpoint(self, market_id: str | None = None) -> Endpoint[MarketTicker | TickerList]:
        if market_id:
            return Endpoint(model=MarketTicker, method="GET", path=f"/markets/{market_id}/ticker")
        return Endpoint(model=TickerList, method="GET", path="/tickers")