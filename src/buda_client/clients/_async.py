from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar, overload, override

from httpx import AsyncClient
from pydantic import BaseModel

from buda_client.auth import BudaAuth
from buda_client.settings import BudaSettings
from buda_client.clients.base import BaseClient
from buda_client.endpoints.base import Endpoint

if TYPE_CHECKING:
    from buda_client.models.markets import Ticker


T = TypeVar("T", bound=BaseModel)


class AsyncBudaClient(BaseClient[AsyncClient]):
    """Asynchronous client for the Buda API."""
    
    def __init__(self, settings: BudaSettings | None = None, auth: BudaAuth | None = None) -> None:
        super().__init__(client=AsyncClient, settings=settings, auth=auth)
    
    @overload
    async def _request(self, endpoint: Endpoint[T], raw: bool = False) -> T: ...
    @overload
    async def _request(self, endpoint: Endpoint[None]) -> dict[str, Any]: ...
    @overload
    async def _request(self, endpoint: Endpoint[None], raw: bool = ...) -> dict[str, Any]: ...
    @overload
    async def _request(self, endpoint: Endpoint[T], raw: bool = True) -> dict[str, Any]: ...

    @override
    async def _request(self, endpoint: Endpoint[T | None], raw: bool = False) -> T | dict[str, Any]:
        request = self._build_request(endpoint)
        response = await self._client.send(request, auth=self._auth)
        response.raise_for_status()
        data = response.json()
        return data if raw or not endpoint.model else endpoint.model(**data)
    
    async def ticker(self, market_id: str, raw: bool = False) -> Ticker | dict[str, Any]:
        return await self._request(self._ticker_endpoint(market_id), raw=raw)