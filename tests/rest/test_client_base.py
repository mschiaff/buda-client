# pyright: reportPrivateUsage=false

from __future__ import annotations

from httpx import Client

from buda.core.providers import StaticCredentials
from buda.core.settings import BudaSettings
from buda.rest.client.base import BaseClient
from buda.rest.endpoints.base import Endpoint
from buda.rest.models.markets import MarketList


class TestBuildRequest:
    def test_get_request(self):
        client = BaseClient(
            client=Client,
            settings=BudaSettings(rate_limit_enabled=False, retry_enabled=False),
        )
        ep = Endpoint(model=MarketList, method="GET", path="/markets", params={})
        req = client._build_request(ep)
        assert req.method == "GET"
        assert req.url.path == "/api/v2/markets"

    def test_post_request_with_json(self):
        client = BaseClient(
            client=Client,
            settings=BudaSettings(rate_limit_enabled=False, retry_enabled=False),
        )
        ep = Endpoint(
            model=MarketList,
            method="POST",
            path="/orders",
            json={"type": "Bid", "amount": 0.5},
        )
        req = client._build_request(ep)
        assert req.method == "POST"
        assert b"Bid" in req.content

    def test_request_with_params(self):
        client = BaseClient(
            client=Client,
            settings=BudaSettings(rate_limit_enabled=False, retry_enabled=False),
        )
        ep = Endpoint(
            model=MarketList,
            method="GET",
            path="/trades",
            params={"limit": 50},
        )
        req = client._build_request(ep)
        assert "limit=50" in str(req.url)

    def test_base_url_in_request(self):
        settings = BudaSettings(rate_limit_enabled=False, retry_enabled=False)
        client = BaseClient(client=Client, settings=settings)
        ep = Endpoint(model=MarketList, method="GET", path="/markets")
        req = client._build_request(ep)
        assert "buda.com" in str(req.url)


class TestBaseClientInit:
    def test_creates_with_defaults(self):
        client = BaseClient(client=Client)
        assert client._auth is None
        assert client._settings is not None

    def test_creates_with_credentials(self):
        creds = StaticCredentials(api_key="k", api_secret="s")
        client = BaseClient(client=Client, provider=creds)
        assert client._auth is not None
        assert client._auth.api_key == "k"

    def test_creates_with_custom_settings(self):
        settings = BudaSettings(timeout=30.0)
        client = BaseClient(client=Client, settings=settings)
        assert client._settings.timeout == 30.0
