"""Golden Horizon AI Backend - FastAPI application entrypoint.

Phase 1 foundation. Boots a FastAPI app and mounts the health router.
Database, connectors, auth, and business logic arrive in later phases.

Run locally:
    uvicorn backend.main:app --reload
"""
from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.health import router as health_router

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("golden_horizon")

APP_ENV = os.getenv("APP_ENV", "development")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Golden Horizon AI Backend (env=%s)", APP_ENV)
    # Phase 2+: initialise the async DB engine / connection pool here.
    yield
    logger.info("Shutting down Golden Horizon AI Backend")


app = FastAPI(
    title="Golden Horizon AI Backend",
    description=(
        "AI infrastructure for Golden Horizon. The backend is the source of "
        "truth between WooCommerce, OpenClaw and Claude."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# Routers
app.include_router(health_router)


@app.get("/", tags=["system"])
async def root() -> dict[str, str]:
    return {"service": "golden-horizon-backend", "version": "0.1.0"}
