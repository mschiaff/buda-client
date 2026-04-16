from typing import NotRequired, TypedDict

from pydantic import TypeAdapter

from buda.rest.endpoints.base import Endpoint
from buda.rest.models.orders import (
    OrderBook,
    OrderCancelAllResponse,
    OrderCancelResponse,
    OrderCreate,
    OrderCreateResponse,
    OrderDetail,
    Quotation,
    QuotationType,
    Trades,
)

class TradesParams(TypedDict, total=False):
    timestamp: int | None
    limit: int | None
    ...


class QuotationPayload(TypedDict, total=False):
    type: QuotationType
    amount: float
    limit: NotRequired[float | None]
    ...


TradesParamsAdapter: TypeAdapter[TradesParams]
QuotationPayloadAdapter: TypeAdapter[QuotationPayload]


def order_book_endpoint(market_id: str) -> Endpoint[OrderBook]: ...

def trades_endpoint(market_id: str, *, params: TradesParams | None = ...) -> Endpoint[Trades]: ...

def quotation_endpoint(market_id: str, *, payload: QuotationPayload) -> Endpoint[Quotation]: ...

def create_order_endpoint(
        market_id: str,
        *,
        payload: OrderCreate
) -> Endpoint[OrderCreateResponse]: ...

def order_detail_endpoint(order_id: int) -> Endpoint[OrderDetail]: ...

def cancel_order_endpoint(order_id: int) -> Endpoint[OrderCancelResponse]: ...

def cancel_all_orders_endpoint(
        market_id: str | None = ...,
        type: str | None = ...
) -> Endpoint[OrderCancelAllResponse]: ...
