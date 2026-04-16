from typing import Any

from pydantic import BaseModel, RootModel, model_validator

from buda.rest.models.common import CurrencyValue

class Market(BaseModel):
    """Represents a market on the Buda exchange."""

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
    def _parse_response(cls, data: dict[str, Any]) -> dict[str, Any]: ...

class MarketList(RootModel[list[Market]]):
    """A list of :class:`Market` entries."""

    @model_validator(mode="before")
    @classmethod
    def _parse_response(cls, data: dict[str, Any]) -> dict[str, Any]: ...

class Ticker(BaseModel):
    """Represents a ticker on the Buda exchange."""

    market_id: str
    price_variation_24h: float
    price_variation_7d: float
    last_price: CurrencyValue
    ...

class MarketTicker(Ticker):
    """Represents a market ticker with additional details."""

    min_ask: CurrencyValue
    max_bid: CurrencyValue
    volume: CurrencyValue
    quote_volume: CurrencyValue

    @model_validator(mode="before")
    @classmethod
    def _parse_response(cls, data: dict[str, Any]) -> dict[str, Any]: ...

class TickerList(RootModel[list[Ticker]]):
    """A list of :class:`Ticker` entries."""

    @model_validator(mode="before")
    @classmethod
    def _parse_response(cls, data: dict[str, Any]) -> dict[str, Any]: ...
