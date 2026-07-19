from pydantic import BaseModel
from datetime import datetime

class OrderOut(BaseModel):
    id: int
    user_id: int
    order_id: int
    item_id: int
    quantity: int
    unit_price: str
    line_total: datetime