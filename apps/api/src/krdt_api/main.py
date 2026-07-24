"""FastAPI application entrypoint."""

from __future__ import annotations

import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from krdt_api.api import health
from krdt_api.api.v1.router import router as v1_router
from krdt_api.config import Settings, get_settings, validate_correlation_id
from krdt_api.infrastructure.database import create_db_engine
from krdt_api.infrastructure.logging import configure_logging, generate_correlation_id

logger = logging.getLogger(__name__)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Attach a validated correlation ID to each request and response."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        settings: Settings = request.app.state.settings
        incoming = request.headers.get("X-Correlation-ID")
        validated = validate_correlation_id(incoming, settings.correlation_id_behavior)
        correlation_id = validated or generate_correlation_id()
        request.state.correlation_id = correlation_id

        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            "request completed",
            extra={
                "correlation_id": correlation_id,
                "request_method": request.method,
                "request_path": request.url.path,
                "response_status": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        response.headers["X-Correlation-ID"] = correlation_id
        return response


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""

    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings)

    app = FastAPI(
        title="KRDT API",
        version=resolved_settings.app_version,
        description="Kundasang Resilience Digital Twin API foundation service.",
    )
    app.state.settings = resolved_settings
    app.state.engine = create_db_engine(resolved_settings)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(CorrelationIdMiddleware)
    app.include_router(health.router)
    app.include_router(v1_router)

    return app


def __getattr__(name: str) -> FastAPI:
    if name == "app":
        return create_app()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
