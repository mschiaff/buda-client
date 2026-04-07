# pyright: reportPrivateUsage=false

from __future__ import annotations

from unittest.mock import MagicMock

import httpx
import pytest
from tenacity import RetryCallState

from buda.core.retry import (
    _build_wait,
    _RetryAfterWait,
    async_retry_on_error,
    is_retryable_error,
    sync_retry_on_error,
)
from buda.core.settings import BudaSettings


def _make_http_status_error(
    status_code: int, headers: dict[str, str] | None = None
) -> httpx.HTTPStatusError:
    request = httpx.Request("GET", "https://test.com")
    response = httpx.Response(status_code, request=request, headers=headers or {})
    return httpx.HTTPStatusError(
        message=f"HTTP {status_code}",
        request=request,
        response=response,
    )


class TestIsRetryableError:
    def test_429_is_retryable(self):
        assert is_retryable_error(_make_http_status_error(429)) is True

    def test_500_is_retryable(self):
        assert is_retryable_error(_make_http_status_error(500)) is True

    def test_503_is_retryable(self):
        assert is_retryable_error(_make_http_status_error(503)) is True

    def test_400_not_retryable(self):
        assert is_retryable_error(_make_http_status_error(400)) is False

    def test_401_not_retryable(self):
        assert is_retryable_error(_make_http_status_error(401)) is False

    def test_404_not_retryable(self):
        assert is_retryable_error(_make_http_status_error(404)) is False

    def test_non_http_error_not_retryable(self):
        assert is_retryable_error(ValueError("nope")) is False

    def test_runtime_error_not_retryable(self):
        assert is_retryable_error(RuntimeError()) is False


class TestRetryAfterWait:
    def _make_retry_state(self, exc: BaseException | None) -> RetryCallState:
        state = MagicMock(spec=RetryCallState)
        outcome = MagicMock()
        outcome.exception.return_value = exc
        state.outcome = outcome
        return state

    def test_returns_retry_after_for_429(self):
        wait = _RetryAfterWait()
        exc = _make_http_status_error(429, headers={"Retry-After": "5"})
        state = self._make_retry_state(exc)
        assert wait(state) == 5.0

    def test_returns_zero_for_429_without_header(self):
        wait = _RetryAfterWait()
        exc = _make_http_status_error(429)
        state = self._make_retry_state(exc)
        assert wait(state) == 0.0

    def test_returns_zero_for_non_429(self):
        wait = _RetryAfterWait()
        exc = _make_http_status_error(500)
        state = self._make_retry_state(exc)
        assert wait(state) == 0.0

    def test_returns_zero_for_non_http_error(self):
        wait = _RetryAfterWait()
        state = self._make_retry_state(ValueError("bad"))
        assert wait(state) == 0.0

    def test_returns_zero_for_invalid_retry_after(self):
        wait = _RetryAfterWait()
        exc = _make_http_status_error(429, headers={"Retry-After": "not-a-number"})
        state = self._make_retry_state(exc)
        assert wait(state) == 0.0

    def test_returns_zero_when_no_outcome(self):
        wait = _RetryAfterWait()
        state = MagicMock(spec=RetryCallState)
        state.outcome = None
        assert wait(state) == 0.0


class TestBuildWait:
    def test_returns_wait_strategy(self):
        settings = BudaSettings()
        wait = _build_wait(settings)
        assert wait is not None


class TestSyncRetryDecorator:
    def test_retries_on_429_then_succeeds(self):
        call_count = 0

        class FakeClient:
            _settings = BudaSettings(retry_max_attempts=3, retry_min_wait=0.01, retry_max_wait=0.1)

            @sync_retry_on_error
            def do_request(self):
                nonlocal call_count
                call_count += 1
                if call_count < 2:
                    raise _make_http_status_error(429, headers={"Retry-After": "0"})
                return "success"

        result = FakeClient().do_request()
        assert result == "success"
        assert call_count == 2

    def test_raises_after_max_attempts(self):
        class FakeClient:
            _settings = BudaSettings(retry_max_attempts=2, retry_min_wait=0.01, retry_max_wait=0.1)

            @sync_retry_on_error
            def do_request(self):
                raise _make_http_status_error(500)

        with pytest.raises(httpx.HTTPStatusError):
            FakeClient().do_request()

    def test_non_retryable_error_passes_through(self):
        class FakeClient:
            _settings = BudaSettings(retry_max_attempts=3)

            @sync_retry_on_error
            def do_request(self):
                raise _make_http_status_error(401)

        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            FakeClient().do_request()
        assert exc_info.value.response.status_code == 401

    def test_no_retry_when_disabled(self):
        call_count = 0

        class FakeClient:
            _settings = BudaSettings(retry_enabled=False)

            @sync_retry_on_error
            def do_request(self):
                nonlocal call_count
                call_count += 1
                return "direct"

        result = FakeClient().do_request()
        assert result == "direct"
        assert call_count == 1


class TestAsyncRetryDecorator:
    async def test_retries_on_503_then_succeeds(self):
        call_count = 0

        class FakeClient:
            _settings = BudaSettings(retry_max_attempts=3, retry_min_wait=0.01, retry_max_wait=0.1)

            @async_retry_on_error
            async def do_request(self):
                nonlocal call_count
                call_count += 1
                if call_count < 2:
                    raise _make_http_status_error(503)
                return "success"

        result = await FakeClient().do_request()
        assert result == "success"
        assert call_count == 2

    async def test_raises_after_max_attempts(self):
        class FakeClient:
            _settings = BudaSettings(retry_max_attempts=2, retry_min_wait=0.01, retry_max_wait=0.1)

            @async_retry_on_error
            async def do_request(self):
                raise _make_http_status_error(429, headers={"Retry-After": "0"})

        with pytest.raises(httpx.HTTPStatusError):
            await FakeClient().do_request()

    async def test_no_retry_when_disabled(self):
        class FakeClient:
            _settings = BudaSettings(retry_enabled=False)

            @async_retry_on_error
            async def do_request(self):
                return "direct"

        result = await FakeClient().do_request()
        assert result == "direct"
