from __future__ import annotations

from buda.rest.endpoints.base import Endpoint
from buda.rest.models.account import Balance, BalanceList, UserInfo


def me_endpoint() -> Endpoint[UserInfo]:
    return Endpoint(model=UserInfo, method="GET", path="/me")


def balances_endpoint(currency: str | None = None) -> Endpoint[Balance] | Endpoint[BalanceList]:
    if currency:
        return Endpoint(model=Balance, method="GET", path=f"/balances/{currency}")
    return Endpoint(model=BalanceList, method="GET", path="/balances")
