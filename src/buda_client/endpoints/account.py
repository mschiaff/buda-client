from __future__ import annotations

from typing import Any

from buda_client.endpoints.base import Endpoint
from buda_client.models.account import UserInfo


class AccountEndpoints:
    """Mixin providing account-related endpoint definitions."""

    # Type hint so the mixin knows about _request
    _request: Any

    def _me_endpoint(self) -> Endpoint[UserInfo]:
        return Endpoint(model=UserInfo, method="GET", path="/me")