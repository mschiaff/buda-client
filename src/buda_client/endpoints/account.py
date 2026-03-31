from __future__ import annotations

from buda_client.endpoints.base import Endpoint
from buda_client.models.account import UserInfo


def me_endpoint() -> Endpoint[UserInfo]:
    return Endpoint(model=UserInfo, method="GET", path="/me")