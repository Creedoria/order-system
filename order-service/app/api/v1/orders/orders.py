"""Order API routes."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user_id
from app.model.entities import Cart
from app.core.redis import get_redis
import redis.asyncio as Redis
import json

router = APIRouter()

@router.get("/get-all-orders")
async def order_item(db: Session = Depends(get_db), r: Redis = Depends(get_redis)):
    try:
      cached = await get_redis('all_orders')
      if not cached:
          orders = json.loads(cached)
      else:
         orders = db.execute(text("SELECT * FROM items LIMIT :limit, OFFSET :offset")).fetchall()
         if not orders:
          return HTTPException(status_code=404, detail = "No Data found")
         results = {"orders": orders },
         await r.set('all_orders', json.dumps(results))
      return { "results":results, "message": "Orders fetched successfully" }
    except Exception as ex:
       raise HTTPException(status_code=500, detail=f"Error : {str(ex)}")
    
@router.post("/add-order")
def add_order(order: dict, db: Session = Depends(get_db)):
    try:
        stmt = text("INSERT INTO orders (order_id, item_id, quantity) VALUES (:order_id, :item_id, :quantity)")
        db.execute(stmt, {"order_id": order["order_id"], "item_id": order["item_id"], "quantity": order["quantity"]})
        db.commit()
        return {"message": "Order added successfully", "order": order}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Something went wrong while adding the order: {str(e)}")
    
@router.get("/get-orders-user-id")
def get_orders_by_id(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    query = db.execute(text("SELECT * FROM orders WHERE user_id = :user_id"), {"user_id": user_id}).fetchall()
    if not query:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return {"orders": [dict(order._mapping) for order in query]}

@router.post("/checkout")
def checkout(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id, Cart.status == "active").first()
    if not cart or not cart.items:
        raise HTTPException(400, "Cart is empty")

    # 1. create the order from cart.items (and trigger payment)
    # ...


    # 2. close the cart
    cart.status = "ordered"
    cart.updated_at = datetime.utcnow()
    db.commit()
    return {"detail": "Order placed"}
