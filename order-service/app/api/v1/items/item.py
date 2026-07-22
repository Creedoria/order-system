from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.item_model import Item as ItemSchema
from app.core.database import get_db
from sqlalchemy import text
from app.core.redis import get_redis
from redis.asyncio import Redis
import json

router = APIRouter()

@router.get("/get-items")
async def get_item(limit: int | None = 10, offset: int | None = 0, r: Redis = Depends(get_redis), db: Session = Depends(get_db)):
    cache_key = f"items:{limit}:{offset}"
    cached = await r.get(cache_key)
    try:
        print(await r.keys("*"))
        if cached:
          return json.loads(cached)
        else:
          items = db.execute(text("SELECT * FROM items LIMIT :limit OFFSET :offset"), {"limit": limit, "offset": offset}).fetchall()
          results = {"items": [dict(item._mapping) for item in items]}   
          await r.set(cache_key, json.dumps(results, default=str), ex=300)
          return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {str(e)}")


# admin privileges required to add items
@router.post("/add-item")
def add_item(item: ItemSchema, db: Session = Depends(get_db)):
    try:
        stmt = text("INSERT INTO items (sku, name, description, price) VALUES (:sku, :name, :description, :price)")
        db.execute(stmt, {"sku": item.sku, "name": item.name, "description": item.description, "price": item.price})
        db.commit()
        return {"message": "Item added successfully", "item": item}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Something went wrong while adding the item: {str(e)}")