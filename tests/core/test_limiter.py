# pyright: reportPrivateUsage=false

from __future__ import annotations

from collections import deque
from unittest.mock import AsyncMock, patch

from buda.core.limiter import AsyncRateLimiter, SyncRateLimiter
from buda.core.settings import BudaSettings

# ── Sync Rate Limiter ──────────────────────────────────────────────

class TestSyncRateLimiterDisabled:
    def test_acquire_returns_immediately_when_disabled(self):
        settings = BudaSettings(rate_limit_enabled=False)
        limiter = SyncRateLimiter(settings)
        limiter.acquire(authenticated=False)  # Should not raise or block


class TestSyncRateLimiterPrune:
    def test_prune_removes_expired(self):
        settings = BudaSettings(rate_limit_enabled=True)
        limiter = SyncRateLimiter(settings)
        window: deque[float] = deque([1.0, 2.0, 3.0, 4.0, 5.0])
        limiter._prune(window, 3.0)
        assert list(window) == [4.0, 5.0]

    def test_prune_empty_deque(self):
        settings = BudaSettings(rate_limit_enabled=True)
        limiter = SyncRateLimiter(settings)
        window: deque[float] = deque()
        limiter._prune(window, 5.0)
        assert len(window) == 0

    def test_prune_nothing_expired(self):
        settings = BudaSettings(rate_limit_enabled=True)
        limiter = SyncRateLimiter(settings)
        window: deque[float] = deque([10.0, 11.0])
        limiter._prune(window, 5.0)
        assert list(window) == [10.0, 11.0]


class TestSyncRateLimiterAcquire:
    def test_acquire_no_sleep_when_under_limit(self):
        settings = BudaSettings(rate_limit_per_second=20)
        limiter = SyncRateLimiter(settings)
        with patch("buda.core.limiter.time.sleep") as mock_sleep:
            limiter.acquire(authenticated=False)
            mock_sleep.assert_not_called()

    def test_acquire_records_timestamp(self):
        settings = BudaSettings(rate_limit_per_second=20)
        limiter = SyncRateLimiter(settings)
        limiter.acquire(authenticated=False)
        assert len(limiter._per_second) == 1
        assert len(limiter._per_minute_unauth) == 1
        assert len(limiter._per_minute_auth) == 0

    def test_acquire_authenticated_records_auth_timestamp(self):
        settings = BudaSettings(rate_limit_per_second=20)
        limiter = SyncRateLimiter(settings)
        limiter.acquire(authenticated=True)
        assert len(limiter._per_second) == 1
        assert len(limiter._per_minute_auth) == 1
        assert len(limiter._per_minute_unauth) == 0

    def test_acquire_sleeps_when_per_second_exceeded(self):
        settings = BudaSettings(rate_limit_per_second=2)
        limiter = SyncRateLimiter(settings)

        # Simulate 2 requests at time 100.0
        now = 100.0
        limiter._per_second = deque([now, now])
        limiter._per_minute_unauth = deque([now, now])

        with (
            patch("buda.core.limiter.time.monotonic", side_effect=[now, now + 1.1]),
            patch("buda.core.limiter.time.sleep") as mock_sleep,
        ):
            limiter.acquire(authenticated=False)
            mock_sleep.assert_called_once()


# ── Async Rate Limiter ─────────────────────────────────────────────

class TestAsyncRateLimiterDisabled:
    async def test_acquire_returns_immediately_when_disabled(self):
        settings = BudaSettings(rate_limit_enabled=False)
        limiter = AsyncRateLimiter(settings)
        await limiter.acquire(authenticated=False)


class TestAsyncRateLimiterAcquire:
    async def test_acquire_no_sleep_when_under_limit(self):
        settings = BudaSettings(rate_limit_per_second=20)
        limiter = AsyncRateLimiter(settings)
        with patch("buda.core.limiter.asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            await limiter.acquire(authenticated=False)
            mock_sleep.assert_not_called()

    async def test_acquire_records_timestamp(self):
        settings = BudaSettings(rate_limit_per_second=20)
        limiter = AsyncRateLimiter(settings)
        await limiter.acquire(authenticated=False)
        assert len(limiter._per_second) == 1
        assert len(limiter._per_minute_unauth) == 1

    async def test_acquire_authenticated_records_auth_timestamp(self):
        settings = BudaSettings(rate_limit_per_second=20)
        limiter = AsyncRateLimiter(settings)
        await limiter.acquire(authenticated=True)
        assert len(limiter._per_second) == 1
        assert len(limiter._per_minute_auth) == 1
        assert len(limiter._per_minute_unauth) == 0

    async def test_acquire_sleeps_when_per_second_exceeded(self):
        settings = BudaSettings(rate_limit_per_second=2)
        limiter = AsyncRateLimiter(settings)

        now = 100.0
        limiter._per_second = deque([now, now])
        limiter._per_minute_unauth = deque([now, now])

        with (
            patch("buda.core.limiter.time.monotonic", side_effect=[now, now + 1.1]),
            patch("buda.core.limiter.asyncio.sleep", new_callable=AsyncMock) as mock_sleep,
        ):
            await limiter.acquire(authenticated=False)
            mock_sleep.assert_called_once()
