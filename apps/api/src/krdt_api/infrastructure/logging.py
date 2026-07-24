"""Structured logging configuration."""

from __future__ import annotations

import json
import logging
import sys
import uuid
from datetime import UTC, datetime
from typing import Any

from krdt_api.config import Settings, redact_database_url


class JsonLogFormatter(logging.Formatter):
    """Format log records as single-line JSON objects."""

    def __init__(self, service: str, environment: str) -> None:
        super().__init__()
        self.service = service
        self.environment = environment

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "service": self.service,
            "environment": self.environment,
            "message": record.getMessage(),
            "logger": record.name,
        }
        for field in (
            "correlation_id",
            "request_method",
            "request_path",
            "response_status",
            "duration_ms",
        ):
            if hasattr(record, field):
                payload[field] = getattr(record, field)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=True)


def configure_logging(settings: Settings) -> None:
    """Configure root logging with JSON output."""

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonLogFormatter(settings.service_name, settings.environment))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(settings.log_level.upper())


def generate_correlation_id() -> str:
    """Generate a new correlation identifier."""

    return str(uuid.uuid4())


def log_safe_database_url(settings: Settings) -> str:
    """Return a redacted database URL for logging."""

    return redact_database_url(settings.database_url)
