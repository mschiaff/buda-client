from typing import Literal

from pydantic import BaseModel, RootModel, model_validator

class CurrencyValue(BaseModel):
    """Represents a currency value with its amount and currency code."""

    value: float
    currency: str

    @model_validator(mode="before")
    @classmethod
    def _parse_list(cls, data: list[str]) -> dict[str, str]: ...

class PriceAmount(BaseModel):
    """Represents a price and amount pair."""

    price: float
    amount: float

    @model_validator(mode="before")
    @classmethod
    def _parse_list(cls, data: list[str]) -> dict[str, str]: ...

class PriceAmountList(RootModel[list[PriceAmount]]):
    """A list of :class:`PriceAmount` entries with utility methods."""

    def __getitem__(self, index: int) -> PriceAmount: ...
    def __len__(self) -> int: ...
    def min(self, key: Literal["price", "amount"] = ...) -> PriceAmount:
        """
        Get the entry with the minimum value for the specified key.

        Parameters
        ----------
        key : Literal["price", "amount"], optional
            The key to compare for finding the minimum value, by default "price"

        Returns
        -------
        PriceAmount
            The entry with the minimum value for the specified key.
        """
        ...

    def max(self, key: Literal["price", "amount"] = ...) -> PriceAmount:
        """
        Get the entry with the maximum value for the specified key.

        Parameters
        ----------
        key : Literal["price", "amount"], optional
            The key to compare for finding the maximum value, by default "price"

        Returns
        -------
        PriceAmount
            The entry with the maximum value for the specified key.
        """
        ...
