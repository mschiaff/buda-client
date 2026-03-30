from __future__ import annotations

from typing import Any

from buda_client.endpoints.base import Endpoint
from buda_client.models.orders import OrderBook, Trades


class OrderEndpoints:
    """Mixin providing order and trades-related endpoint definitions."""

    # Type hint so the mixin knows about _request
    _request: Any

    def _order_book_endpoint(self, market_id: str) -> Endpoint[OrderBook]:
        return Endpoint(model=OrderBook, method="GET", path=f"/markets/{market_id}/order_book")
    
    def _trades_endpoint(self, market_id: str) -> Endpoint[Trades]:
        return Endpoint(model=Trades, method="GET", path=f"/markets/{market_id}/trades")