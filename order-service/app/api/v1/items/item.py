from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.item_model import Item
from app.core.database import get_db
from sqlalchemy import text

router = APIRouter()

@router.get("/get-items")
def get_item(db: Session = Depends(get_db)):
    try:
        items = db.execute(text("SELECT * FROM items")).fetchall()
        return {"items": [dict(item._mapping) for item in items]}   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {str(e)}")

@router.post("/add-item")
def add_item(item: Item, db: Session = Depends(get_db)):
    try:
        stmt = text("INSERT INTO items (sku, name, description, price) VALUES (:sku, :name, :description, :price)")
        db.execute(stmt, {"sku": item.sku, "name": item.name, "description": item.description, "price": item.price})
        db.commit()
        return {"message": "Item added successfully", "item": item}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Something went wrong while adding the item: {str(e)}")