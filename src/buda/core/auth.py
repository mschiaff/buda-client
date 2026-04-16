from __future__ import annotations

import base64
import hmac
import time
from typing import TYPE_CHECKING

import httpx
from httpx import Request

if TYPE_CHECKING:
    from collections.abc import Generator

    from httpx import Response


class BudaAuth(httpx.Auth):
    __slots__ = (
        "api_key",
        "api_secret",
    )

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_nonce(self) -> str:
        return str(int(time.time() * 1e6))

    def sign(self, request: httpx.Request, nonce: str) -> str:
        components = [request.method, request.url.path]

        if request.content:
            body = base64.b64encode(request.content).decode()
            components.append(body)
        components.append(nonce)
        message = " ".join(components)

        hash = hmac.new(key=self.api_secret.encode(), msg=message.encode(), digestmod="sha384")

        return hash.hexdigest()

    def auth_flow(self, request: Request) -> Generator[Request, Response]:
        nonce = self.get_nonce()
        signature = self.sign(request, nonce)

        request.headers["X-SBTC-APIKEY"] = self.api_key
        request.headers["X-SBTC-SIGNATURE"] = signature
        request.headers["X-SBTC-NONCE"] = nonce

        yield request
