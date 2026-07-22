from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class CartStatus(str, Enum):
    ACTIVE = "active"
    ORDERED = "ordered"
    ABANDONED = "abandoned"


# ---- Request schemas (what the client sends) ----

class CartItem(BaseModel):
    item_id: int
    quantity: int = Field(gt=0, le=100)   # must be positive, sane upper bound


# Note: no request schema needed for cart creation at all —
# the cart is auto-created server-side when the first item is added.


# ---- Response schemas (what the API returns) ----

class CartItemResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    unit_price: float
    added_at: datetime

    model_config = {"from_attributes": True}


class CartResponse(BaseModel):
    id: int
    user_id: int
    status: CartStatus
    created_at: datetime
    updated_at: datetime
    items: list[CartItemResponse] = []

    model_config = {"from_attributes": True}