from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    sku: str
    name: str
    description: str
    price: float
    created_at: str | None = None
    updated_at: str | None = None
