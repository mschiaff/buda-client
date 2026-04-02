from __future__ import annotations

from typing import Annotated, NotRequired, TypedDict

from pydantic import Field, TypeAdapter

from buda_client.endpoints.base import Endpoint
from buda_client.models.orders import OrderBook, Quotation, QuotationType, Trades


class TradesParams(TypedDict, total=False):
    timestamp: Annotated[int | None, Field(gt=0)]
    limit: Annotated[int | None, Field(gt=0, le=100)]


class QuotationPayload(TypedDict, total=False):
    type: Annotated[QuotationType, Field(...)]
    amount: Annotated[float, Field(..., gt=0)]
    limit: NotRequired[Annotated[float | None, Field(default=None, gt=0)]]


TradesParamsAdapter = TypeAdapter(TradesParams)
QuotationPayloadAdapter = TypeAdapter(QuotationPayload)


def order_book_endpoint(market_id: str) -> Endpoint[OrderBook]:
    return Endpoint(
        model=OrderBook, method="GET", path=f"/markets/{market_id}/order_book"
    )


def trades_endpoint(market_id: str, *, params: TradesParams | None = None) -> Endpoint[Trades]:
    params = TradesParamsAdapter.validate_python(params) if params else {}
    return Endpoint(
        model=Trades, method="GET", path=f"/markets/{market_id}/trades", params=params
    )


def quotation_endpoint(market_id: str, *, payload: QuotationPayload) -> Endpoint[Quotation]:
    payload = QuotationPayloadAdapter.validate_python(payload)
    return Endpoint(
        model=Quotation, method="POST", path=f"/markets/{market_id}/quotations", json=payload
    )