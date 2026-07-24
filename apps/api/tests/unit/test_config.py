"""Unit tests for configuration."""

import pytest

from krdt_api.config import Settings, redact_database_url, validate_correlation_id


def test_settings_parse_valid_environment_values() -> None:
    settings = Settings(
        environment="development",
        log_level="INFO",
        api_host="0.0.0.0",
        api_port=8000,
        database_url="postgresql+psycopg://krdt:secret@localhost:5432/krdt",
        database_connect_timeout_seconds=5,
        cors_origins=["http://localhost:5173"],
    )
    assert settings.environment == "development"
    assert settings.cors_origins == ["http://localhost:5173"]


def test_settings_reject_invalid_timeout_values() -> None:
    with pytest.raises(ValueError):
        Settings(
            environment="development",
            log_level="INFO",
            api_host="0.0.0.0",
            api_port=8000,
            database_url="postgresql+psycopg://krdt:secret@localhost:5432/krdt",
            database_connect_timeout_seconds=0,
            cors_origins=["http://localhost:5173"],
        )


def test_wildcard_cors_is_not_accepted() -> None:
    with pytest.raises(ValueError):
        Settings(
            environment="development",
            log_level="INFO",
            api_host="0.0.0.0",
            api_port=8000,
            database_url="postgresql+psycopg://krdt:secret@localhost:5432/krdt",
            database_connect_timeout_seconds=5,
            cors_origins=["*"],
        )


def test_malformed_correlation_id_is_replaced() -> None:
    assert validate_correlation_id("bad id!", "replace") is None


def test_valid_correlation_id_is_accepted() -> None:
    value = "abc12345-valid.correlation_id"
    assert validate_correlation_id(value, "replace") == value


def test_logging_redacts_database_credentials() -> None:
    redacted = redact_database_url("postgresql+psycopg://krdt:secret@localhost:5432/krdt")
    assert "secret" not in redacted
    assert "krdt:***@" in redacted
