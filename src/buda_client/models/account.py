from __future__ import annotations

from typing import Any

from pydantic import BaseModel, RootModel, model_validator

from buda_client.models.common import CurrencyValue  # noqa: TC001


class UserInfo(BaseModel):
    id: str
    email: str
    category: str | None
    display_name: str | None
    account_data: AccountInfo
    tags: list[str]
    monthly_transacted: CurrencyValue
    pubsub_key: str | None
    alerts: list[str]
    referral_terms_accepted: bool
    referral_payout_currency: str | None
    analytics_user_id: int | None
    security_disclaimer_dismissed: bool
    withdrawal_trust_level: str | None
    withdrawal_not_trusted_message: str | None
    banco_de_bogota_sandbox_state: str | None
    investor_profile: str | None
    site_terms_country_codes: str | None
    needs_one_time_password: bool
    updated_at: str | None
    total_usd_balance: CurrencyValue
    daily_fiat_flow: CurrencyValue
    monthly_fiat_flow: CurrencyValue
    withdrawals_unblock_at: str | None
    fiat_withdrawals_blocked: str | None
    crypto_withdrawals_blocked: str | None
    fiat_withdrawals_blocked_reason: str | None
    crypto_withdrawals_blocked_reason: str | None

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["user"]


class AccountInfo(BaseModel):
    names: str | None
    surnames: str | None
    nationality: str | None
    document_country: str | None
    document_type: str | None
    document_number: str | None
    birth_date: str | None
    profession: str | None
    pep_check: bool
    document_front_upload_id: int | None
    document_back_upload_id: int | None
    residence_address: str | None
    residence_country: str | None
    residence_state: str | None
    residence_comune: str | None
    residence_city: str | None
    residence_phone: str | None
    residence_street_type: str | None
    residence_location_type: str | None
    residence_location: str | None
    residence_province: str | None
    residence_postal_code: str | None
    residence_proof_upload_id: int | None
    document_verification_code: str | None
    main_activity: str | None
    city_of_birth: str | None
    civil_status: str | None
    spouse_names: str | None
    spouse_surnames: str | None
    spouse_document_type: str | None
    spouse_document_number: str | None
    operation_estimate: str | None
    sworn_declarations_check: bool | None
    anual_income_range: str | None
    co_tax_code_rut: str | None
    pe_tax_code_ruc: str | None
    workplace: str | None
    jobtitle: str | None
    service_time: str | None
    place_of_birth: str | None
    selfie_upload_id: int | None
    cuit_or_cuil: str | None
    has_afip: bool | None
    security_sworn_declaration_check: bool
    document_exp_date: str | None
    residence_land_phone: str | None
    pep_relative_check: bool | None
    relatives: str | None
    purpose: str | None
    purpose_other: str | None
    funds_source: str | None
    funds_source_other: str | None
    patrimony_source: str | None
    operation_funds_source: str | None


class Balance(BaseModel):
    id: str
    amount: CurrencyValue
    available_amount: CurrencyValue
    promissory_amount: CurrencyValue
    available_for_orders_amount: CurrencyValue
    frozen_amount: CurrencyValue
    pending_withdraw_amount: CurrencyValue
    account_id: int

    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        if data.get("balance"):
            return data["balance"]
        return data


class BalanceList(RootModel[list[Balance]]):
    @model_validator(mode="before")
    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data["balances"]