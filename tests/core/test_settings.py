from __future__ import annotations

import pytest
from pydantic import ValidationError

from buda.core.settings import BudaSettings


class TestBudaSettingsDefaults:
    def test_default_base_url(self, default_settings: BudaSettings):
        assert "buda.com/api/v2" in default_settings.base_url

    def test_default_timeout(self, default_settings: BudaSettings):
        assert default_settings.timeout == 10.0

    def test_default_retry_enabled(self, default_settings: BudaSettings):
        assert default_settings.retry_enabled is True

    def test_default_retry_max_attempts(self, default_settings: BudaSettings):
        assert default_settings.retry_max_attempts == 3

    def test_default_retry_min_wait(self, default_settings: BudaSettings):
        assert default_settings.retry_min_wait == 1.0

    def test_default_retry_max_wait(self, default_settings: BudaSettings):
        assert default_settings.retry_max_wait == 30.0

    def test_default_retry_exponential_base(self, default_settings: BudaSettings):
        assert default_settings.retry_exponential_base == 2.0

    def test_default_rate_limit_enabled(self, default_settings: BudaSettings):
        assert default_settings.rate_limit_enabled is True

    def test_default_rate_limit_per_second(self, default_settings: BudaSettings):
        assert default_settings.rate_limit_per_second == 20

    def test_default_rate_limit_auth_per_minute(self, default_settings: BudaSettings):
        assert default_settings.rate_limit_auth_per_minute == 375

    def test_default_rate_limit_unauth_per_minute(self, default_settings: BudaSettings):
        assert default_settings.rate_limit_unauth_per_minute == 120

    def test_default_websocket_settings(self, default_settings: BudaSettings):
        assert default_settings.open_timeout == 10.0
        assert default_settings.ping_interval == 10.0
        assert default_settings.ping_timeout == 20.0
        assert default_settings.close_timeout == 10.0

    def test_default_user_agent(self, default_settings: BudaSettings):
        assert default_settings.user_agent == "python-buda-client/0.1.0"


class TestBudaSettingsCustom:
    def test_custom_timeout(self):
        s = BudaSettings(timeout=30.0)
        assert s.timeout == 30.0

    def test_custom_retry_disabled(self):
        s = BudaSettings(retry_enabled=False)
        assert s.retry_enabled is False

    def test_custom_rate_limit_disabled(self):
        s = BudaSettings(rate_limit_enabled=False)
        assert s.rate_limit_enabled is False

    def test_custom_rate_limits(self):
        s = BudaSettings(
            rate_limit_per_second=10,
            rate_limit_auth_per_minute=100,
            rate_limit_unauth_per_minute=50,
        )
        assert s.rate_limit_per_second == 10
        assert s.rate_limit_auth_per_minute == 100
        assert s.rate_limit_unauth_per_minute == 50

    def test_custom_retry_values(self):
        s = BudaSettings(
            retry_max_attempts=5,
            retry_min_wait=2.0,
            retry_max_wait=60.0,
            retry_exponential_base=3.0,
        )
        assert s.retry_max_attempts == 5
        assert s.retry_min_wait == 2.0
        assert s.retry_max_wait == 60.0
        assert s.retry_exponential_base == 3.0

    def test_websocket_none_timeouts(self):
        s = BudaSettings(
            open_timeout=None,
            ping_interval=None,
            ping_timeout=None,
            close_timeout=None,
        )
        assert s.open_timeout is None
        assert s.ping_interval is None
        assert s.ping_timeout is None
        assert s.close_timeout is None

    def test_integer_timeout(self):
        s = BudaSettings(timeout=5)
        assert s.timeout == 5


class TestBudaSettingsImmutability:
    def test_frozen_raises_on_mutation(self, default_settings: BudaSettings):
        with pytest.raises(Exception):  # noqa: B017
            default_settings.timeout = 99.0  # type: ignore[misc]


class TestBudaSettingsHeaders:
    def test_headers_property(self, default_settings: BudaSettings):
        headers = default_settings.headers
        assert headers == {"User-Agent": "python-buda-client/0.1.0"}

    def test_custom_user_agent_in_headers(self):
        s = BudaSettings(user_agent="custom-agent/1.0")
        assert s.headers == {"User-Agent": "custom-agent/1.0"}


class TestBudaSettingsUrlValidation:
    def test_valid_base_url(self):
        s = BudaSettings(base_url="https://example.com/api")
        assert "example.com" in s.base_url

    def test_invalid_base_url_raises(self):
        with pytest.raises(ValidationError):
            BudaSettings(base_url="not-a-url")
