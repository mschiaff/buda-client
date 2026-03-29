from __future__ import annotations

from typing import Any

from pydantic import BaseModel, model_validator

from buda_client.models.common import CurrencyValue


class Ticker(BaseModel):
    market_id: str
    last_price: CurrencyValue
    min_ask: CurrencyValue
    max_bid: CurrencyValue
    volume: CurrencyValue
    quote_volume: CurrencyValue
    price_variation_24h: float
    price_variation_7d: float

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["ticker"]