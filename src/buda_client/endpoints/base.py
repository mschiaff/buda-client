from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, Field, field_validator
from pydantic.dataclasses import dataclass

if TYPE_CHECKING:
    from collections.abc import Mapping


@dataclass(frozen=True, kw_only=True, slots=True)
class Endpoint[T: BaseModel]:
    path: str
    model: type[T]
    method: Literal["GET", "POST", "PUT", "DELETE"]
    params: Mapping[str, Any] = Field(default_factory=dict)
    json: Mapping[str, Any] | None = Field(default=None)

    @field_validator("params", mode="before")
    @classmethod
    def parse_params(cls, data: Mapping[str, Any]) -> Mapping[str, Any]:
        # Remove None values to avoid sending them as query parameters
        return {k: v for k, v in data.items() if v is not None} if data else {}