from __future__ import annotations

from typing import Any

from buda_client.endpoints.base import Endpoint
from buda_client.models.markets import Ticker

class MarketEndpoints:
    """Mixin providing market-related endpoint definitions."""

    # Type hint so the mixin knows about _request
    _request: Any

    def _ticker_endpoint(self, market_id: str) -> Endpoint[Ticker]:
        return Endpoint(
            model=Ticker,
            method="GET",
            path=f"/markets/{market_id}/ticker",
        )