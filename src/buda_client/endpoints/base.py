from __future__ import annotations

from typing import Literal, Mapping, Any

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class Endpoint[_T: BaseModel]:
    path: str
    model: type[_T]
    method: Literal["GET", "POST", "PUT", "DELETE"]
    params: Mapping[str, Any] = Field(default_factory=dict)
    json: Mapping[str, Any] | None = Field(default=None)