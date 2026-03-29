from __future__ import annotations

from typing import Any

from buda_client.endpoints.base import Endpoint


class AccountEndpoints:
    """Mixin providing account-related endpoint definitions."""

    # Type hint so the mixin knows about _request
    _request: Any

    def _me_endpoint(self) -> Endpoint[None]:
        return Endpoint(model=None, method="GET", path="/me")