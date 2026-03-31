from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, Field, HttpUrl
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
    user_agent: str = Field(
        default="python-buda-client/0.1.0",
        description="User agent for the Buda API client",
    )
    timeout: float | int = Field(
        default=10.0,
        union_mode="left_to_right",
        description="Timeout for API requests in seconds",
    )

    @property
    def headers(self) -> dict[str, str]:
        """Default headers for API requests."""
        return {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }