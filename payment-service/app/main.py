"""Payment Service - FastAPI entry point."""
from fastapi import FastAPI

from app.api.v1 import payments
from app.core.config import settings

app = FastAPI(
    title="Payment Service",
    description="Manages payment processing.",
    version="0.1.0",
)

app.include_router(payments.router, prefix="/api/v1/payments", tags=["payments"])


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok", "service": settings.SERVICE_NAME}


@app.get("/", tags=["root"])
def root() -> dict:
    return {
        "service": settings.SERVICE_NAME,
        "docs": "/docs",
        "health": "/health",
    }
