from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any

from httpx import AsyncClient, Client, Request

if TYPE_CHECKING:
    from buda_client.core.providers import BudaCredentials
    from buda_client.core.settings import BudaSettings
    from buda_client.rest.endpoints.base import Endpoint


type HttpxClient = Annotated[
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
        from buda_client.core.auth import BudaAuth
        from buda_client.core.settings import BudaSettings

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