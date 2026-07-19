"""Order API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()


@router.get("/ping")
def ping() -> dict:
    """Placeholder endpoint - proves the router is wired up."""
    return {"message": "orders router is alive"}

@router.post("/orders")
def order_item(db: Session = Depends(get_db)):
    try:
      orders = db.execute(text("SELECT * FROM orders")).fetchall()
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
