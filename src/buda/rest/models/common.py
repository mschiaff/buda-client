from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, RootModel, model_validator


class CurrencyValue(BaseModel):
    value: float
    currency: str

    @model_validator(mode="before")
    @classmethod
    def _parse_list(cls, data: list[str]) -> dict[str, str]:
        value, currency = data
        return dict(value=value, currency=currency)


class PriceAmount(BaseModel):
    price: float
    amount: float

    @model_validator(mode="before")
    @classmethod
    def _parse_list(cls, data: list[str]) -> dict[str, str]:
        price, amount = data
        return dict(price=price, amount=amount)


class PriceAmountList(RootModel[list[PriceAmount]]):
    def __getitem__(self, index: int) -> PriceAmount:
        return self.root[index]

    def __len__(self) -> int:
        return len(self.root)

    def min(self, key: Literal["price", "amount"] = "price") -> PriceAmount:
        return min(self.root, key=lambda entry: getattr(entry, key))

    def max(self, key: Literal["price", "amount"] = "price") -> PriceAmount:
        return max(self.root, key=lambda entry: getattr(entry, key))
