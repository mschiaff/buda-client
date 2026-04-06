from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, Field, HttpUrl, WebsocketUrl
from pydantic.dataclasses import dataclass

BaseUrl = Annotated[
    str, 
    BeforeValidator(
        lambda v: HttpUrl(v).encoded_string()
    )
]


@dataclass(frozen=True, kw_only=True, slots=True)
class BudaSettings:
    """Settings for Buda API clients."""
    
    base_url: BaseUrl = Field(
        default="https://www.buda.com/api/v2",
        description="Base URL for the Buda API",
    )
    base_uri: WebsocketUrl = Field(
        default=WebsocketUrl("wss://realtime.buda.com"),
        description="Base URI for the Buda WebSocket API",
    )
    user_agent: str = Field(
        default="python-buda-client/0.1.0",
        description="User agent for the Buda API client",
    )
    timeout: float | int = Field(
        default=10.0,
        union_mode="left_to_right",
        description="Timeout for API requests in seconds",
    )

    # Retry settings (tenacity)
    retry_enabled: bool = Field(
        default=True,
        description="Enable automatic retry for 429, 500, and 503 HTTP errors",
    )
    retry_max_attempts: int = Field(
        default=3,
        description="Maximum number of retry attempts",
    )
    retry_min_wait: float = Field(
        default=1.0,
        description="Minimum wait time between retries in seconds",
    )
    retry_max_wait: float = Field(
        default=30.0,
        description="Maximum wait time between retries in seconds",
    )
    retry_exponential_base: float = Field(
        default=2.0,
        description="Base for exponential backoff between retries",
    )

    # Rate limit settings
    rate_limit_enabled: bool = Field(
        default=True,
        description="Enable proactive rate limiting",
    )
    rate_limit_per_second: int = Field(
        default=20,
        description="Maximum requests per second (shared across auth/unauth)",
    )
    rate_limit_auth_per_minute: int = Field(
        default=375,
        description="Maximum authenticated requests per minute (per API key)",
    )
    rate_limit_unauth_per_minute: int = Field(
        default=120,
        description="Maximum unauthenticated requests per minute (per IP)",
    )

    @property
    def headers(self) -> dict[str, str]:
        """Default headers for API requests."""
        return {
            "User-Agent": self.user_agent,
        }