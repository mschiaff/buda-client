from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, model_validator

from buda_client.models.common import CurrencyValue, PriceAmount


QuotationType = Literal[
    "bid_given_size", "bid_given_earned_base",
    "bid_given_value", "bid_given_spent_quote",
    "ask_given_size", "ask_given_spent_base",
    "ask_given_value", "ask_given_earned_quote"
]


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