from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Annotated, Any

from httpx import Client, AsyncClient, Request

from buda_client.auth import BudaAuth
from buda_client.settings import BudaSettings
from buda_client.endpoints.base import Endpoint
from buda_client.endpoints.markets import MarketEndpoints


HttpxClientType = Annotated[
    type[Client] | type[AsyncClient],
    "Must be either type httpx.Client or httpx.AsyncClient"
]

HttpxClient = Annotated[
    Client | AsyncClient,
    "Must be an instance of httpx.Client or httpx.AsyncClient"
]


class BaseClient[T: HttpxClient](MarketEndpoints, ABC):
    """Base client class for Buda API clients."""
    
    def __init__(
            self,
            client: HttpxClientType,
            settings: BudaSettings | None = None,
            auth: BudaAuth | None = None,
    ) -> None:
        self._settings: BudaSettings = settings or BudaSettings()
        self._auth: BudaAuth | None = auth
        self._client: T = client(
            base_url=self._settings.base_url,
            timeout=self._settings.timeout,
            headers=self._settings.headers
        )
    
    @abstractmethod
    def _request(self, endpoint: Endpoint, raw: bool = False):
        raise NotImplementedError("Subclasses must implement this method")
    
    def _build_request(self, endpoint: Endpoint[Any]) -> Request:
        return self._client.build_request(
            url=endpoint.path,
            json=endpoint.json,
            method=endpoint.method,
            params=endpoint.params,
        )