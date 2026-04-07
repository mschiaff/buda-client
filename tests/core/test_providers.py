from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from pydantic import ValidationError

from buda.core.providers import (
    DotEnvCredentials,
    EnvCredentials,
    StaticCredentials,
)

if TYPE_CHECKING:
    from pathlib import Path

    from pytest import MonkeyPatch


class TestStaticCredentials:
    def test_stores_credentials(self):
        creds = StaticCredentials(api_key="my-key", api_secret="my-secret")
        assert creds.api_key.get_secret_value() == "my-key"
        assert creds.api_secret.get_secret_value() == "my-secret"

    def test_serialize_returns_plain_dict(self):
        creds = StaticCredentials(api_key="my-key", api_secret="my-secret")
        serialized = creds.model_dump()
        assert serialized == {"api_key": "my-key", "api_secret": "my-secret"}

    def test_secret_str_hidden_in_repr(self):
        creds = StaticCredentials(api_key="my-key", api_secret="my-secret")
        repr_str = repr(creds)
        assert "my-key" not in repr_str
        assert "my-secret" not in repr_str


class TestEnvCredentials:
    def test_reads_from_env(self, monkeypatch: MonkeyPatch):
        monkeypatch.setenv("BUDA_API_KEY", "env-key")
        monkeypatch.setenv("BUDA_API_SECRET", "env-secret")
        creds = EnvCredentials()
        assert creds.api_key.get_secret_value() == "env-key"
        assert creds.api_secret.get_secret_value() == "env-secret"

    def test_missing_env_raises(self, monkeypatch: MonkeyPatch):
        monkeypatch.delenv("BUDA_API_KEY", raising=False)
        monkeypatch.delenv("BUDA_API_SECRET", raising=False)
        with pytest.raises(ValidationError):
            EnvCredentials()

    def test_serialize(self, monkeypatch: MonkeyPatch):
        monkeypatch.setenv("BUDA_API_KEY", "env-key")
        monkeypatch.setenv("BUDA_API_SECRET", "env-secret")
        creds = EnvCredentials()
        serialized = creds.model_dump()
        assert serialized == {"api_key": "env-key", "api_secret": "env-secret"}


class TestDotEnvCredentials:
    def test_reads_from_dotenv(self, tmp_path: Path):
        env_file = tmp_path / ".env"
        env_file.write_text("BUDA_API_KEY=dotenv-key\nBUDA_API_SECRET=dotenv-secret\n")
        creds = DotEnvCredentials(env_file=str(env_file))
        assert creds.api_key.get_secret_value() == "dotenv-key"
        assert creds.api_secret.get_secret_value() == "dotenv-secret"

    def test_ignores_env_vars(self, tmp_path: Path, monkeypatch: MonkeyPatch):
        monkeypatch.setenv("BUDA_API_KEY", "env-key")
        monkeypatch.setenv("BUDA_API_SECRET", "env-secret")
        env_file = tmp_path / ".env"
        env_file.write_text("BUDA_API_KEY=dotenv-key\nBUDA_API_SECRET=dotenv-secret\n")
        creds = DotEnvCredentials(env_file=str(env_file))
        # DotEnvCredentials uses only dotenv source, not env vars
        assert creds.api_key.get_secret_value() == "dotenv-key"

    def test_missing_file_raises(self, tmp_path: Path):
        with pytest.raises(ValidationError):
            DotEnvCredentials(env_file=str(tmp_path / "nonexistent.env"))

    def test_serialize(self, tmp_path: Path):
        env_file = tmp_path / ".env"
        env_file.write_text("BUDA_API_KEY=k\nBUDA_API_SECRET=s\n")
        creds = DotEnvCredentials(env_file=str(env_file))
        serialized = creds.model_dump()
        assert serialized == {"api_key": "k", "api_secret": "s"}
