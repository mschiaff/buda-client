from __future__ import annotations

import base64
import hmac
import time
import httpx

from httpx import Request
from collections.abc import Generator


class BudaAuth(httpx.Auth):
    """Attach Buda HMAC authentication to the Request object."""

    def __init__(self, api_key: str, secret: str):
        self.api_key = api_key
        self.secret = secret

    def get_nonce(self) -> str:
        """Generate a nonce (timestamp in microseconds)"""
        return str(int(time.time() * 1e6))

    def sign(self, request: httpx.Request, nonce: str) -> str:
        """Create the HMAC signature for the request."""
        components = [
            request.method,
            request.url.path
        ]
        
        if request.content:
            body = base64.b64encode(
                request.content
            ).decode()
            components.append(body)
        components.append(nonce)
        message = ' '.join(components)
        
        hash = hmac.new(
            key=self.secret.encode(),
            msg=message.encode(),
            digestmod='sha384'
        )
        
        return hash.hexdigest()

    def auth_flow(self, request: Request) -> Generator[Request, None, None]:
        nonce = self.get_nonce()
        signature = self.sign(request, nonce)
        
        request.headers['X-SBTC-APIKEY'] = self.api_key
        request.headers['X-SBTC-SIGNATURE'] = signature
        request.headers['X-SBTC-NONCE'] = nonce
        
        yield request