from __future__ import annotations

from abc import ABC
from typing import Annotated

from pydantic.dataclasses import dataclass
from pydantic import Field, HttpUrl, BeforeValidator


Url = Annotated[
    str, 
    BeforeValidator(
        lambda v: HttpUrl(v).encoded_string()
    )
]


@dataclass(frozen=True, kw_only=True, slots=True)
class BudaSettings:
    """Settings for Buda API clients."""
    
    base_url: Url = Field(
        default="https://www.buda.com/api/v2",
        description="Base URL for the Buda API",
    )
    user_agent: str = Field(
        default="python-buda-client/0.1.0",
        description="User agent for the Buda API client"
    )


class BaseClient(ABC):
    """Base client class for Buda API clients."""
    
    def __init__(self, settings: BudaSettings | None = None):
        self._settings: BudaSettings = settings or BudaSettings()