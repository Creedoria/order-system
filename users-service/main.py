""" User Service main entry point """
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import users
from app.api.utils.custom_utils import TokenVerificationMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.model.user_model import User  # noqa: F401 - needed for table creation


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.SERVICE_NAME, description="Manages user lifecycle (create, read, update, delete).", version="0.1.0", lifespan=lifespan)
app.add_middleware(TokenVerificationMiddleware)
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

    