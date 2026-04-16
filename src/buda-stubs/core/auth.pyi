from collections.abc import Generator

import httpx
from httpx import Request, Response

class BudaAuth(httpx.Auth):
    """Attach Buda HMAC authentication to the Request object."""

    __slots__ = (
        "api_key",
        "api_secret",
    )

    api_key: str
    """The API key for authentication."""
    api_secret: str
    """The API secret for authentication."""

    def __init__(self, api_key: str, api_secret: str) -> None:
        """
        Initialize the BudaAuth with the provided API key and secret.

        Parameters
        ----------
        api_key : str
            The API key for authentication.
        api_secret : str
            The API secret for authentication.
        """
        ...

    def get_nonce(self) -> str:
        """Generate a nonce (timestamp in microseconds)"""
        ...

    def sign(self, request: httpx.Request, nonce: str) -> str:
        """Create the HMAC signature for the request."""
        ...

    def auth_flow(self, request: Request) -> Generator[Request, Response]:
        """Attach the necessary authentication headers to the request."""
        ...
