from __future__ import annotations

from typing import Any, TypedDict, Annotated

from pydantic import Field, TypeAdapter

from buda_client.endpoints.base import Endpoint
from buda_client.models.orders import OrderBook, Trades, Quotation, QuotationType


class TradesParams(TypedDict, total=False):
    timestamp: Annotated[int | None, Field(gt=0)]
    limit: Annotated[int | None, Field(gt=0, le=100)]


class QuotationParams(TypedDict):
    type: Annotated[QuotationType, Field(...)]
    amount: Annotated[float, Field(gt=0)]
    limit: Annotated[float | None, Field(default=None, gt=0)]


TradesParamsAdapter = TypeAdapter(TradesParams)
QuotationParamsAdapter = TypeAdapter(QuotationParams)


class OrderEndpoints:
    """Mixin providing order and trades-related endpoint definitions."""

    # Type hint so the mixin knows about _request
    _request: Any

    def _order_book_endpoint(self, market_id: str) -> Endpoint[OrderBook]:
        return Endpoint(model=OrderBook, method="GET", path=f"/markets/{market_id}/order_book")
    
    def _trades_endpoint(self, market_id: str, *, params: TradesParams | None = None) -> Endpoint[Trades]:
        params = TradesParamsAdapter.validate_python(params) if params else {}
        return Endpoint(model=Trades, method="GET", path=f"/markets/{market_id}/trades", params=params)
    
    def _quotation_endpoint(self, market_id: str, *, params: QuotationParams) -> Endpoint[Quotation]:
        params = QuotationParamsAdapter.validate_python(params)
        return Endpoint(model=Quotation, method="POST", path=f"/markets/{market_id}/quotations", json=params)