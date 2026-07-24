"""Application configuration from environment variables."""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

CorrelationIdBehavior = Literal["replace", "reject"]

CORRELATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]{8,128}$")


class Settings(BaseSettings):
    """Typed KRDT API configuration."""

    model_config = SettingsConfigDict(
        env_prefix="KRDT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str
    database_connect_timeout_seconds: int = Field(default=5, ge=1, le=60)
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    correlation_id_behavior: CorrelationIdBehavior = "replace"
    service_name: str = "krdt-api"
    app_version: str = "0.1.0"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> list[str]:
        if isinstance(value, str):
            origins = [item.strip() for item in value.split(",") if item.strip()]
        elif isinstance(value, list):
            origins = [str(item).strip() for item in value if str(item).strip()]
        else:
            raise ValueError("KRDT_CORS_ORIGINS must be a comma-separated list or list value")

        for origin in origins:
            if origin == "*":
                raise ValueError("Wildcard CORS origins are not permitted")
        return origins

    @field_validator("database_connect_timeout_seconds")
    @classmethod
    def validate_timeout(cls, value: int) -> int:
        if value < 1 or value > 60:
            raise ValueError("KRDT_DATABASE_CONNECT_TIMEOUT_SECONDS must be between 1 and 60")
        return value


@lru_cache
def get_settings() -> Settings:
    """Return cached settings loaded from the environment."""

    return Settings()  # type: ignore[call-arg]


def validate_correlation_id(value: str | None, behavior: CorrelationIdBehavior) -> str | None:
    """Validate an incoming correlation ID according to configured behavior."""

    if value is None:
        return None
    if CORRELATION_ID_PATTERN.fullmatch(value):
        return value
    if behavior == "reject":
        return None
    return None


def redact_database_url(database_url: str) -> str:
    """Return a log-safe database URL with credentials removed."""

    return re.sub(r"://([^:/@]+):([^@/]+)@", r"://\1:***@", database_url)
