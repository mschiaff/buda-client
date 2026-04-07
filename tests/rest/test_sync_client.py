# pyright: reportPrivateUsage=false

from __future__ import annotations

from unittest.mock import patch

import pytest

from buda.core.providers import StaticCredentials
from buda.core.settings import BudaSettings
from buda.rest.client.sync_ import BudaClient
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


class TestBudaClientInit:
    def test_creates_public_and_private(self):
        client = BudaClient(settings=FAST_SETTINGS)
        assert client.public is not None
        assert client.private is not None


class TestBudaClientContextManager:
    def test_context_manager(self):
        with BudaClient(settings=FAST_SETTINGS) as client:
            assert client is not None

    def test_close(self):
        client = BudaClient(settings=FAST_SETTINGS)
        client.close()


class TestBudaClientRequest:
    def test_request_raises_without_credentials(self):
        client = BudaClient(settings=FAST_SETTINGS)
        from buda.rest.endpoints.account import me_endpoint
        with pytest.raises(ValueError, match="no auth credentials"):
            client._request(me_endpoint(), authenticated=True)

    def test_request_returns_parsed_model(self):
        client = BudaClient(settings=FAST_SETTINGS)
        response = make_mock_response({"markets": [MARKET_RAW]})
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.endpoints.markets import markets_endpoint
            result = client._request(markets_endpoint(None))
            assert isinstance(result, MarketList)

    def test_request_returns_raw_dict(self):
        client = BudaClient(settings=FAST_SETTINGS)
        raw_data = {"markets": [MARKET_RAW]}
        response = make_mock_response(raw_data)
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.endpoints.markets import markets_endpoint
            result = client._request(markets_endpoint(None), raw=True)
            assert isinstance(result, dict)
            assert "markets" in result

    def test_request_authenticated(self):
        client = BudaClient(settings=FAST_SETTINGS, provider=CREDS)
        response = make_mock_response(USER_INFO_RAW)
        with patch.object(client._client, "send", return_value=response) as mock_send:
            from buda.rest.endpoints.account import me_endpoint
            result = client._request(me_endpoint(), authenticated=True)  # type: ignore # noqa: F841
            # Verify auth was passed
            _, kwargs = mock_send.call_args
            assert kwargs.get("auth") is not None


class TestPublicAPI:
    def _make_client(self) -> BudaClient:
        return BudaClient(settings=FAST_SETTINGS)

    def test_markets_all(self):
        client = self._make_client()
        response = make_mock_response({"markets": [MARKET_RAW]})
        with patch.object(client._client, "send", return_value=response):
            result = client.public.markets()
            assert isinstance(result, MarketList)

    def test_markets_single(self):
        client = self._make_client()
        response = make_mock_response({"market": MARKET_RAW})
        with patch.object(client._client, "send", return_value=response):
            result = client.public.markets("btc-clp")
            assert isinstance(result, Market)
            assert result.id == "btc-clp"

    def test_markets_raw(self):
        client = self._make_client()
        response = make_mock_response({"markets": [MARKET_RAW]})
        with patch.object(client._client, "send", return_value=response):
            result = client.public.markets(raw=True)
            assert isinstance(result, dict)

    def test_tickers_all(self):
        client = self._make_client()
        ticker_data = {
            "market_id": "btc-clp",
            "price_variation_24h": 0.05,
            "price_variation_7d": -0.02,
            "last_price": ["50000.0", "CLP"],
        }
        response = make_mock_response({"tickers": [ticker_data]})
        with patch.object(client._client, "send", return_value=response):
            result = client.public.tickers()
            from buda.rest.models.markets import TickerList
            assert isinstance(result, TickerList)

    def test_tickers_single(self):
        client = self._make_client()
        ticker_data = {
            "ticker": {
                "market_id": "btc-clp",
                "price_variation_24h": 0.05,
                "price_variation_7d": -0.02,
                "last_price": ["50000.0", "CLP"],
                "min_ask": ["51000.0", "CLP"],
                "max_bid": ["49000.0", "CLP"],
                "volume": ["10.0", "BTC"],
                "quote_volume": ["500000000.0", "CLP"],
            }
        }
        response = make_mock_response(ticker_data)
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.models.markets import MarketTicker
            result = client.public.tickers("btc-clp")
            assert isinstance(result, MarketTicker)

    def test_order_book(self):
        client = self._make_client()
        data = {
            "order_book": {
                "market_id": "btc-clp",
                "bids": [["50000.0", "1.0"]],
                "asks": [["51000.0", "0.5"]],
            }
        }
        response = make_mock_response(data)
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.models.orders import OrderBook
            result = client.public.order_book("btc-clp")
            assert isinstance(result, OrderBook)

    def test_trades(self):
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
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.models.orders import Trades
            result = client.public.trades("btc-clp")
            assert isinstance(result, Trades)

    def test_quotations(self):
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
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.models.orders import Quotation
            result = client.public.quotations(
                "btc-clp",
                payload={"type": "bid_given_size", "amount": 0.5},
            )
            assert isinstance(result, Quotation)


class TestPrivateAPI:
    def _make_client(self) -> BudaClient:
        return BudaClient(settings=FAST_SETTINGS, provider=CREDS)

    def test_me(self):
        client = self._make_client()
        response = make_mock_response(USER_INFO_RAW)
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.models.account import UserInfo
            result = client.private.me()
            assert isinstance(result, UserInfo)

    def test_balances_all(self):
        client = self._make_client()
        response = make_mock_response({"balances": [BALANCE_RAW]})
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.models.account import BalanceList
            result = client.private.balances()
            assert isinstance(result, BalanceList)

    def test_balances_single(self):
        client = self._make_client()
        response = make_mock_response({"balance": BALANCE_RAW})
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.models.account import Balance
            result = client.private.balances("BTC")
            assert isinstance(result, Balance)

    def test_create_order(self):
        client = self._make_client()
        response = make_mock_response({"order": ORDER_RESPONSE_RAW})
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.models.orders import OrderCreateResponse
            payload = OrderCreate(type="Bid", price_type="market", amount=0.5)
            result = client.private.create_order("btc-clp", payload=payload)
            assert isinstance(result, OrderCreateResponse)

    def test_order_detail(self):
        client = self._make_client()
        response = make_mock_response({"order": ORDER_RESPONSE_RAW})
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.models.orders import OrderDetail
            result = client.private.order_detail(12345)
            assert isinstance(result, OrderDetail)

    def test_cancel_order(self):
        client = self._make_client()
        response = make_mock_response({"order": ORDER_RESPONSE_RAW})
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.models.orders import OrderCancelResponse
            result = client.private.cancel_order(12345)
            assert isinstance(result, OrderCancelResponse)

    def test_cancel_all_orders(self):
        client = self._make_client()
        response = make_mock_response({"orders": [ORDER_RESPONSE_RAW]})
        with patch.object(client._client, "send", return_value=response):
            from buda.rest.models.orders import OrderCancelAllResponse
            result = client.private.cancel_all_orders()
            assert isinstance(result, OrderCancelAllResponse)
