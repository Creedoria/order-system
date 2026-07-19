"""Order Service - FastAPI entry point."""
from fastapi import FastAPI

from app.api.v1.orders import orders
from app.api.v1.items import item
from app.core.config import settings

# Create the FastAPI application instance
app = FastAPI(
    title="Order Service",
    description="Manages order lifecycle (create, read, cancel).",
    version="0.1.0",
)

# Register routers — this attaches the order endpoints under /api/v1/orders
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])
app.include_router(item.router, prefix="/api/v1/items", tags=["items"])


@app.get("/health", tags=["health"])
def health_check() -> dict:
    """Simple liveness probe. Used to check if the service is running."""
    return {"status": "ok", "service": settings.SERVICE_NAME}


@app.get("/", tags=["root"])
def root() -> dict:
    """Root endpoint - shows where to find docs and health."""
    return {
        "service": settings.SERVICE_NAME,
        "docs": "/docs",
        "health": "/health",
    }