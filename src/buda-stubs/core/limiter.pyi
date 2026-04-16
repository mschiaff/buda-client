import asyncio
from collections import deque

from buda.core.settings import BudaSettings

class SyncRateLimiter:
    """
    Proactive sliding-window rate limiter for synchronous requests.

    Tracks per-second (shared) and per-minute (auth vs unauth) request
    timestamps and sleeps when the next request would exceed limits.

    Each ``BudaClient`` instance owns its own limiter, since Buda rate
    limits are scoped per IP (unauthenticated) and per API key (authenticated).
    """

    __slots__ = (
        "_enabled",
        "_lock",
        "_per_minute_auth",
        "_per_minute_auth_limit",
        "_per_minute_unauth",
        "_per_minute_unauth_limit",
        "_per_second",
        "_per_second_limit",
    )

    settings: BudaSettings
    """The settings object containing rate limit configurations."""

    _enabled: bool
    """Whether rate limiting is enabled."""
    _per_second_limit: int
    """Maximum requests per second (shared)."""
    _per_minute_auth_limit: int
    """Maximum requests per minute for authenticated requests."""
    _per_minute_unauth_limit: int
    """Maximum requests per minute for unauthenticated requests."""

    _per_second: deque[float]
    """Timestamps of recent requests for per-second limit."""
    _per_minute_auth: deque[float]
    """Timestamps of recent authenticated requests for per-minute limit."""
    _per_minute_unauth: deque[float]
    """Timestamps of recent unauthenticated requests for per-minute limit."""
    _lock: asyncio.Lock
    """Lock to synchronize access to the limiter state."""

    def __init__(self, settings: BudaSettings) -> None:
        """
        Initialize the SyncRateLimiter with the provided settings.

        Parameters
        ----------
        settings : BudaSettings
            The settings object containing rate limit configurations.
        """
        ...
    
    def _prune(self, window: deque[float], cutoff: float) -> None:
        """
        Remove timestamps from the left of the window that
        are older than the cutoff.

        Parameters
        ----------
        window : deque[float]
            The deque of timestamps to prune.
        cutoff : float
            The cutoff time; timestamps <= this value will be removed.
        """
        ...
    
    def acquire(self, *, authenticated: bool) -> None:
        """
        Acquire the rate limiter for a new request, sleeping if necessary
        to comply with limits.

        Parameters
        ----------
        authenticated : bool
            Whether the request is authenticated.
        """
        ...
    


class AsyncRateLimiter:
    """
    Proactive sliding-window rate limiter for asynchronous requests.

    Same logic as :class:`SyncRateLimiter` but uses ``asyncio.Lock`` and
    ``asyncio.sleep``.
    """
    
    __slots__ = (
        "_enabled",
        "_lock",
        "_per_minute_auth",
        "_per_minute_auth_limit",
        "_per_minute_unauth",
        "_per_minute_unauth_limit",
        "_per_second",
        "_per_second_limit",
    )
    settings: BudaSettings
    """The settings object containing rate limit configurations."""

    _enabled: bool
    """Whether rate limiting is enabled."""
    _per_second_limit: int
    """Maximum requests per second (shared)."""
    _per_minute_auth_limit: int
    """Maximum requests per minute for authenticated requests."""
    _per_minute_unauth_limit: int
    """Maximum requests per minute for unauthenticated requests."""

    _per_second: deque[float]
    """Timestamps of recent requests for per-second limit."""
    _per_minute_auth: deque[float]
    """Timestamps of recent authenticated requests for per-minute limit."""
    _per_minute_unauth: deque[float]
    """Timestamps of recent unauthenticated requests for per-minute limit."""
    _lock: asyncio.Lock
    """Lock to synchronize access to the limiter state."""

    def __init__(self, settings: BudaSettings) -> None:
        """
        Initialize the AsyncRateLimiter with the provided settings.

        Parameters
        ----------
        settings : BudaSettings
            The settings object containing rate limit configurations.
        """
        ...
    
    async def acquire(self, *, authenticated: bool) -> None:
        """
        Acquire the rate limiter for a new request, sleeping if necessary
        to comply with limits.

        Parameters
        ----------
        authenticated : bool
            Whether the request is authenticated.
        """
        ...
