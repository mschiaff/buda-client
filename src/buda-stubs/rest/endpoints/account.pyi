from typing import overload

from buda.rest.endpoints.base import Endpoint
from buda.rest.models.account import Balance, BalanceList, UserInfo

def me_endpoint() -> Endpoint[UserInfo]:
    """Endpoint to retrieve user information."""
    ...

@overload
def balances_endpoint(currency: str) -> Endpoint[Balance]: ...
@overload
def balances_endpoint(currency: None = ...) -> Endpoint[BalanceList]: ...
def balances_endpoint(currency: str | None = ...) -> Endpoint[Balance] | Endpoint[BalanceList]:
    """Endpoint to retrieve account balances."""
    ...
