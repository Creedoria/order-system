""" User Service main entry point """
from fastapi import FastAPI

from app.api.v1 import users
from app.core.config import settings

app = FastAPI(title=settings.SERVICE_NAME,  description="Manages user lifecycle (create, read, update, delete).", version="0.1.0")
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

