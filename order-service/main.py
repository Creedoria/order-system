"""Order Service - FastAPI entry point."""
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.orders import orders
from app.api.v1.items import item
from app.api.v1.search import search_item
from app.api.v1.cart import cart
from app.core.config import settings

# redis
from contextlib import asynccontextmanager
from redis.asyncio import Redis
from app.core import redis as redis_module

@asynccontextmanager
async def lifespan (app: FastAPI):
    redis_module.redis_client = Redis.from_url( "redis://localhost:6379/0", encoding="utf-8", decode_responses=True,)
    yield
    await redis_module.redis_client.aclose()

# Create the FastAPI application instance
app = FastAPI(
    title="Order Service",
    description="Manages order lifecycle (create, read, cancel).",
    version="0.1.0",
    lifespan=lifespan
)


# Register routers — this attaches the order endpoints under /api/v1/orders
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])
app.include_router(item.router, prefix="/api/v1/items", tags=["items"])
app.include_router(search_item.router, prefix="/api/v1/search", tags=["search"])
app.include_router(cart.router, prefix="/api/v1/cart", tags=["cart"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

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