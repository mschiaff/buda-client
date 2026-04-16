from collections.abc import Callable
from logging import Logger
from typing import Any

from tenacity import RetryCallState
from tenacity.wait import WaitBaseT

from buda.core.settings import BudaSettings

logger: Logger = ...

RETRYABLE_STATUS_CODES: frozenset[int] = ...


def is_retryable_error(exc: BaseException) -> bool:
    """
    Test whether *exc* is an HTTP error with a retryable status code.
    
    Parameters
    ----------
    exc : BaseException
        The exception to check.
    
    Returns
    -------
    bool
        ``True`` if *exc* is an HTTP error with a retryable
        status code, ``False`` otherwise.
    """
    ...


class _RetryAfterWait:
    """
    Tenacity wait strategy that honours the ``Retry-After`` header.

    If the last exception is a 429 with a ``Retry-After`` header the wait
    time will be *at least* the value specified by the server.  Otherwise
    it falls back to zero so a chained exponential strategy takes over.
    """
    
    def __call__(self, retry_state: RetryCallState) -> float:
        """
        Calculate the wait time based on the ``Retry-After`` header.

        Parameters
        ----------
        retry_state : RetryCallState
            The state of the current retry attempt.

        Returns
        -------
        float
            The wait time in seconds.
        """
        ...


def _build_wait(settings: BudaSettings) -> WaitBaseT:
    """
    Build a combined wait strategy: Retry-After header OR exponential backoff.

    Parameters
    ----------
    settings : BudaSettings
        The settings to use for configuring the wait strategy.

    Returns
    -------
    WaitBaseT
        The combined wait strategy.
    """
    ...


def sync_retry_on_error(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator for synchronous methods that retries on 429 / 500 / 503.

    Reads retry configuration from ``self._settings`` at call time, so each
    client instance can have its own retry policy.

    Parameters
    ----------
    fn : Callable[..., Any]
        The function to decorate.
    
    Returns
    -------
    Callable[..., Any]
        The decorated function with retry logic.
    """
    ...


def async_retry_on_error(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator for async methods that retries on 429 / 500 / 503.

    Same semantics as :func:`sync_retry_on_error` but for coroutines.

    Parameters
    ----------
    fn : Callable[..., Any]
        The function to decorate.

    Returns
    -------
    Callable[..., Any]
        The decorated function with retry logic.
    """
    ...

