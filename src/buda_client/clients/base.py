from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any

from httpx import AsyncClient, Client, Request

from buda_client.auth import BudaAuth
from buda_client.settings import BudaSettings

if TYPE_CHECKING:

    from buda_client.endpoints.base import Endpoint
    from buda_client.providers import BudaCredentials


HttpxClient = Annotated[
    Client | AsyncClient,
    "Must be an instance of httpx.Client or httpx.AsyncClient"
]


class BaseClient[T: HttpxClient]:
    """Base client class for Buda API clients."""

    __slots__ = ("_auth", "_client", "_settings")
    
    def __init__(
            self,
            client: type[T],
            settings: BudaSettings | None = None,
            provider: BudaCredentials | None = None,
    ) -> None:
        self._settings: BudaSettings = settings or BudaSettings()
        self._auth: BudaAuth | None = BudaAuth(
            **provider.model_dump()
        ) if provider else None
        self._client: T = client(
            base_url=self._settings.base_url,
            timeout=self._settings.timeout,
            headers=self._settings.headers
        )
    
    def _build_request(self, endpoint: Endpoint[Any]) -> Request:
        return self._client.build_request(
            url=endpoint.path,
            json=endpoint.json,
            method=endpoint.method,
            params=endpoint.params,
        )