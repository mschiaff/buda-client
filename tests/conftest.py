from __future__ import annotations

from typing import Any

import httpx
import pytest

from buda.core.providers import StaticCredentials
from buda.core.settings import BudaSettings


@pytest.fixture
def default_settings() -> BudaSettings:
    return BudaSettings()


@pytest.fixture
def fast_settings() -> BudaSettings:
    """Settings with rate limiting and retry disabled for fast tests."""
    return BudaSettings(
        rate_limit_enabled=False,
        retry_enabled=False,
    )


@pytest.fixture
def mock_credentials() -> StaticCredentials:
    return StaticCredentials(api_key="test-key", api_secret="test-secret")


def make_mock_response(
    data: dict[str, Any],
    status_code: int = 200,
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    """Build a mock httpx.Response with JSON body."""
    response = httpx.Response(
        status_code=status_code,
        json=data,
        headers=headers or {},
        request=httpx.Request("GET", "https://test.com"),
    )
    return response


# ── Shared realistic API response data ─────────────────────────────

CURRENCY_VALUE_RAW: list[str] = ["100.5", "BTC"]

MARKET_RAW: dict[str, Any] = {
    "id": "btc-clp",
    "name": "btc-clp",
    "base_currency": "BTC",
    "quote_currency": "CLP",
    "minimum_order_amount": ["0.00002", "BTC"],
    "disabled": False,
    "illiquid": False,
    "rpo_disabled": None,
    "taker_fee": 0.008,
    "maker_fee": 0.004,
    "max_orders_per_minute": 40,
    "maker_discount_percentage": 0.0,
    "taker_discount_percentage": 0.0,
    "taker_discount_tiers": {},
    "maker_discount_tiers": {},
}

ACCOUNT_INFO_RAW: dict[str, Any] = {
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

USER_INFO_RAW: dict[str, Any] = {
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

BALANCE_RAW: dict[str, Any] = {
    "id": "BTC",
    "amount": ["1.5", "BTC"],
    "available_amount": ["1.0", "BTC"],
    "promissory_amount": ["0.0", "BTC"],
    "available_for_orders_amount": ["1.0", "BTC"],
    "frozen_amount": ["0.0", "BTC"],
    "pending_withdraw_amount": ["0.5", "BTC"],
    "account_id": 42,
}

ORDER_RESPONSE_RAW: dict[str, Any] = {
    "id": 12345,
    "client_id": None,
    "amount": ["0.5", "BTC"],
    "created_at": "2024-01-01T00:00:00.000Z",
    "fee_currency": "CLP",
    "limit": None,
    "market_id": "btc-clp",
    "original_amount": ["0.5", "BTC"],
    "paid_fee": ["0.0", "CLP"],
    "price_type": "market",
    "order_type": "Bid",
    "state": "pending",
    "total_exchanged": ["0.0", "CLP"],
    "traded_amount": ["0.0", "BTC"],
    "type": "Bid",
}
