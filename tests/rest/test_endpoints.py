from __future__ import annotations

from buda.rest.endpoints.account import balances_endpoint, me_endpoint
from buda.rest.endpoints.markets import markets_endpoint, tickers_endpoint
from buda.rest.endpoints.orders import (
    cancel_all_orders_endpoint,
    cancel_order_endpoint,
    create_order_endpoint,
    order_book_endpoint,
    order_detail_endpoint,
    quotation_endpoint,
    trades_endpoint,
)
from buda.rest.models.account import Balance, BalanceList, UserInfo
from buda.rest.models.markets import Market, MarketList, MarketTicker, TickerList
from buda.rest.models.orders import (
    OrderBook,
    OrderCancelAllResponse,
    OrderCancelResponse,
    OrderCreate,
    OrderCreateResponse,
    OrderDetail,
    Quotation,
    Trades,
)

# ── Market Endpoints ───────────────────────────────────────────────


class TestMarketsEndpoint:
    def test_all_markets(self):
        ep = markets_endpoint(None)
        assert ep.path == "/markets"
        assert ep.method == "GET"
        assert ep.model is MarketList

    def test_single_market(self):
        ep = markets_endpoint("btc-clp")
        assert ep.path == "/markets/btc-clp"
        assert ep.method == "GET"
        assert ep.model is Market


class TestTickersEndpoint:
    def test_all_tickers(self):
        ep = tickers_endpoint(None)
        assert ep.path == "/tickers"
        assert ep.method == "GET"
        assert ep.model is TickerList

    def test_single_ticker(self):
        ep = tickers_endpoint("btc-clp")
        assert ep.path == "/markets/btc-clp/ticker"
        assert ep.method == "GET"
        assert ep.model is MarketTicker


# ── Account Endpoints ──────────────────────────────────────────────


class TestMeEndpoint:
    def test_me(self):
        ep = me_endpoint()
        assert ep.path == "/me"
        assert ep.method == "GET"
        assert ep.model is UserInfo


class TestBalancesEndpoint:
    def test_all_balances(self):
        ep = balances_endpoint(None)
        assert ep.path == "/balances"
        assert ep.method == "GET"
        assert ep.model is BalanceList

    def test_single_balance(self):
        ep = balances_endpoint("BTC")
        assert ep.path == "/balances/BTC"
        assert ep.method == "GET"
        assert ep.model is Balance


# ── Order Endpoints ────────────────────────────────────────────────


class TestOrderBookEndpoint:
    def test_order_book(self):
        ep = order_book_endpoint("btc-clp")
        assert ep.path == "/markets/btc-clp/order_book"
        assert ep.method == "GET"
        assert ep.model is OrderBook


class TestTradesEndpoint:
    def test_no_params(self):
        ep = trades_endpoint("btc-clp")
        assert ep.path == "/markets/btc-clp/trades"
        assert ep.method == "GET"
        assert ep.model is Trades

    def test_with_params(self):
        ep = trades_endpoint("btc-clp", params={"timestamp": 1000, "limit": 50})
        assert ep.params["timestamp"] == 1000
        assert ep.params["limit"] == 50

    def test_params_none_stripped(self):
        ep = trades_endpoint("btc-clp", params={"timestamp": None, "limit": 10})
        assert "timestamp" not in ep.params
        assert ep.params["limit"] == 10


class TestQuotationEndpoint:
    def test_quotation(self):
        ep = quotation_endpoint(
            "btc-clp",
            payload={"type": "bid_given_size", "amount": 0.5},
        )
        assert ep.path == "/markets/btc-clp/quotations"
        assert ep.method == "POST"
        assert ep.model is Quotation
        assert ep.json is not None

    def test_quotation_with_limit(self):
        ep = quotation_endpoint(
            "btc-clp",
            payload={"type": "bid_given_size", "amount": 0.5, "limit": 50000.0},
        )
        assert ep.json["limit"] == 50000.0  # type: ignore[index]


class TestCreateOrderEndpoint:
    def test_create_order(self):
        payload = OrderCreate(type="Bid", price_type="market", amount=0.5)
        ep = create_order_endpoint("btc-clp", payload=payload)
        assert ep.path == "/markets/btc-clp/orders"
        assert ep.method == "POST"
        assert ep.model is OrderCreateResponse
        assert ep.json is not None


class TestOrderDetailEndpoint:
    def test_order_detail(self):
        ep = order_detail_endpoint(12345)
        assert ep.path == "/orders/12345"
        assert ep.method == "GET"
        assert ep.model is OrderDetail


class TestCancelOrderEndpoint:
    def test_cancel_order(self):
        ep = cancel_order_endpoint(12345)
        assert ep.path == "/orders/12345"
        assert ep.method == "PUT"
        assert ep.json == {"state": "canceling"}
        assert ep.model is OrderCancelResponse


class TestCancelAllOrdersEndpoint:
    def test_cancel_all_no_filters(self):
        ep = cancel_all_orders_endpoint()
        assert ep.path == "/orders"
        assert ep.method == "DELETE"
        assert ep.model is OrderCancelAllResponse

    def test_cancel_all_with_market(self):
        ep = cancel_all_orders_endpoint(market_id="btc-clp")
        assert ep.json["market_id"] == "btc-clp"  # type: ignore[index]

    def test_cancel_all_with_type(self):
        ep = cancel_all_orders_endpoint(type="Bid")
        assert ep.json["type"] == "Bid"  # type: ignore[index]


# ── Endpoint parse_params ──────────────────────────────────────────


class TestEndpointParseParams:
    def test_strips_none_values(self):
        ep = trades_endpoint("btc-clp", params={"timestamp": None, "limit": None})
        assert ep.params == {}

    def test_keeps_non_none_values(self):
        ep = trades_endpoint("btc-clp", params={"limit": 50})
        assert ep.params == {"limit": 50}
