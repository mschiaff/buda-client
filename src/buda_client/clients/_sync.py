from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload, override

from httpx import Client
from pydantic import BaseModel

from buda_client.auth import BudaAuth
from buda_client.settings import BudaSettings
from buda_client.clients.base import BaseClient
from buda_client.endpoints.base import Endpoint

if TYPE_CHECKING:
    from buda_client.models.account import UserInfo
    from buda_client.models.markets import Market, MarketList, MarketTicker, TickerList


T = TypeVar("T", bound=BaseModel)


class BudaClient(BaseClient[Client]):
    """Synchronous client for the Buda API."""
    
    def __init__(self, settings: BudaSettings | None = None, auth: BudaAuth | None = None) -> None:
        super().__init__(client=Client, settings=settings, auth=auth)
    
    def __enter__(self) -> BudaClient:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._client.close()
    
    def _raw_request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        response = self._client.request(method, path, auth=self._auth, **kwargs)
        response.raise_for_status()
        return response.json()
    
    @overload
    def _request(self, endpoint: Endpoint[T], raw: Literal[False] = ...) -> T: ...
    @overload
    def _request(self, endpoint: Endpoint[T], raw: Literal[True]) -> dict[str, Any]: ...

    @override
    def _request(self, endpoint: Endpoint[T], raw: bool = False) -> T | dict[str, Any]:
        request = self._build_request(endpoint)
        response = self._client.send(request, auth=self._auth)
        response.raise_for_status()
        data = response.json()
        return data if raw else endpoint.model(**data)
    
    @overload
    def me(self, raw: Literal[False] = ...) -> UserInfo: ...
    @overload
    def me(self, raw: Literal[True]) -> dict[str, Any]: ...

    def me(self, raw: bool = False) -> UserInfo | dict[str, Any]:
        return self._request(self._me_endpoint(), raw=raw)
    
    @overload
    def markets(self, market_id: str, raw: Literal[False] = ...) -> Market: ...
    @overload
    def markets(self, market_id: None = ..., raw: Literal[False] = ...) -> MarketList: ...
    @overload
    def markets(self, market_id: str | None = None, raw: Literal[True] = ...) -> dict[str, Any]: ...

    def markets(self, market_id: str | None = None, raw: bool = False) -> Market | MarketList | dict[str, Any]:
        return self._request(self._markets_endpoint(market_id), raw=raw)
    
    @overload
    def tickers(self, market_id: str, raw: Literal[False] = ...) -> MarketTicker: ...
    @overload
    def tickers(self, market_id: None = ..., raw: Literal[False] = ...) -> TickerList: ...
    @overload
    def tickers(self, market_id: str | None = None, raw: Literal[True] = ...) -> dict[str, Any]: ...

    def tickers(self, market_id: str | None = None, raw: bool = False) -> MarketTicker | TickerList | dict[str, Any]:
        return self._request(self._tickers_endpoint(market_id), raw=raw)