# pyright: reportPrivateUsage=false

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from buda.core.providers import StaticCredentials
from buda.core.settings import BudaSettings
from buda.rest.client.async_ import AsyncBudaClient
from buda.rest.models.markets import Market, MarketList
from buda.rest.models.orders import OrderCreate
from tests.conftest import (
    BALANCE_RAW,
    MARKET_RAW,
    ORDER_RESPONSE_RAW,
    USER_INFO_RAW,
    make_mock_response,
)

FAST_SETTINGS = BudaSettings(rate_limit_enabled=False, retry_enabled=False)
CREDS = StaticCredentials(api_key="k", api_secret="s")


class TestAsyncBudaClientInit:
    def test_creates_public_and_private(self):
        client = AsyncBudaClient(settings=FAST_SETTINGS)
        assert client.public is not None
        assert client.private is not None


class TestAsyncBudaClientContextManager:
    async def test_context_manager(self):
        async with AsyncBudaClient(settings=FAST_SETTINGS) as client:
            assert client is not None

    async def test_close(self):
        client = AsyncBudaClient(settings=FAST_SETTINGS)
        await client.close()


class TestAsyncBudaClientRequest:
    async def test_request_raises_without_credentials(self):
        client = AsyncBudaClient(settings=FAST_SETTINGS)
        from buda.rest.endpoints.account import me_endpoint

        with pytest.raises(ValueError, match="no auth credentials"):
            await client._request(me_endpoint(), authenticated=True)

    async def test_request_returns_parsed_model(self):
        client = AsyncBudaClient(settings=FAST_SETTINGS)
        response = make_mock_response({"markets": [MARKET_RAW]})
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.endpoints.markets import markets_endpoint

            result = await client._request(markets_endpoint(None))
            assert isinstance(result, MarketList)

    async def test_request_returns_raw_dict(self):
        client = AsyncBudaClient(settings=FAST_SETTINGS)
        raw_data = {"markets": [MARKET_RAW]}
        response = make_mock_response(raw_data)
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.endpoints.markets import markets_endpoint

            result = await client._request(markets_endpoint(None), raw=True)
            assert isinstance(result, dict)

    async def test_request_authenticated(self):
        client = AsyncBudaClient(settings=FAST_SETTINGS, provider=CREDS)
        response = make_mock_response(USER_INFO_RAW)
        with patch.object(
            client._client, "send", new_callable=AsyncMock, return_value=response
        ) as mock_send:
            from buda.rest.endpoints.account import me_endpoint

            await client._request(me_endpoint(), authenticated=True)
            _, kwargs = mock_send.call_args
            assert kwargs.get("auth") is not None


class TestAsyncRawRequest:
    async def test_raw_request_returns_json(self):
        client = AsyncBudaClient(settings=FAST_SETTINGS)
        response = make_mock_response({"markets": [MARKET_RAW]})
        with patch.object(client._client, "request", new_callable=AsyncMock, return_value=response):
            result = await client._raw_request("GET", "/markets")
            assert isinstance(result, dict)
            assert "markets" in result

    async def test_raw_request_authenticated(self):
        client = AsyncBudaClient(settings=FAST_SETTINGS, provider=CREDS)
        response = make_mock_response(USER_INFO_RAW)
        with patch.object(
            client._client, "request", new_callable=AsyncMock, return_value=response
        ) as mock_req:
            result = await client._raw_request("GET", "/me", authenticated=True)
            assert "user" in result
            _, kwargs = mock_req.call_args
            assert kwargs.get("auth") is not None

    async def test_raw_request_raises_without_credentials(self):
        client = AsyncBudaClient(settings=FAST_SETTINGS)
        with pytest.raises(ValueError, match="no auth credentials"):
            await client._raw_request("GET", "/me", authenticated=True)


class TestAsyncPublicAPI:
    def _make_client(self) -> AsyncBudaClient:
        return AsyncBudaClient(settings=FAST_SETTINGS)

    async def test_markets_all(self):
        client = self._make_client()
        response = make_mock_response({"markets": [MARKET_RAW]})
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            result = await client.public.markets()
            assert isinstance(result, MarketList)

    async def test_markets_single(self):
        client = self._make_client()
        response = make_mock_response({"market": MARKET_RAW})
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            result = await client.public.markets("btc-clp")
            assert isinstance(result, Market)

    async def test_tickers_all(self):
        client = self._make_client()
        ticker_data = {
            "market_id": "btc-clp",
            "price_variation_24h": 0.05,
            "price_variation_7d": -0.02,
            "last_price": ["50000.0", "CLP"],
        }
        response = make_mock_response({"tickers": [ticker_data]})
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.models.markets import TickerList

            result = await client.public.tickers()
            assert isinstance(result, TickerList)

    async def test_order_book(self):
        client = self._make_client()
        data = {
            "order_book": {
                "market_id": "btc-clp",
                "bids": [["50000.0", "1.0"]],
                "asks": [["51000.0", "0.5"]],
            }
        }
        response = make_mock_response(data)
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.models.orders import OrderBook

            result = await client.public.order_book("btc-clp")
            assert isinstance(result, OrderBook)

    async def test_trades(self):
        client = self._make_client()
        data = {
            "trades": {
                "market_id": "btc-clp",
                "timestamp": None,
                "last_timestamp": 1700000000000,
                "entries": [[1700000000000, "0.5", "50000.0", "buy", 1]],
            }
        }
        response = make_mock_response(data)
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.models.orders import Trades

            result = await client.public.trades("btc-clp")
            assert isinstance(result, Trades)

    async def test_quotations(self):
        client = self._make_client()
        data = {
            "quotation": {
                "amount": ["0.5", "BTC"],
                "limit": None,
                "type": "bid_given_size",
                "order_amount": ["0.5", "BTC"],
                "base_exchanged": ["0.5", "BTC"],
                "quote_exchanged": ["25000000.0", "CLP"],
                "base_balance_change": ["-0.5", "BTC"],
                "quote_balance_change": ["25000000.0", "CLP"],
                "fee": ["200000.0", "CLP"],
                "incomplete": False,
            }
        }
        response = make_mock_response(data)
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.models.orders import Quotation

            result = await client.public.quotations(
                "btc-clp",
                payload={"type": "bid_given_size", "amount": 0.5},
            )
            assert isinstance(result, Quotation)


class TestAsyncPrivateAPI:
    def _make_client(self) -> AsyncBudaClient:
        return AsyncBudaClient(settings=FAST_SETTINGS, provider=CREDS)

    async def test_me(self):
        client = self._make_client()
        response = make_mock_response(USER_INFO_RAW)
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.models.account import UserInfo

            result = await client.private.me()
            assert isinstance(result, UserInfo)

    async def test_balances_all(self):
        client = self._make_client()
        response = make_mock_response({"balances": [BALANCE_RAW]})
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.models.account import BalanceList

            result = await client.private.balances()
            assert isinstance(result, BalanceList)

    async def test_balances_single(self):
        client = self._make_client()
        response = make_mock_response({"balance": BALANCE_RAW})
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.models.account import Balance

            result = await client.private.balances("BTC")
            assert isinstance(result, Balance)

    async def test_create_order(self):
        client = self._make_client()
        response = make_mock_response({"order": ORDER_RESPONSE_RAW})
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.models.orders import OrderCreateResponse

            payload = OrderCreate(type="Bid", price_type="market", amount=0.5)
            result = await client.private.create_order("btc-clp", payload=payload)
            assert isinstance(result, OrderCreateResponse)

    async def test_order_detail(self):
        client = self._make_client()
        response = make_mock_response({"order": ORDER_RESPONSE_RAW})
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.models.orders import OrderDetail

            result = await client.private.order_detail(12345)
            assert isinstance(result, OrderDetail)

    async def test_cancel_order(self):
        client = self._make_client()
        response = make_mock_response({"order": ORDER_RESPONSE_RAW})
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.models.orders import OrderCancelResponse

            result = await client.private.cancel_order(12345)
            assert isinstance(result, OrderCancelResponse)

    async def test_cancel_all_orders(self):
        client = self._make_client()
        response = make_mock_response({"orders": [ORDER_RESPONSE_RAW]})
        with patch.object(client._client, "send", new_callable=AsyncMock, return_value=response):
            from buda.rest.models.orders import OrderCancelAllResponse

            result = await client.private.cancel_all_orders()
            assert isinstance(result, OrderCancelAllResponse)
