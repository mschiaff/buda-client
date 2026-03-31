from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload, override
from warnings import deprecated

from httpx import Client
from pydantic import BaseModel

from buda_client.auth import BudaAuth
from buda_client.settings import BudaSettings
from buda_client.clients.base import BaseClient
from buda_client.endpoints.base import Endpoint
from buda_client.endpoints import markets, account, orders

if TYPE_CHECKING:
    from buda_client.models.account import UserInfo
    from buda_client.models.orders import OrderBook, Trades, Quotation
    from buda_client.models.markets import Market, MarketList, MarketTicker, TickerList
    
    from buda_client.endpoints.orders import TradesParams, QuotationParams


T = TypeVar("T", bound=BaseModel)


class PublicAPI:
    __slots__ = ("_client",)

    def __init__(self, client: BudaClient):
        self._client: BudaClient = client

    @overload
    def markets(self, market_id: str, *, raw: Literal[False] = ..., authenticated: bool = ...) -> Market: ...
    @overload
    def markets(self, market_id: None = ..., *, raw: Literal[False] = ..., authenticated: bool = ...) -> MarketList: ...
    @overload
    def markets(self, market_id: str | None = None, *, raw: Literal[True], authenticated: bool = ...) -> dict[str, Any]: ...
    
    def markets(self, market_id: str | None = None, *, raw: bool = False, authenticated: bool = False) -> Market | MarketList | dict[str, Any]:
        return self._client._request(markets.markets_endpoint(market_id), raw=raw, authenticated=authenticated)
    
    @overload
    def tickers(self, market_id: str, *, raw: Literal[False] = ..., authenticated: bool = ...) -> MarketTicker: ...
    @overload
    def tickers(self, market_id: None = ..., *, raw: Literal[False] = ..., authenticated: bool = ...) -> TickerList: ...
    @overload
    def tickers(self, market_id: str | None = None, *, raw: Literal[True], authenticated: bool = ...) -> dict[str, Any]: ...
    
    def tickers(self, market_id: str | None = None, *, raw: bool = False, authenticated: bool = False) -> MarketTicker | TickerList | dict[str, Any]:
        return self._client._request(markets.tickers_endpoint(market_id), raw=raw, authenticated=authenticated)
    
    @overload
    def order_book(self, market_id: str, *, raw: Literal[False] = ..., authenticated: bool = ...) -> OrderBook: ...
    @overload
    def order_book(self, market_id: str, *, raw: Literal[True], authenticated: bool = ...) -> dict[str, Any]: ...
    
    def order_book(self, market_id: str, *, raw: bool = False, authenticated: bool = False) -> OrderBook | dict[str, Any]:
        return self._client._request(orders.order_book_endpoint(market_id), raw=raw, authenticated=authenticated)
    
    @overload
    @deprecated("Authenticated trades requests with query params return 401. Use authenticated=False (default) when passing params.")
    def trades(self, market_id: str, *, params: TradesParams, authenticated: Literal[True], raw: Literal[False] = ...) -> Trades: ...

    @overload
    @deprecated("Authenticated trades requests with query params return 401. Use authenticated=False (default) when passing params.")
    def trades(self, market_id: str, *, params: TradesParams, authenticated: Literal[True], raw: Literal[True]) -> dict[str, Any]: ...
    
    @overload
    def trades(self, market_id: str, *, params: TradesParams | None = ..., raw: Literal[False] = ..., authenticated: bool = ...) -> Trades: ...
    @overload
    def trades(self, market_id: str, *, params: TradesParams | None = ..., raw: Literal[True], authenticated: bool = ...) -> dict[str, Any]: ...
    
    def trades(self, market_id: str, *, params: TradesParams | None = None, raw: bool = False, authenticated: bool = False) -> Trades | dict[str, Any]:
        return self._client._request(orders.trades_endpoint(market_id, params=params), raw=raw, authenticated=authenticated)
    
    @overload
    def quotations(self, market_id: str, *, params: QuotationParams, raw: Literal[False] = ..., authenticated: bool = ...) -> Quotation: ...
    @overload
    def quotations(self, market_id: str, *, params: QuotationParams, raw: Literal[True], authenticated: bool = ...) -> dict[str, Any]: ...
    
    def quotations(self, market_id: str, *, params: QuotationParams, raw: bool = False, authenticated: bool = False) -> Quotation | dict[str, Any]:
        return self._client._request(orders.quotation_endpoint(market_id, params=params), raw=raw, authenticated=authenticated)


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


class BudaClient(BaseClient[Client]):
    """Synchronous client for the Buda API."""

    __slots__ = ("public", "private")
    
    def __init__(self, settings: BudaSettings | None = None, auth: BudaAuth | None = None) -> None:
        super().__init__(client=Client, settings=settings, auth=auth)
        self.public = PublicAPI(self)
        self.private = PrivateAPI(self)
    
    def __enter__(self) -> BudaClient:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._client.close()
    
    @overload
    @override
    def _request(self, endpoint: Endpoint[T], *, raw: Literal[False] = ..., authenticated: bool = ...) -> T: ...
    @overload
    @override
    def _request(self, endpoint: Endpoint[T], *, raw: Literal[True], authenticated: bool = ...) -> dict[str, Any]: ...

    @override
    def _request(self, endpoint: Endpoint[T], *, raw: bool = False, authenticated: bool = False) -> T | dict[str, Any]:
        if authenticated and not self._auth:
            raise ValueError("Authentication was requested, but no auth credentials were provided.")
        
        request = self._build_request(endpoint)
        response = self._client.send(request, auth=self._auth if authenticated else None)
        response.raise_for_status()
        return response.json() if raw else endpoint.model(**response.json())
    
    def _raw_request(self, method: str, path: str, *, authenticated: bool = False, **kwargs: Any) -> dict[str, Any]:
        if authenticated and not self._auth:
            raise ValueError("Authentication was requested, but no auth credentials were provided.")
        
        response = self._client.request(method, path, auth=self._auth if authenticated else None, **kwargs)
        response.raise_for_status()
        return response.json()