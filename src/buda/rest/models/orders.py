from __future__ import annotations

from typing import Annotated, Any, Literal, NotRequired, TypedDict

from pydantic import BaseModel, Field, RootModel, model_validator

from buda.rest.models.common import CurrencyValue, PriceAmount  # noqa: TC001

type QuotationType = Literal[
    "bid_given_size",
    "bid_given_earned_base",
    "bid_given_value",
    "bid_given_spent_quote",
    "ask_given_size",
    "ask_given_spent_base",
    "ask_given_value",
    "ask_given_earned_quote",
]


class LimitOrder(TypedDict, total=False):
    price: Annotated[float, ...]
    type: NotRequired[Annotated[Literal["gtc", "ioc", "fok", "post_only", "gtd"], ...]]


class StopOrder(TypedDict, total=False):
    price: Annotated[float, ...]
    type: NotRequired[Annotated[Literal["stop_loss", "take_profit"], ...]]


class OrderBook(BaseModel):
    market_id: str
    bids: list[PriceAmount]
    asks: list[PriceAmount]

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["order_book"]


class Trades(BaseModel):
    market_id: str
    timestamp: int | None
    last_timestamp: int
    entries: list[TradeEntry]

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["trades"]


class TradeEntry(BaseModel):
    id: int
    timestamp: int
    direction: Literal["buy", "sell"]
    amount: float
    price: float

    @model_validator(mode="before")
    @classmethod
    def parse_list(cls, data: list[str | int]) -> dict[str, Any]:
        timestamp, amount, price, direction, id = data
        return dict(
            timestamp=timestamp,
            amount=float(amount),
            price=float(price),
            direction=direction,
            id=id,
        )


class Quotation(BaseModel):
    amount: CurrencyValue
    limit: CurrencyValue | None
    type: QuotationType
    order_amount: CurrencyValue
    base_exchanged: CurrencyValue
    quote_exchanged: CurrencyValue
    base_balance_change: CurrencyValue
    quote_balance_change: CurrencyValue
    fee: CurrencyValue
    incomplete: bool

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["quotation"]


class OrderCreate(BaseModel):
    type: Literal["Bid", "Ask"]
    price_type: Literal["limit", "market"]
    amount: float
    limit: LimitOrder | None = Field(default=None)
    stop: StopOrder | None = Field(default=None)
    client_id: str | None = Field(default=None)


class OrderCreateResponse(BaseModel):
    id: int
    client_id: str | None
    amount: CurrencyValue
    created_at: str
    fee_currency: str
    limit: CurrencyValue | None
    market_id: str
    original_amount: CurrencyValue
    paid_fee: CurrencyValue
    price_type: Literal["limit", "market"]
    order_type: str
    state: str
    total_exchanged: CurrencyValue
    traded_amount: CurrencyValue
    type: Literal["Bid", "Ask"]

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["order"]


class OrderDetail(BaseModel):
    id: int
    client_id: str | None
    amount: CurrencyValue
    created_at: str
    fee_currency: str
    limit: CurrencyValue | None
    market_id: str
    original_amount: CurrencyValue
    paid_fee: CurrencyValue
    price_type: Literal["limit", "market"]
    order_type: str
    state: str
    total_exchanged: CurrencyValue
    traded_amount: CurrencyValue
    type: Literal["Bid", "Ask"]

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["order"]


class OrderCancelResponse(BaseModel):
    id: int
    client_id: str | None
    amount: CurrencyValue
    created_at: str
    fee_currency: str
    limit: CurrencyValue | None
    market_id: str
    original_amount: CurrencyValue
    paid_fee: CurrencyValue
    price_type: Literal["limit", "market"]
    order_type: str
    state: str
    total_exchanged: CurrencyValue
    traded_amount: CurrencyValue
    type: Literal["Bid", "Ask"]

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        if data.get("order"):
            return data["order"]
        return data


class OrderCancelAllResponse(RootModel[list[OrderCancelResponse]]):
    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["orders"]
