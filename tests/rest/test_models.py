from __future__ import annotations

from buda.rest.models.account import Balance, BalanceList, UserInfo
from buda.rest.models.common import CurrencyValue, PriceAmount
from buda.rest.models.markets import Market, MarketList, MarketTicker, Ticker, TickerList
from buda.rest.models.orders import (
    OrderBook,
    OrderCancelAllResponse,
    OrderCancelResponse,
    OrderCreate,
    OrderCreateResponse,
    OrderDetail,
    Quotation,
    TradeEntry,
    Trades,
)
from tests.conftest import MARKET_RAW, ORDER_RESPONSE_RAW

# ── Common Models ──────────────────────────────────────────────────

class TestCurrencyValue:
    def test_parse_from_list(self):
        cv = CurrencyValue.model_validate(["100.5", "BTC"])
        assert cv.value == 100.5
        assert cv.currency == "BTC"

    def test_parse_zero(self):
        cv = CurrencyValue.model_validate(["0.0", "CLP"])
        assert cv.value == 0.0
        assert cv.currency == "CLP"


class TestPriceAmount:
    def test_parse_from_list(self):
        pa = PriceAmount.model_validate(["50000.0", "1.5"])
        assert pa.price == 50000.0
        assert pa.amount == 1.5


# ── Market Models ──────────────────────────────────────────────────

class TestMarket:
    def test_unwrap_from_market_key(self):
        m = Market.model_validate({"market": MARKET_RAW})
        assert m.id == "btc-clp"
        assert m.base_currency == "BTC"
        assert m.quote_currency == "CLP"
        assert m.taker_fee == 0.008
        assert m.minimum_order_amount.currency == "BTC"

    def test_parse_direct_dict(self):
        m = Market.model_validate(MARKET_RAW)
        assert m.id == "btc-clp"


class TestMarketList:
    def test_unwrap_from_markets_key(self):
        ml = MarketList.model_validate({"markets": [MARKET_RAW, MARKET_RAW]})
        assert len(ml.root) == 2
        assert ml.root[0].id == "btc-clp"


class TestTicker:
    def test_parse_ticker(self):
        data = {
            "market_id": "btc-clp",
            "price_variation_24h": 0.05,
            "price_variation_7d": -0.02,
            "last_price": ["50000.0", "CLP"],
        }
        t = Ticker.model_validate(data)
        assert t.market_id == "btc-clp"
        assert t.last_price.value == 50000.0


class TestMarketTicker:
    def test_unwrap_from_ticker_key(self):
        data = {
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
        mt = MarketTicker.model_validate(data)
        assert mt.market_id == "btc-clp"
        assert mt.min_ask.value == 51000.0
        assert mt.max_bid.value == 49000.0
        assert mt.volume.value == 10.0


class TestTickerList:
    def test_unwrap_from_tickers_key(self):
        ticker_data = {
            "market_id": "btc-clp",
            "price_variation_24h": 0.05,
            "price_variation_7d": -0.02,
            "last_price": ["50000.0", "CLP"],
        }
        tl = TickerList.model_validate({"tickers": [ticker_data]})
        assert len(tl.root) == 1


# ── Account Models ─────────────────────────────────────────────────

ACCOUNT_INFO_RAW = {
    "names": "Test",
    "surnames": "User",
    "nationality": "CL",
    "document_country": "CL",
    "document_type": "rut",
    "document_number": "12345678-9",
    "birth_date": "1990-01-01",
    "profession": "Engineer",
    "pep_check": False,
    "document_front_upload_id": None,
    "document_back_upload_id": None,
    "residence_address": None,
    "residence_country": None,
    "residence_state": None,
    "residence_comune": None,
    "residence_city": None,
    "residence_phone": None,
    "residence_street_type": None,
    "residence_location_type": None,
    "residence_location": None,
    "residence_province": None,
    "residence_postal_code": None,
    "residence_proof_upload_id": None,
    "document_verification_code": None,
    "main_activity": None,
    "city_of_birth": None,
    "civil_status": None,
    "spouse_names": None,
    "spouse_surnames": None,
    "spouse_document_type": None,
    "spouse_document_number": None,
    "operation_estimate": None,
    "sworn_declarations_check": None,
    "anual_income_range": None,
    "co_tax_code_rut": None,
    "pe_tax_code_ruc": None,
    "workplace": None,
    "jobtitle": None,
    "service_time": None,
    "place_of_birth": None,
    "selfie_upload_id": None,
    "cuit_or_cuil": None,
    "has_afip": None,
    "security_sworn_declaration_check": False,
    "document_exp_date": None,
    "residence_land_phone": None,
    "pep_relative_check": None,
    "relatives": None,
    "purpose": None,
    "purpose_other": None,
    "funds_source": None,
    "funds_source_other": None,
    "patrimony_source": None,
    "operation_funds_source": None,
}

USER_INFO_RAW = {
    "user": {
        "id": "123",
        "email": "test@example.com",
        "category": None,
        "display_name": None,
        "account_data": ACCOUNT_INFO_RAW,
        "tags": [],
        "monthly_transacted": ["0.0", "USD"],
        "pubsub_key": "pk-123",
        "alerts": [],
        "referral_terms_accepted": False,
        "referral_payout_currency": None,
        "analytics_user_id": None,
        "security_disclaimer_dismissed": False,
        "withdrawal_trust_level": None,
        "withdrawal_not_trusted_message": None,
        "banco_de_bogota_sandbox_state": None,
        "investor_profile": None,
        "site_terms_country_codes": None,
        "needs_one_time_password": False,
        "updated_at": None,
        "total_usd_balance": ["100.0", "USD"],
        "daily_fiat_flow": ["0.0", "CLP"],
        "monthly_fiat_flow": ["0.0", "CLP"],
        "withdrawals_unblock_at": None,
        "fiat_withdrawals_blocked": None,
        "crypto_withdrawals_blocked": None,
        "fiat_withdrawals_blocked_reason": None,
        "crypto_withdrawals_blocked_reason": None,
    }
}


class TestUserInfo:
    def test_unwrap_from_user_key(self):
        ui = UserInfo.model_validate(USER_INFO_RAW)
        assert ui.id == "123"
        assert ui.email == "test@example.com"
        assert ui.pubsub_key == "pk-123"
        assert ui.account_data.names == "Test"


BALANCE_RAW = {
    "id": "BTC",
    "amount": ["1.5", "BTC"],
    "available_amount": ["1.0", "BTC"],
    "promissory_amount": ["0.0", "BTC"],
    "available_for_orders_amount": ["1.0", "BTC"],
    "frozen_amount": ["0.0", "BTC"],
    "pending_withdraw_amount": ["0.5", "BTC"],
    "account_id": 42,
}


class TestBalance:
    def test_unwrap_from_balance_key(self):
        b = Balance.model_validate({"balance": BALANCE_RAW})
        assert b.id == "BTC"
        assert b.amount.value == 1.5
        assert b.available_amount.value == 1.0

    def test_parse_direct_dict(self):
        b = Balance.model_validate(BALANCE_RAW)
        assert b.id == "BTC"


class TestBalanceList:
    def test_unwrap_from_balances_key(self):
        bl = BalanceList.model_validate({"balances": [BALANCE_RAW]})
        assert len(bl.root) == 1
        assert bl.root[0].id == "BTC"


# ── Order Models ───────────────────────────────────────────────────

class TestOrderBook:
    def test_unwrap_from_order_book_key(self):
        data = {
            "order_book": {
                "market_id": "btc-clp",
                "bids": [["50000.0", "1.0"], ["49000.0", "2.0"]],
                "asks": [["51000.0", "0.5"]],
            }
        }
        ob = OrderBook.model_validate(data)
        assert ob.market_id == "btc-clp"
        assert len(ob.bids) == 2
        assert ob.bids[0].price == 50000.0
        assert ob.bids[0].amount == 1.0
        assert len(ob.asks) == 1


class TestTradeEntry:
    def test_parse_from_list(self):
        raw = [1700000000000, "0.5", "50000.0", "buy", 99]
        te = TradeEntry.model_validate(raw)
        assert te.id == 99
        assert te.timestamp == 1700000000000
        assert te.direction == "buy"
        assert te.amount == 0.5
        assert te.price == 50000.0


class TestTrades:
    def test_unwrap_from_trades_key(self):
        data = {
            "trades": {
                "market_id": "btc-clp",
                "timestamp": None,
                "last_timestamp": 1700000000000,
                "entries": [
                    [1700000000000, "0.5", "50000.0", "buy", 1],
                    [1700000000001, "1.0", "49000.0", "sell", 2],
                ],
            }
        }
        t = Trades.model_validate(data)
        assert t.market_id == "btc-clp"
        assert len(t.entries) == 2
        assert t.entries[0].direction == "buy"
        assert t.entries[1].direction == "sell"


class TestQuotation:
    def test_unwrap_from_quotation_key(self):
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
        q = Quotation.model_validate(data)
        assert q.type == "bid_given_size"
        assert q.amount.value == 0.5
        assert q.incomplete is False


class TestOrderCreate:
    def test_market_order(self):
        oc = OrderCreate(type="Bid", price_type="market", amount=0.5)
        assert oc.type == "Bid"
        assert oc.limit is None
        assert oc.stop is None

    def test_limit_order(self):
        oc = OrderCreate(
            type="Ask",
            price_type="limit",
            amount=1.0,
            limit={"price": 50000.0, "type": "gtc"},
        )
        assert oc.limit is not None
        assert oc.limit["price"] == 50000.0 # type: ignore

    def test_model_dump_excludes_none(self):
        oc = OrderCreate(type="Bid", price_type="market", amount=0.5)
        dumped = oc.model_dump(exclude_none=True)
        assert "limit" not in dumped
        assert "stop" not in dumped
        assert "client_id" not in dumped


class TestOrderCreateResponse:
    def test_unwrap_from_order_key(self):
        ocr = OrderCreateResponse.model_validate({"order": ORDER_RESPONSE_RAW})
        assert ocr.id == 12345
        assert ocr.type == "Bid"
        assert ocr.state == "pending"


class TestOrderDetail:
    def test_unwrap_from_order_key(self):
        od = OrderDetail.model_validate({"order": ORDER_RESPONSE_RAW})
        assert od.id == 12345


class TestOrderCancelResponse:
    def test_unwrap_from_order_key(self):
        ocr = OrderCancelResponse.model_validate({"order": ORDER_RESPONSE_RAW})
        assert ocr.id == 12345

    def test_parse_direct_dict(self):
        ocr = OrderCancelResponse.model_validate(ORDER_RESPONSE_RAW)
        assert ocr.id == 12345


class TestOrderCancelAllResponse:
    def test_unwrap_from_orders_key(self):
        ocar = OrderCancelAllResponse.model_validate(
            {"orders": [ORDER_RESPONSE_RAW, ORDER_RESPONSE_RAW]}
        )
        assert len(ocar.root) == 2
