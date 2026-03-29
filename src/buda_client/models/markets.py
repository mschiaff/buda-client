from __future__ import annotations

from typing import Any

from pydantic import BaseModel, model_validator


class TickerRecord(BaseModel):
    value: float
    currency: str

    @model_validator(mode="before")
    @classmethod
    def parse_list(cls, data: list[str]) -> dict[str, str]:
        value, currency = data
        return dict(
            value=value,
            currency=currency
        )


class Ticker(BaseModel):
    market_id: str
    last_price: TickerRecord
    min_ask: TickerRecord
    max_bid: TickerRecord
    volume: TickerRecord
    quote_volume: TickerRecord
    price_variation_24h: float
    price_variation_7d: float

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["ticker"]