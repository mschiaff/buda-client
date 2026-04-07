from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx

from buda.core.auth import BudaAuth


class TestBudaAuthInit:
    def test_stores_credentials(self):
        auth = BudaAuth(api_key="key", api_secret="secret")
        assert auth.api_key == "key"
        assert auth.api_secret == "secret"


class TestGetNonce:
    @patch("buda.core.auth.time.time", return_value=1700000000.123456)
    def test_returns_microsecond_string(self, mock_time: MagicMock):
        auth = BudaAuth(api_key="k", api_secret="s")
        nonce = auth.get_nonce()
        assert nonce == str(int(1700000000.123456 * 1e6))
        mock_time.assert_called_once()

    def test_nonce_is_string(self):
        auth = BudaAuth(api_key="k", api_secret="s")
        nonce = auth.get_nonce()
        assert isinstance(nonce, str)
        assert nonce.isdigit()


class TestSign:
    def test_signature_is_hex_string(self):
        auth = BudaAuth(api_key="k", api_secret="secret")
        request = httpx.Request("GET", "https://www.buda.com/api/v2/markets")
        sig = auth.sign(request, "12345")
        assert isinstance(sig, str)
        assert len(sig) == 96  # SHA-384 hex = 96 chars

    def test_signature_deterministic(self):
        auth = BudaAuth(api_key="k", api_secret="secret")
        request = httpx.Request("GET", "https://www.buda.com/api/v2/markets")
        sig1 = auth.sign(request, "12345")
        sig2 = auth.sign(request, "12345")
        assert sig1 == sig2

    def test_different_nonce_different_signature(self):
        auth = BudaAuth(api_key="k", api_secret="secret")
        request = httpx.Request("GET", "https://www.buda.com/api/v2/markets")
        sig1 = auth.sign(request, "12345")
        sig2 = auth.sign(request, "99999")
        assert sig1 != sig2

    def test_signature_with_body(self):
        auth = BudaAuth(api_key="k", api_secret="secret")
        request = httpx.Request(
            "POST",
            "https://www.buda.com/api/v2/orders",
            json={"type": "Bid", "amount": 0.5},
        )
        sig = auth.sign(request, "12345")
        assert isinstance(sig, str)
        assert len(sig) == 96

    def test_signature_with_body_differs_from_without(self):
        auth = BudaAuth(api_key="k", api_secret="secret")
        nonce = "12345"
        get_req = httpx.Request("GET", "https://www.buda.com/api/v2/orders")
        post_req = httpx.Request(
            "POST",
            "https://www.buda.com/api/v2/orders",
            json={"type": "Bid"},
        )
        sig_get = auth.sign(get_req, nonce)
        sig_post = auth.sign(post_req, nonce)
        assert sig_get != sig_post


class TestAuthFlow:
    def test_adds_auth_headers(self):
        auth = BudaAuth(api_key="my-key", api_secret="my-secret")
        request = httpx.Request("GET", "https://www.buda.com/api/v2/markets")
        flow = auth.auth_flow(request)
        modified = next(flow)

        assert modified.headers["X-SBTC-APIKEY"] == "my-key"
        assert "X-SBTC-SIGNATURE" in modified.headers
        assert "X-SBTC-NONCE" in modified.headers

    def test_nonce_in_headers_is_digit_string(self):
        auth = BudaAuth(api_key="key", api_secret="secret")
        request = httpx.Request("GET", "https://www.buda.com/api/v2/markets")
        flow = auth.auth_flow(request)
        modified = next(flow)
        assert modified.headers["X-SBTC-NONCE"].isdigit()

    def test_signature_is_valid_hex(self):
        auth = BudaAuth(api_key="key", api_secret="secret")
        request = httpx.Request("GET", "https://www.buda.com/api/v2/markets")
        flow = auth.auth_flow(request)
        modified = next(flow)
        sig = modified.headers["X-SBTC-SIGNATURE"]
        int(sig, 16)  # Should not raise
