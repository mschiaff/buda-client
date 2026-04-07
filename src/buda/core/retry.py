from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING, Any

from httpx import HTTPStatusError
from tenacity import (
    AsyncRetrying,
    RetryCallState,
    Retrying,
    before_sleep_log,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from tenacity.wait import WaitBaseT

    from buda.core.settings import BudaSettings

logger = logging.getLogger("buda.retry")

RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({429, 500, 503})


def is_retryable_error(exc: BaseException) -> bool:
    """Return ``True`` if *exc* is an HTTP error with a retryable status code."""
    return isinstance(exc, HTTPStatusError) and exc.response.status_code in RETRYABLE_STATUS_CODES


class _RetryAfterWait:
    """Tenacity wait strategy that honours the ``Retry-After`` header.

    If the last exception is a 429 with a ``Retry-After`` header the wait
    time will be *at least* the value specified by the server.  Otherwise
    it falls back to zero so a chained exponential strategy takes over.
    """

    def __call__(self, retry_state: RetryCallState) -> float:
        exc = retry_state.outcome and retry_state.outcome.exception()
        if isinstance(exc, HTTPStatusError) and exc.response.status_code == 429:
            retry_after = exc.response.headers.get("Retry-After")
            if retry_after is not None:
                try:
                    wait = float(retry_after)
                    logger.info(
                        "Server returned Retry-After: %.2fs — will wait at least that long",
                        wait,
                    )
                    return wait
                except (ValueError, OverflowError):
                    pass
        return 0.0


def _build_wait(settings: BudaSettings) -> WaitBaseT:
    """Build a combined wait strategy: Retry-After header OR exponential backoff."""
    retry_after: Any = _RetryAfterWait()
    exponential: Any = wait_exponential(
        min=settings.retry_min_wait,
        max=settings.retry_max_wait,
        exp_base=settings.retry_exponential_base,
    )
    # For each attempt pick the larger of [Retry-After header, exponential backoff].
    return retry_after + exponential


def sync_retry_on_error(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for synchronous methods that retries on 429 / 500 / 503.

    Reads retry configuration from ``self._settings`` at call time, so each
    client instance can have its own retry policy.
    """

    @functools.wraps(fn)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        if not self._settings.retry_enabled:
            return fn(self, *args, **kwargs)
        retrying = Retrying(
            retry=retry_if_exception(is_retryable_error),
            stop=stop_after_attempt(self._settings.retry_max_attempts),
            wait=_build_wait(self._settings),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        )
        return retrying(fn, self, *args, **kwargs)

    return wrapper


def async_retry_on_error(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for async methods that retries on 429 / 500 / 503.

    Same semantics as :func:`sync_retry_on_error` but for coroutines.
    """

    @functools.wraps(fn)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        if not self._settings.retry_enabled:
            return await fn(self, *args, **kwargs)
        retrying = AsyncRetrying(
            retry=retry_if_exception(is_retryable_error),
            stop=stop_after_attempt(self._settings.retry_max_attempts),
            wait=_build_wait(self._settings),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        )
        return await retrying(fn, self, *args, **kwargs)

    return wrapper
