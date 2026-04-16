from collections.abc import Mapping
from typing import Any, Literal

from pydantic import BaseModel, field_validator
from pydantic.dataclasses import dataclass

RequestMethod = Literal["GET", "POST", "PUT", "DELETE"]
"""Supported HTTP request methods for API endpoints."""

@dataclass(frozen=True, kw_only=True, slots=True)
class Endpoint[T: BaseModel]:
    """
    Represents an API endpoint with its path, request method, and
    associated data model.
    """

    path: str
    model: type[T]
    method: RequestMethod
    params: Mapping[str, Any] = ...
    json: Mapping[str, Any] | None = ...

    @field_validator("params", mode="before")
    @classmethod
    def _parse_params(cls, data: Mapping[str, Any]) -> Mapping[str, Any]: ...
