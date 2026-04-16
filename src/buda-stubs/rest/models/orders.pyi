from typing import Any, Literal, NotRequired, TypedDict

from pydantic import BaseModel, RootModel, model_validator

from buda.rest.models.common import CurrencyValue, PriceAmountList

QuotationType = Literal[
    "bid_given_size",
    "bid_given_earned_base",
    "bid_given_value",
    "bid_given_spent_quote",
    "ask_given_size",
    "ask_given_spent_base",
    "ask_given_value",
    "ask_given_earned_quote",
]
"""Represents the type of a quotation."""

class LimitOrder(TypedDict, total=False):
    """Represents a limit order with optional price and type."""

    price: float
    type: NotRequired[Literal["gtc", "ioc", "fok", "post_only", "gtd"]]
    ...

class StopOrder(TypedDict, total=False):
    """Represents a stop order with optional price and type."""

    price: float
    type: NotRequired[Literal["stop_loss", "take_profit"]]
    ...

class OrderBook(BaseModel):
    """Represents the order book for a market."""

    market_id: str
    bids: PriceAmountList
    asks: PriceAmountList

    @model_validator(mode="before")
    @classmethod
    def _parse_response(cls, data: dict[str, Any]) -> dict[str, Any]: ...

class Trades(BaseModel):
    """Represents a collection of trades for a market."""

    market_id: str
    timestamp: int | None
    last_timestamp: int
    entries: list[TradeEntry]

    @model_validator(mode="before")
    @classmethod
    def _parse_response(cls, data: dict[str, Any]) -> dict[str, Any]: ...

class TradeEntry(BaseModel):
    """Represents a single trade entry."""

    id: int
    timestamp: int
    direction: Literal["buy", "sell"]
    amount: float
    price: float

    @model_validator(mode="before")
    @classmethod
    def _parse_list(cls, data: list[str | int]) -> dict[str, Any]: ...

class Quotation(BaseModel):
    """Represents a quotation."""

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
    def _parse_response(cls, data: dict[str, Any]) -> dict[str, Any]: ...

class OrderCreate(BaseModel):
    """Represents the data required to create an order."""

    type: Literal["Bid", "Ask"]
    price_type: Literal["limit", "market"]
    amount: float
    limit: LimitOrder | None = ...
    stop: StopOrder | None = ...
    client_id: str | None = ...

class OrderCreateResponse(BaseModel):
    """Represents the response received after creating an order."""

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
    def _parse_response(cls, data: dict[str, Any]) -> dict[str, Any]: ...

class OrderDetail(BaseModel):
    """Represents the details of an order."""

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
    def _parse_response(cls, data: dict[str, Any]) -> dict[str, Any]: ...

class OrderCancelResponse(BaseModel):
    """Represents the response received after canceling an order."""

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
    def _parse_response(cls, data: dict[str, Any]) -> dict[str, Any]: ...

class OrderCancelAllResponse(RootModel[list[OrderCancelResponse]]):
    """Represents the response received after canceling all orders."""

    @model_validator(mode="before")
    @classmethod
    def _parse_response(cls, data: dict[str, Any]) -> dict[str, Any]: ...
