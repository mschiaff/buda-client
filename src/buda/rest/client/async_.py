# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from httpx import AsyncClient
from pydantic import BaseModel

from buda.core.limiter import AsyncRateLimiter
from buda.core.retry import async_retry_on_error
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
    from types import TracebackType

    from buda.core.providers import BudaCredentials
    from buda.core.settings import BudaSettings
    from buda.rest.endpoints.base import Endpoint, RequestMethod
    from buda.rest.endpoints.orders import QuotationPayload, TradesParams


T = TypeVar("T", bound=BaseModel)


class AsyncPublicAPI:
    __slots__ = ("_client",)

    def __init__(self, client: AsyncBudaClient):
        self._client: AsyncBudaClient = client

    async def markets(
            self,
            market_id: str | None = None,
            *,
            raw: bool = False,
            authenticated: bool = False
    ) -> Market | MarketList | dict[str, Any]:
        return await self._client._request(
            markets.markets_endpoint(market_id),
            raw=raw,
            authenticated=authenticated
        )

    async def tickers(
            self,
            market_id: str | None = None,
            *,
            raw: bool = False,
            authenticated: bool = False
    ) -> MarketTicker | TickerList | dict[str, Any]:
        return await self._client._request(
            markets.tickers_endpoint(market_id),
            raw=raw,
            authenticated=authenticated
        )

    async def order_book(
            self,
            market_id: str,
            *,
            raw: bool = False,
            authenticated: bool = False
    ) -> OrderBook | dict[str, Any]:
        return await self._client._request(
            orders.order_book_endpoint(market_id),
            raw=raw,
            authenticated=authenticated
        )

    async def trades(
            self,
            market_id: str,
            *,
            params: TradesParams | None = None,
            raw: bool = False,
            authenticated: bool = False,
    ) -> Trades | dict[str, Any]:
        return await self._client._request(
            orders.trades_endpoint(
                market_id=market_id,
                params=params
            ),
            raw=raw,
            authenticated=authenticated
        )

    async def quotations(
            self,
            market_id: str,
            *,
            payload: QuotationPayload,
            raw: bool = False,
            authenticated: bool = False,
    ) -> Quotation | dict[str, Any]:
        return await self._client._request(
            orders.quotation_endpoint(
                market_id=market_id,
                payload=payload
            ),
            raw=raw,
            authenticated=authenticated,
        )


class AsyncPrivateAPI:
    __slots__ = ("_client",)

    def __init__(self, client: AsyncBudaClient):
        self._client: AsyncBudaClient = client

    async def me(
            self,
            *,
            raw: bool = False
    ) -> UserInfo | dict[str, Any]:
        return await self._client._request(
            account.me_endpoint(),
            raw=raw,
            authenticated=True
        )

    async def balances(
            self,
            currency: str | None = None,
            *,
            raw: bool = False
    ) -> Balance | BalanceList | dict[str, Any]:
        return await self._client._request(
            account.balances_endpoint(currency),
            raw=raw,
            authenticated=True
        )

    async def create_order(
            self,
            market_id: str,
            *,
            payload: OrderCreate,
            raw: bool = False
    ) -> OrderCreateResponse | dict[str, Any]:
        return await self._client._request(
            orders.create_order_endpoint(
                market_id,
                payload=payload
            ),
            raw=raw,
            authenticated=True
        )

    async def order_detail(
            self,
            order_id: int,
            *,
            raw: bool = False
    ) -> OrderDetail | dict[str, Any]:
        return await self._client._request(
            orders.order_detail_endpoint(order_id),
            raw=raw,
            authenticated=True
        )

    async def cancel_order(
            self,
            order_id: int,
            *,
            raw: bool = False
    ) -> OrderCancelResponse | dict[str, Any]:
        return await self._client._request(
            orders.cancel_order_endpoint(order_id),
            raw=raw,
            authenticated=True
        )

    async def cancel_all_orders(
            self,
            market_id: str | None = None,
            type: str | None = None,
            *,
            raw: bool = False
    ) -> OrderCancelAllResponse | dict[str, Any]:
        return await self._client._request(
            orders.cancel_all_orders_endpoint(
                market_id=market_id,
                type=type
            ),
            raw=raw,
            authenticated=True
        )


class AsyncBudaClient(BaseClient[AsyncClient]):
    """Asynchronous client for the Buda API."""

    __slots__ = ("_rate_limiter", "private", "public")

    def __init__(
            self,
            settings: BudaSettings | None = None,
            provider: BudaCredentials | None = None
    ) -> None:
        super().__init__(
            client=AsyncClient,
            settings=settings,
            provider=provider
        )
        self._rate_limiter = AsyncRateLimiter(
            self._settings
        )
        self.public = AsyncPublicAPI(self)
        self.private = AsyncPrivateAPI(self)

    async def __aenter__(self) -> AsyncBudaClient:
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None
    ) -> None:
        await self.close()

    async def close(self) -> None:
        await self._client.aclose()

    @async_retry_on_error
    async def _request(
            self,
            endpoint: Endpoint[T],
            *,
            raw: bool = False,
            authenticated: bool = False
    ) -> T | dict[str, Any]:
        if authenticated and not self._auth:
            raise ValueError(
                "Authentication was requested, "
                "but no auth credentials were provided."
            )

        await self._rate_limiter.acquire(
            authenticated=authenticated
        )
        request = self._build_request(
            endpoint
        )
        response = await self._client.send(
            request,
            auth=self._auth if authenticated else None
        )

        response.raise_for_status()

        return (
            response.json()
            if raw else endpoint.model(
                **response.json()
            )
        )

    @async_retry_on_error
    async def _raw_request(
            self,
            method: RequestMethod,
            path: str,
            *,
            authenticated: bool = False,
            **kwargs: Any
    ) -> dict[str, Any]:
        if authenticated and not self._auth:
            raise ValueError(
                "Authentication was requested, "
                "but no auth credentials were provided."
            )

        await self._rate_limiter.acquire(
            authenticated=authenticated
        )
        response = await self._client.request(
            method,
            path,
            auth=self._auth if authenticated else None,
            **kwargs
        )

        response.raise_for_status()

        return response.json()
