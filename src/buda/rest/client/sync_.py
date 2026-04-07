# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload
from warnings import deprecated

from httpx import Client
from pydantic import BaseModel

from buda.core.limiter import SyncRateLimiter
from buda.core.retry import sync_retry_on_error
from buda.rest.client.base import BaseClient
from buda.rest.endpoints import account, markets, orders
from buda.rest.models.account import Balance, BalanceList, UserInfo  # noqa: TC001
from buda.rest.models.markets import (  # noqa: TC001
    Market,
    MarketList,
    MarketTicker,
    TickerList,
)
from buda.rest.models.orders import (  # noqa: TC001
    OrderBook,
    OrderCancelAllResponse,
    OrderCancelResponse,
    OrderCreate,
    OrderCreateResponse,
    OrderDetail,
    Quotation,
    Trades,
)

if TYPE_CHECKING:
    from buda.core.providers import BudaCredentials
    from buda.core.settings import BudaSettings
    from buda.rest.endpoints.base import Endpoint, RequestMethod
    from buda.rest.endpoints.orders import QuotationPayload, TradesParams


T = TypeVar("T", bound=BaseModel)


class PublicAPI:
    __slots__ = ("_client",)

    def __init__(self, client: BudaClient):
        self._client: BudaClient = client

    @overload
    def markets(
        self, market_id: str, *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> Market: ...
    @overload
    def markets(
        self, market_id: None = ..., *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> MarketList: ...
    @overload
    def markets(
        self, market_id: str | None = None, *, raw: Literal[True], authenticated: bool = ...
    ) -> dict[str, Any]: ...

    def markets(
        self, market_id: str | None = None, *, raw: bool = False, authenticated: bool = False
    ) -> Market | MarketList | dict[str, Any]:
        return self._client._request(
            markets.markets_endpoint(market_id), raw=raw, authenticated=authenticated
        )

    @overload
    def tickers(
        self, market_id: str, *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> MarketTicker: ...
    @overload
    def tickers(
        self, market_id: None = ..., *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> TickerList: ...
    @overload
    def tickers(
        self, market_id: str | None = None, *, raw: Literal[True], authenticated: bool = ...
    ) -> dict[str, Any]: ...

    def tickers(
        self, market_id: str | None = None, *, raw: bool = False, authenticated: bool = False
    ) -> MarketTicker | TickerList | dict[str, Any]:
        return self._client._request(
            markets.tickers_endpoint(market_id), raw=raw, authenticated=authenticated
        )

    @overload
    def order_book(
        self, market_id: str, *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> OrderBook: ...
    @overload
    def order_book(
        self, market_id: str, *, raw: Literal[True], authenticated: bool = ...
    ) -> dict[str, Any]: ...

    def order_book(
        self, market_id: str, *, raw: bool = False, authenticated: bool = False
    ) -> OrderBook | dict[str, Any]:
        return self._client._request(
            orders.order_book_endpoint(market_id), raw=raw, authenticated=authenticated
        )

    @overload
    @deprecated(
        "Authenticated trades requests with query params return 401. "
        "Use authenticated=False (default) when passing params."
    )
    def trades(
        self,
        market_id: str,
        *,
        params: TradesParams,
        authenticated: Literal[True],
        raw: Literal[False] = ...,
    ) -> Trades: ...

    @overload
    @deprecated(
        "Authenticated trades requests with query params return 401. "
        "Use authenticated=False (default) when passing params."
    )
    def trades(
        self,
        market_id: str,
        *,
        params: TradesParams,
        authenticated: Literal[True],
        raw: Literal[True],
    ) -> dict[str, Any]: ...

    @overload
    def trades(
        self,
        market_id: str,
        *,
        params: TradesParams | None = ...,
        raw: Literal[False] = ...,
        authenticated: bool = ...,
    ) -> Trades: ...
    @overload
    def trades(
        self,
        market_id: str,
        *,
        params: TradesParams | None = ...,
        raw: Literal[True],
        authenticated: bool = ...,
    ) -> dict[str, Any]: ...

    def trades(
        self,
        market_id: str,
        *,
        params: TradesParams | None = None,
        raw: bool = False,
        authenticated: bool = False,
    ) -> Trades | dict[str, Any]:
        return self._client._request(
            orders.trades_endpoint(market_id, params=params), raw=raw, authenticated=authenticated
        )

    @overload
    def quotations(
        self,
        market_id: str,
        *,
        payload: QuotationPayload,
        raw: Literal[False] = ...,
        authenticated: bool = ...,
    ) -> Quotation: ...
    @overload
    def quotations(
        self,
        market_id: str,
        *,
        payload: QuotationPayload,
        raw: Literal[True],
        authenticated: bool = ...,
    ) -> dict[str, Any]: ...

    def quotations(
        self,
        market_id: str,
        *,
        payload: QuotationPayload,
        raw: bool = False,
        authenticated: bool = False,
    ) -> Quotation | dict[str, Any]:
        return self._client._request(
            orders.quotation_endpoint(market_id, payload=payload),
            raw=raw,
            authenticated=authenticated,
        )


class PrivateAPI:
    __slots__ = ("_client",)

    def __init__(self, client: BudaClient):
        self._client: BudaClient = client

    @overload
    def me(self, *, raw: Literal[False] = ...) -> UserInfo: ...
    @overload
    def me(self, *, raw: Literal[True]) -> dict[str, Any]: ...

    def me(self, *, raw: bool = False) -> UserInfo | dict[str, Any]:
        return self._client._request(account.me_endpoint(), raw=raw, authenticated=True)

    @overload
    def balances(self, currency: str, *, raw: Literal[False] = ...) -> Balance: ...
    @overload
    def balances(self, currency: None = ..., *, raw: Literal[False] = ...) -> BalanceList: ...
    @overload
    def balances(self, currency: str | None = ..., *, raw: Literal[True]) -> dict[str, Any]: ...

    def balances(
        self, currency: str | None = None, *, raw: bool = False
    ) -> Balance | BalanceList | dict[str, Any]:
        return self._client._request(
            account.balances_endpoint(currency), raw=raw, authenticated=True
        )

    @overload
    def create_order(
        self,
        market_id: str,
        *,
        payload: OrderCreate,
        raw: Literal[False] = ...,
    ) -> OrderCreateResponse: ...
    @overload
    def create_order(
        self,
        market_id: str,
        *,
        payload: OrderCreate,
        raw: Literal[True],
    ) -> dict[str, Any]: ...

    def create_order(
        self, market_id: str, *, payload: OrderCreate, raw: bool = False
    ) -> OrderCreateResponse | dict[str, Any]:
        return self._client._request(
            orders.create_order_endpoint(market_id, payload=payload), raw=raw, authenticated=True
        )

    @overload
    def order_detail(
        self,
        order_id: int,
        *,
        raw: Literal[False] = ...,
    ) -> OrderDetail: ...
    @overload
    def order_detail(
        self,
        order_id: int,
        *,
        raw: Literal[True],
    ) -> dict[str, Any]: ...

    def order_detail(self, order_id: int, *, raw: bool = False) -> OrderDetail | dict[str, Any]:
        return self._client._request(
            orders.order_detail_endpoint(order_id), raw=raw, authenticated=True
        )

    @overload
    def cancel_order(
        self,
        order_id: int,
        *,
        raw: Literal[False] = ...,
    ) -> OrderCancelResponse: ...
    @overload
    def cancel_order(
        self,
        order_id: int,
        *,
        raw: Literal[True],
    ) -> dict[str, Any]: ...

    def cancel_order(
        self, order_id: int, *, raw: bool = False
    ) -> OrderCancelResponse | dict[str, Any]:
        return self._client._request(
            orders.cancel_order_endpoint(order_id), raw=raw, authenticated=True
        )

    @overload
    def cancel_all_orders(
        self,
        market_id: str | None = None,
        type: str | None = None,
        *,
        raw: Literal[False] = ...,
    ) -> OrderCancelAllResponse: ...
    @overload
    def cancel_all_orders(
        self,
        market_id: str | None = None,
        type: str | None = None,
        *,
        raw: Literal[True],
    ) -> dict[str, Any]: ...

    def cancel_all_orders(
        self, market_id: str | None = None, type: str | None = None, *, raw: bool = False
    ) -> OrderCancelAllResponse | dict[str, Any]:
        return self._client._request(
            orders.cancel_all_orders_endpoint(market_id, type), raw=raw, authenticated=True
        )


class BudaClient(BaseClient[Client]):
    """Synchronous client for the Buda API."""

    __slots__ = ("_rate_limiter", "private", "public")

    def __init__(
        self, settings: BudaSettings | None = None, provider: BudaCredentials | None = None
    ) -> None:
        super().__init__(client=Client, settings=settings, provider=provider)
        self._rate_limiter = SyncRateLimiter(self._settings)
        self.public = PublicAPI(self)
        self.private = PrivateAPI(self)

    def __enter__(self) -> BudaClient:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore
        self.close()

    def close(self) -> None:
        self._client.close()

    @overload
    def _request(
        self, endpoint: Endpoint[T], *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> T: ...
    @overload
    def _request(
        self, endpoint: Endpoint[T], *, raw: Literal[True], authenticated: bool = ...
    ) -> dict[str, Any]: ...

    @sync_retry_on_error
    def _request(
        self, endpoint: Endpoint[T], *, raw: bool = False, authenticated: bool = False
    ) -> T | dict[str, Any]:
        if authenticated and not self._auth:
            raise ValueError("Authentication was requested, but no auth credentials were provided.")

        self._rate_limiter.acquire(authenticated=authenticated)

        request = self._build_request(endpoint)
        response = self._client.send(request, auth=self._auth if authenticated else None)

        response.raise_for_status()

        return response.json() if raw else endpoint.model(**response.json())

    @sync_retry_on_error
    def _raw_request(
        self, method: RequestMethod, path: str, *, authenticated: bool = False, **kwargs: Any
    ) -> dict[str, Any]:
        if authenticated and not self._auth:
            raise ValueError("Authentication was requested, but no auth credentials were provided.")

        self._rate_limiter.acquire(authenticated=authenticated)

        response = self._client.request(
            method, path, auth=self._auth if authenticated else None, **kwargs
        )

        response.raise_for_status()
        return response.json()
