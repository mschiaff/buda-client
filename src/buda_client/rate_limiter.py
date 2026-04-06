from __future__ import annotations

import asyncio
import logging
import threading
import time
from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from buda_client.settings import BudaSettings

logger = logging.getLogger("buda_client.rate_limiter")


class SyncRateLimiter:
    """Proactive sliding-window rate limiter for synchronous requests.

    Tracks per-second (shared) and per-minute (auth vs unauth) request
    timestamps and sleeps when the next request would exceed limits.

    Each ``BudaClient`` instance owns its own limiter, which is correct
    since Buda rate limits are scoped per IP (unauthenticated) and per
    API key (authenticated).
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

    def __init__(self, settings: BudaSettings) -> None:
        self._enabled = settings.rate_limit_enabled
        self._per_second_limit = settings.rate_limit_per_second
        self._per_minute_auth_limit = settings.rate_limit_auth_per_minute
        self._per_minute_unauth_limit = settings.rate_limit_unauth_per_minute

        self._per_second: deque[float] = deque()
        self._per_minute_auth: deque[float] = deque()
        self._per_minute_unauth: deque[float] = deque()
        self._lock = threading.Lock()

    def _prune(self, window: deque[float], cutoff: float) -> None:
        while window and window[0] <= cutoff:
            window.popleft()

    def acquire(self, *, authenticated: bool) -> None:
        if not self._enabled:
            return

        with self._lock:
            while True:
                now = time.monotonic()

                # Prune expired timestamps
                self._prune(self._per_second, now - 1.0)
                if authenticated:
                    self._prune(self._per_minute_auth, now - 60.0)
                else:
                    self._prune(self._per_minute_unauth, now - 60.0)

                # Calculate how long we need to wait (if at all)
                wait = 0.0

                if len(self._per_second) >= self._per_second_limit:
                    wait = max(wait, self._per_second[0] + 1.0 - now)

                if authenticated:
                    if len(self._per_minute_auth) >= self._per_minute_auth_limit:
                        wait = max(wait, self._per_minute_auth[0] + 60.0 - now)
                else:
                    if len(self._per_minute_unauth) >= self._per_minute_unauth_limit:
                        wait = max(wait, self._per_minute_unauth[0] + 60.0 - now)

                if wait > 0:
                    logger.warning(
                        "Rate limit approaching — sleeping %.2fs before request "
                        "(authenticated=%s)",
                        wait,
                        authenticated,
                    )
                    # Release lock while sleeping so other threads aren't blocked
                    self._lock.release()
                    try:
                        time.sleep(wait)
                    finally:
                        self._lock.acquire()
                    continue  # Re-check after sleeping

                # Record the request timestamp
                self._per_second.append(now)
                if authenticated:
                    self._per_minute_auth.append(now)
                else:
                    self._per_minute_unauth.append(now)
                return


class AsyncRateLimiter:
    """Proactive sliding-window rate limiter for asynchronous requests.

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

    def __init__(self, settings: BudaSettings) -> None:
        self._enabled = settings.rate_limit_enabled
        self._per_second_limit = settings.rate_limit_per_second
        self._per_minute_auth_limit = settings.rate_limit_auth_per_minute
        self._per_minute_unauth_limit = settings.rate_limit_unauth_per_minute

        self._per_second: deque[float] = deque()
        self._per_minute_auth: deque[float] = deque()
        self._per_minute_unauth: deque[float] = deque()
        self._lock = asyncio.Lock()

    def _prune(self, window: deque[float], cutoff: float) -> None:
        while window and window[0] <= cutoff:
            window.popleft()

    async def acquire(self, *, authenticated: bool) -> None:
        if not self._enabled:
            return

        async with self._lock:
            while True:
                now = time.monotonic()

                self._prune(self._per_second, now - 1.0)
                if authenticated:
                    self._prune(self._per_minute_auth, now - 60.0)
                else:
                    self._prune(self._per_minute_unauth, now - 60.0)

                wait = 0.0

                if len(self._per_second) >= self._per_second_limit:
                    wait = max(wait, self._per_second[0] + 1.0 - now)

                if authenticated:
                    if len(self._per_minute_auth) >= self._per_minute_auth_limit:
                        wait = max(wait, self._per_minute_auth[0] + 60.0 - now)
                else:
                    if len(self._per_minute_unauth) >= self._per_minute_unauth_limit:
                        wait = max(wait, self._per_minute_unauth[0] + 60.0 - now)

                if wait > 0:
                    logger.warning(
                        "Rate limit approaching — sleeping %.2fs before request "
                        "(authenticated=%s)",
                        wait,
                        authenticated,
                    )
                    await asyncio.sleep(wait)
                    continue

                self._per_second.append(now)
                if authenticated:
                    self._per_minute_auth.append(now)
                else:
                    self._per_minute_unauth.append(now)
                return
