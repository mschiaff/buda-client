from pydantic import WebsocketUrl
from pydantic.dataclasses import dataclass

type BaseUrl = str

@dataclass(frozen=True, kw_only=True, slots=True)
class BudaSettings:
    """Settings for Buda API clients."""

    # REST API Settings
    base_url: BaseUrl
    """Base URL for the Buda API."""
    timeout: float | int
    """Timeout for API requests in seconds."""

    # REST API - Retry Settings (tenacity)
    retry_enabled: bool
    """Enable automatic retry for 429, 500, and 503 HTTP errors."""
    retry_max_attempts: int
    """Maximum number of retry attempts."""
    retry_min_wait: float
    """Minimum wait time between retries in seconds."""
    retry_max_wait: float
    """Maximum wait time between retries in seconds."""
    retry_exponential_base: float
    """Base for exponential backoff between retries."""

    # REST API - Rate Limit Settings
    rate_limit_enabled: bool
    """Enable proactive rate limiting."""
    rate_limit_per_second: int
    """Maximum requests per second (shared across auth/unauth)."""
    rate_limit_auth_per_minute: int
    """Maximum authenticated requests per minute (per API key)."""
    rate_limit_unauth_per_minute: int
    """Maximum unauthenticated requests per minute (per IP)."""

    # WebSocket API Settings
    base_uri: WebsocketUrl
    """Base URI for the Buda WebSocket API."""
    open_timeout: float | None
    """Timeout for opening WebSocket connections in seconds."""
    ping_interval: float | None
    """Interval for sending WebSocket pings in seconds."""
    ping_timeout: float | None
    """Timeout for WebSocket pings in seconds."""
    close_timeout: float | None
    """Timeout for closing WebSocket connections in seconds."""

    # Common Settings
    user_agent: str
    """User-Agent header to use for API requests."""

    def __init__(
        self,
        *,
        base_url: BaseUrl = ...,
        timeout: float | int = ...,
        retry_enabled: bool = ...,
        retry_max_attempts: int = ...,
        retry_min_wait: float = ...,
        retry_max_wait: float = ...,
        retry_exponential_base: float = ...,
        rate_limit_enabled: bool = ...,
        rate_limit_per_second: int = ...,
        rate_limit_auth_per_minute: int = ...,
        rate_limit_unauth_per_minute: int = ...,
        base_uri: WebsocketUrl = ...,
        open_timeout: float | None = ...,
        ping_interval: float | None = ...,
        ping_timeout: float | None = ...,
        close_timeout: float | None = ...,
        user_agent: str = ...,
    ) -> None:
        """
        Initialize the BudaSettings with the provided values.

        Parameters
        ----------
        base_url : BaseUrl, optional
            Base URL for the Buda API (default: "https://www.buda.com/api/v2").
        timeout : float | int, optional
            Timeout for API requests in seconds (default: 10).
        retry_enabled : bool, optional
            Enable automatic retry for 429, 500, and 503 HTTP errors (default: True).
        retry_max_attempts : int, optional
            Maximum number of retry attempts (default: 3).
        retry_min_wait : float, optional
            Minimum wait time between retries in seconds (default: 1.0).
        retry_max_wait : float, optional
            Maximum wait time between retries in seconds (default: 30.0).
        retry_exponential_base : float, optional
            Base for exponential backoff between retries (default: 2.0).
        rate_limit_enabled : bool, optional
            Enable proactive rate limiting (default: True).
        rate_limit_per_second : int, optional
            Maximum requests per second (shared across auth/unauth) (default: 20).
        rate_limit_auth_per_minute : int, optional
            Maximum authenticated requests per minute (per API key) (default: 375).
        rate_limit_unauth_per_minute : int, optional
            Maximum unauthenticated requests per minute (per IP) (default: 120).
        base_uri : WebsocketUrl, optional
            Base URI for the Buda WebSocket API (default: "wss://realtime.buda.com").
        open_timeout : float | None, optional
            Timeout for opening WebSocket connections in seconds (default: 10.0).
        ping_interval : float | None, optional
            Interval for sending WebSocket pings in seconds (default: 10.0).
        ping_timeout : float | None, optional
            Timeout for WebSocket pings in seconds (default: 20.0).
        close_timeout : float | None, optional
            Timeout for closing WebSocket connections in seconds (default: 10.0).
        user_agent : str, optional
            User-Agent header to use for API requests (default: "buda-client/1.0").
        """
        ...

    @property
    def headers(self) -> dict[str, str]:
        """Default headers for API requests."""
        ...
