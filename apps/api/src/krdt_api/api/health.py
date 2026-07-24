"""Health endpoints for liveness and readiness probes."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.engine import Engine

from krdt_api.infrastructure.database import check_database_health

router = APIRouter(tags=["health"])


class LiveResponse(BaseModel):
    status: Literal["ok"]
    service: Literal["krdt-api"]


class ReadyResponse(BaseModel):
    status: Literal["ready"]
    database: Literal["available"]
    postgis: Literal["available"]


class NotReadyResponse(BaseModel):
    status: Literal["not_ready"]
    database: Literal["unavailable"]
    postgis: Literal["unavailable"]
    detail: str = Field(default="Required dependencies are unavailable")


@router.get("/health/live", response_model=LiveResponse)
def live() -> LiveResponse:
    """Return liveness without querying external dependencies."""

    return LiveResponse(status="ok", service="krdt-api")


@router.get(
    "/health/ready",
    responses={
        status.HTTP_200_OK: {"model": ReadyResponse},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": NotReadyResponse},
    },
)
def ready(request: Request, response: Response) -> ReadyResponse | NotReadyResponse:
    """Return readiness based on database and PostGIS availability."""

    engine: Engine = request.app.state.engine
    health = check_database_health(engine)
    if health.available and health.postgis_available:
        return ReadyResponse(status="ready", database="available", postgis="available")

    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return NotReadyResponse(
        status="not_ready",
        database="unavailable",
        postgis="unavailable",
        detail="Required dependencies are unavailable",
    )
