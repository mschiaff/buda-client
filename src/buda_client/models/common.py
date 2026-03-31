from __future__ import annotations

from pydantic import BaseModel, model_validator


class CurrencyValue(BaseModel):
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


class PriceAmount(BaseModel):
    price: float
    amount: float

    @model_validator(mode="before")
    @classmethod
    def parse_list(cls, data: list[str]) -> dict[str, str]:
        price, amount = data
        return dict(
            price=price,
            amount=amount
        )