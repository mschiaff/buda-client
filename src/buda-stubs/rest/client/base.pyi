from typing import Any

from httpx import AsyncClient, Client, Request

from buda.core.auth import BudaAuth
from buda.core.providers import BudaCredentials
from buda.core.settings import BudaSettings
from buda.rest.endpoints.base import Endpoint

HttpxClient = Client | AsyncClient

class BaseClient[T: HttpxClient]:
    """Base client class for Buda API clients."""

    __slots__ = (
        "_auth",
        "_client",
        "_settings",
    )

    _auth: BudaAuth | None
    """The credentials used for authentication, if any."""
    _client: T
    """The underlying HTTP client (httpx.Client or httpx.AsyncClient)."""
    _settings: BudaSettings
    """The settings object containing client configurations."""

    def __init__(
        self,
        client: type[T],
        settings: BudaSettings | None = ...,
        provider: BudaCredentials | None = ...,
    ) -> None:
        """
        Initialize the BaseClient with the provided HTTP client type, settings, and credentials.

        Parameters
        ----------
        client : type[T]
            The HTTP client class to use (httpx.Client or httpx.AsyncClient).
        settings : BudaSettings | None, optional
            The settings object containing client configurations, by default None.
        provider : BudaCredentials | None, optional
            The credentials used for authentication, if any, by default None.
        """
        ...

    def _build_request(self, endpoint: Endpoint[Any]) -> Request:
        """
        Build an HTTP request for the given endpoint.

        Parameters
        ----------
        endpoint : Endpoint[Any]
            The endpoint for which to build the request.

        Returns
        -------
        Request
            The constructed HTTP request.
        """
        ...
