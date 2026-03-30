from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload, override

from httpx import AsyncClient
from pydantic import BaseModel

from buda_client.auth import BudaAuth
from buda_client.settings import BudaSettings
from buda_client.clients.base import BaseClient
from buda_client.endpoints.base import Endpoint

if TYPE_CHECKING:
    from buda_client.models.account import UserInfo
    from buda_client.models.orders import OrderBook, Trades
    from buda_client.models.markets import Market, MarketList, MarketTicker, TickerList


T = TypeVar("T", bound=BaseModel)


class AsyncBudaClient(BaseClient[AsyncClient]):
    """Asynchronous client for the Buda API."""
    
    def __init__(self, settings: BudaSettings | None = None, auth: BudaAuth | None = None) -> None:
        super().__init__(client=AsyncClient, settings=settings, auth=auth)
    
    async def __aenter__(self) -> AsyncBudaClient:
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._client.aclose()
    
    async def _raw_request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        response = await self._client.request(method, path, auth=self._auth, **kwargs)
        response.raise_for_status()
        return response.json()
    
    @overload
    async def _request(self, endpoint: Endpoint[T], raw: Literal[False] = ...) -> T: ...
    @overload
    async def _request(self, endpoint: Endpoint[T], raw: Literal[True]) -> dict[str, Any]: ...

    @override
    async def _request(self, endpoint: Endpoint[T], raw: bool = False) -> T | dict[str, Any]:
        request = self._build_request(endpoint)
        response = await self._client.send(request, auth=self._auth)
        response.raise_for_status()
        data = response.json()
        return data if raw else endpoint.model(**data)
    
    @overload
    async def me(self, raw: Literal[False] = ...) -> UserInfo: ...
    @overload
    async def me(self, raw: Literal[True]) -> dict[str, Any]: ...

    async def me(self, raw: bool = False) -> UserInfo | dict[str, Any]:
        return await self._request(self._me_endpoint(), raw=raw)
    
    @overload
    async def markets(self, market_id: str, raw: Literal[False] = ...) -> Market: ...
    @overload
    async def markets(self, market_id: None = ..., raw: Literal[False] = ...) -> MarketList: ...
    @overload
    async def markets(self, market_id: str | None = None, raw: Literal[True] = ...) -> dict[str, Any]: ...

    async def markets(self, market_id: str | None = None, raw: bool = False) -> Market | MarketList | dict[str, Any]:
        return await self._request(self._markets_endpoint(market_id), raw=raw)
    
    @overload
    async def tickers(self, market_id: str, raw: Literal[False] = ...) -> MarketTicker: ...
    @overload
    async def tickers(self, market_id: None = ..., raw: Literal[False] = ...) -> TickerList: ...
    @overload
    async def tickers(self, market_id: str | None = None, raw: Literal[True] = ...) -> dict[str, Any]: ...

    async def tickers(self, market_id: str | None = None, raw: bool = False) -> MarketTicker | TickerList | dict[str, Any]:
        return await self._request(self._tickers_endpoint(market_id), raw=raw)
    
    @overload
    async def order_book(self, market_id: str, raw: Literal[False] = ...) -> OrderBook: ...
    @overload
    async def order_book(self, market_id: str, raw: Literal[True] = ...) -> dict[str, Any]: ...

    async def order_book(self, market_id: str, raw: bool = False) -> OrderBook | dict[str, Any]:
        return await self._request(self._order_book_endpoint(market_id), raw=raw)
    
    @overload
    def trades(self, market_id: str, raw: Literal[False] = ...) -> Trades: ...
    @overload
    def trades(self, market_id: str, raw: Literal[True] = ...) -> dict[str, Any]: ...

    def trades(self, market_id: str, raw: bool = False) -> Trades | dict[str, Any]:
        return self._request(self._trades_endpoint(market_id), raw=raw)