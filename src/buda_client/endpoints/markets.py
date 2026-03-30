from __future__ import annotations

from typing import Any, overload

from buda_client.endpoints.base import Endpoint
from buda_client.models.markets import Market, MarketList, Ticker

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

    def _ticker_endpoint(self, market_id: str) -> Endpoint[Ticker]:
        return Endpoint(model=Ticker, method="GET", path=f"/markets/{market_id}/ticker")