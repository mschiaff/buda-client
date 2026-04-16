from typing import Any, ClassVar

from pydantic import SecretStr, model_serializer
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

class BudaCredentials(BaseSettings):
    """Buda API credentials."""

    api_key: SecretStr
    """The API key for authentication."""
    api_secret: SecretStr
    """The API secret for authentication."""

    def __init__(self, *, api_key: str, api_secret: str) -> None:
        """
        Initialize BudaCredentials with API key and secret.

        Parameters
        ----------
        api_key : str
            The API key for authentication.
        api_secret : str
            The API secret for authentication.
        """
        ...
    
    @model_serializer(mode="plain", return_type=dict[str, str])
    def _serialize(self) -> dict[str, str]:
        """Serialize the credentials to a plain dictionary."""
        ...


class StaticCredentials(BudaCredentials):
    """Provider that uses static credentials."""
    
    def __init__(self, *, api_key: str, api_secret: str) -> None:
        """
        Initialize StaticCredentials with API key and secret.

        Parameters
        ----------
        api_key : str
            The API key for authentication.
        api_secret : str
            The API secret for authentication.
        """
        ...


class EnvCredentials(BudaCredentials):
    """Provider that loads credentials from environment variables."""

    model_config: ClassVar[SettingsConfigDict] = ...

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize EnvCredentials with optional arguments."""
        ...


class DotEnvCredentials(BudaCredentials):
    """Provider that loads credentials from a .env file."""

    model_config: ClassVar[SettingsConfigDict] = ...

    def __init__(self, env_file: str = ..., **kwargs: Any) -> None:
        """
        Initialize DotEnvCredentials with a .env file.
        
        Parameters
        ----------
        env_file : str, optional
            The path to the .env file (default is ".env").
        """
        ...

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        ...
