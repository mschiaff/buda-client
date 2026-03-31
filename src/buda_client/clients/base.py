from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Annotated, Any, TypeVar

from httpx import AsyncClient, Client, Request
from pydantic import BaseModel

from buda_client.settings import BudaSettings

if TYPE_CHECKING:

    from buda_client.auth import BudaAuth
    from buda_client.endpoints.base import Endpoint


HttpxClient = Annotated[
    Client | AsyncClient,
    "Must be an instance of httpx.Client or httpx.AsyncClient"
]

_T = TypeVar("_T", bound=BaseModel)


class BaseClient[T: HttpxClient](ABC):
    """Base client class for Buda API clients."""

    __slots__ = ("_auth", "_client", "_settings")
    
    def __init__(
            self,
            client: type[T],
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
    
    def _build_request(self, endpoint: Endpoint[Any]) -> Request:
        return self._client.build_request(
            url=endpoint.path,
            json=endpoint.json,
            method=endpoint.method,
            params=endpoint.params,
        )
    
    @abstractmethod
    def _request(
            self,
            endpoint: Endpoint[_T],
            *,
            raw: bool = False,
            authenticated: bool = False
    ) -> _T | dict[str, Any]:
        raise NotImplementedError(
            "Subclasses must implement this method"
        )