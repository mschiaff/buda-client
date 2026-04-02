# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload
from warnings import deprecated

from httpx import AsyncClient
from pydantic import BaseModel

from buda_client.clients.base import BaseClient
from buda_client.endpoints import account, markets, orders
from buda_client.models.account import UserInfo  # noqa: TC001
from buda_client.models.markets import Market, MarketList, MarketTicker, TickerList  # noqa: TC001
from buda_client.models.orders import OrderBook, Quotation, Trades  # noqa: TC001

if TYPE_CHECKING:
    from buda_client.endpoints.base import Endpoint
    from buda_client.endpoints.orders import QuotationParams, TradesParams
    from buda_client.providers import BudaCredentials
    from buda_client.settings import BudaSettings


T = TypeVar("T", bound=BaseModel)


class AsyncPublicAPI:
    __slots__ = ("_client",)

    def __init__(self, client: AsyncBudaClient):
        self._client: AsyncBudaClient = client

    @overload
    async def markets(
            self,
            market_id: str,
            *,
            raw: Literal[False] = ...,
            authenticated: bool = ...
    ) -> Market: ...
    @overload
    async def markets(
            self,
            market_id: None = ...,
            *,
            raw: Literal[False] = ...,
            authenticated: bool = ...
    ) -> MarketList: ...
    @overload
    async def markets(
            self,
            market_id: str | None = None,
            *,
            raw: Literal[True],
            authenticated: bool = ...
    ) -> dict[str, Any]: ...

    async def markets(
            self,
            market_id: str | None = None,
            *,
            raw: bool = False,
            authenticated: bool = False
    ) -> Market | MarketList | dict[str, Any]:
        return await self._client._request(
            markets.markets_endpoint(
                market_id
            ),
            raw=raw,
            authenticated=authenticated
        )

    @overload
    async def tickers(
            self,
            market_id: str,
            *,
            raw: Literal[False] = ...,
            authenticated: bool = ...
    ) -> MarketTicker: ...
    @overload
    async def tickers(
            self,
            market_id: None = ...,
            *,
            raw: Literal[False] = ...,
            authenticated: bool = ...
    ) -> TickerList: ...
    @overload
    async def tickers(
            self,
            market_id: str | None = None,
            *,
            raw: Literal[True],
            authenticated: bool = ...
    ) -> dict[str, Any]: ...

    async def tickers(
            self,
            market_id: str | None = None,
            *,
            raw: bool = False,
            authenticated: bool = False
    ) -> MarketTicker | TickerList | dict[str, Any]:
        return await self._client._request(
            markets.tickers_endpoint(
                market_id
            ),
            raw=raw,
            authenticated=authenticated
        )

    @overload
    async def order_book(
            self,
            market_id: str,
            *,
            raw: Literal[False] = ...,
            authenticated: bool = ...
    ) -> OrderBook: ...
    @overload
    async def order_book(
            self,
            market_id: str,
            *,
            raw: Literal[True],
            authenticated: bool = ...
    ) -> dict[str, Any]: ...

    async def order_book(
            self,
            market_id: str,
            *,
            raw: bool = False,
            authenticated: bool = False
    ) -> OrderBook | dict[str, Any]:
        return await self._client._request(
            orders.order_book_endpoint(
                market_id
            ),
            raw=raw,
            authenticated=authenticated
        )

    @overload
    @deprecated(
        "Authenticated trades requests with query params return 401. "
        "Use authenticated=False (default) when passing params."
    )
    async def trades(
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
    async def trades(
            self,
            market_id: str,
            *,
            params: TradesParams,
            authenticated: Literal[True],
            raw: Literal[True],
    ) -> dict[str, Any]: ...

    @overload
    async def trades(
            self,
            market_id: str,
            *,
            params: TradesParams | None = ...,
            raw: Literal[False] = ...,
            authenticated: bool = ...,
    ) -> Trades: ...
    @overload
    async def trades(
            self,
            market_id: str,
            *,
            params: TradesParams | None = ...,
            raw: Literal[True],
            authenticated: bool = ...,
    ) -> dict[str, Any]: ...

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
                market_id,
                params=params
            ),
            raw=raw,
            authenticated=authenticated
        )

    @overload
    async def quotations(
            self,
            market_id: str,
            *,
            params: QuotationParams,
            raw: Literal[False] = ...,
            authenticated: bool = ...,
    ) -> Quotation: ...
    @overload
    async def quotations(
            self,
            market_id: str,
            *,
            params: QuotationParams,
            raw: Literal[True],
            authenticated: bool = ...,
    ) -> dict[str, Any]: ...

    async def quotations(
            self,
            market_id: str,
            *,
            params: QuotationParams,
            raw: bool = False,
            authenticated: bool = False,
    ) -> Quotation | dict[str, Any]:
        return await self._client._request(
            orders.quotation_endpoint(
                market_id,
                params=params
            ),
            raw=raw,
            authenticated=authenticated,
        )


class AsyncPrivateAPI:
    __slots__ = ("_client",)

    def __init__(self, client: AsyncBudaClient):
        self._client: AsyncBudaClient = client

    @overload
    async def me(
            self,
            *,
            raw: Literal[False] = ...
    ) -> UserInfo: ...
    @overload
    async def me(
            self,
            *,
            raw: Literal[True]
    ) -> dict[str, Any]: ...

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


class AsyncBudaClient(BaseClient[AsyncClient]):
    """Asynchronous client for the Buda API."""

    __slots__ = ("private", "public")

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
        self.public = AsyncPublicAPI(self)
        self.private = AsyncPrivateAPI(self)

    async def __aenter__(self) -> AsyncBudaClient:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None: # type: ignore
        await self._client.aclose()

    @overload
    async def _request(
            self,
            endpoint: Endpoint[T],
            *,
            raw: Literal[False] = ...,
            authenticated: bool = ...
    ) -> T: ...
    @overload
    async def _request(
            self,
            endpoint: Endpoint[T],
            *,
            raw: Literal[True],
            authenticated: bool = ...
    ) -> dict[str, Any]: ...

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

        request = self._build_request(endpoint)
        response = await self._client.send(
            request,
            auth=self._auth if authenticated else None
        )
        
        response.raise_for_status()
        
        return (
            response.json() if raw
            else endpoint.model(
                **response.json()
            )
        )

    async def _raw_request(
            self,
            method: str,
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

        response = await self._client.request(
            method,
            path,
            auth=self._auth if authenticated else None,
            **kwargs
        )
        
        response.raise_for_status()
        return response.json()