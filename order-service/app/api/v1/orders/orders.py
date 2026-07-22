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


@router.get("/ping")
def ping(user_id:str = Depends(get_current_user_id)) -> dict:
    """Placeholder endpoint - proves the router is wired up."""
    return {"message": "orders router is alive"}

@router.get("/get-all-orders")
async def order_item(db: Session = Depends(get_db), r: Redis = Depends(get_redis)):
    try:
      cached = await get_redis('orders_redis')
      print('cached :', cached)
      orders = ""
      if cached:
          orders = json.loads(cached)
          print('orders from redis :', orders)
      else:
         orders = db.execute(text("SELECT * FROM items")).fetchall()
         if not orders:
          return HTTPException(status_code=404, message = "No Data found")
         await r.set('orders_redis', json.dumps(orders))
      return { "results":{"orders": orders }, "message": "Orders fetched successfully" }
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
    
@router.get("/get-orders-userid")
def get_orders_by_id(user_id: int = Depends(get_current_user_id)):
    print(f'user_id : {user_id}')
    # query = db.execute(text("SELECT * FROM orders")).fetchall()
    # print(f"query {query}")
    return user_id

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
