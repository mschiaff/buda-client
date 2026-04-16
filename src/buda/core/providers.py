from __future__ import annotations

from typing import Any

from pydantic import Field, SecretStr, model_serializer
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class BudaCredentials(BaseSettings):
    api_key: SecretStr = Field(..., validation_alias="buda_api_key")
    api_secret: SecretStr = Field(..., validation_alias="buda_api_secret")

    @model_serializer(mode="plain", return_type=dict[str, str])
    def _serialize(self) -> dict[str, str]:
        return {
            "api_key": self.api_key.get_secret_value(),
            "api_secret": self.api_secret.get_secret_value(),
        }


class StaticCredentials(BudaCredentials):
    """Provider that uses static credentials."""

    def __init__(self, *, api_key: str, api_secret: str) -> None:
        super().__init__(buda_api_key=api_key, buda_api_secret=api_secret)  # type: ignore


class EnvCredentials(BudaCredentials):
    """Provider that loads credentials from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="BUDA_",
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class DotEnvCredentials(BudaCredentials):
    """Provider that loads credentials from a .env file."""

    model_config = SettingsConfigDict(env_file=".env")

    def __init__(self, env_file: str = ".env", **kwargs: Any) -> None:
        super().__init__(_env_file=env_file, **kwargs)  # type: ignore

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (dotenv_settings,)
