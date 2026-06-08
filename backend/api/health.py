"""Health check endpoints.

Used by container health checks, the reverse proxy, and uptime monitors.
"""
from __future__ import annotations

import os

from fastapi import APIRouter

router = APIRouter(tags=["system"])

APP_ENV = os.getenv("APP_ENV", "development")


@router.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe. Returns 200 while the process is up."""
    return {"status": "ok", "service": "fastapi", "env": APP_ENV}


@router.get("/health/ready")
async def readiness() -> dict[str, str]:
    """Readiness probe.

    Phase 1 reports ready as soon as the app is serving. Phase 2 will extend
    this to verify the PostgreSQL connection before reporting ready.
    """
    return {"status": "ready"}
