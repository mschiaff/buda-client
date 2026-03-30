from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, model_validator

from buda_client.models.common import PriceAmount


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