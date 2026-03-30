from __future__ import annotations

from typing import Any

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