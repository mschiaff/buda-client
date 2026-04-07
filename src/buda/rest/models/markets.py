from __future__ import annotations

from typing import Any

from pydantic import BaseModel, RootModel, model_validator

from buda.rest.models.common import CurrencyValue  # noqa: TC001


class Market(BaseModel):
    id: str
    name: str
    base_currency: str
    quote_currency: str
    minimum_order_amount: CurrencyValue
    disabled: bool
    illiquid: bool
    rpo_disabled: bool | None
    taker_fee: float
    maker_fee: float
    max_orders_per_minute: int
    maker_discount_percentage: float
    taker_discount_percentage: float
    taker_discount_tiers: dict[str, float]
    maker_discount_tiers: dict[str, float]

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        if data.get("market"):
            return data["market"]
        return data


class MarketList(RootModel[list[Market]]):
    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["markets"]


class Ticker(BaseModel):
    market_id: str
    price_variation_24h: float
    price_variation_7d: float
    last_price: CurrencyValue


class MarketTicker(Ticker):
    min_ask: CurrencyValue
    max_bid: CurrencyValue
    volume: CurrencyValue
    quote_volume: CurrencyValue

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["ticker"]


class TickerList(RootModel[list[Ticker]]):
    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["tickers"]