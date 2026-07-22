from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db
from pydantic import BaseModel, Field

router = APIRouter()

class SearchItem(BaseModel):
    search_query: str = Field(..., description="The search query to look for in item name, description, or SKU.")

@router.post("/search-items")
def search_items(search_item: SearchItem, limit: int | None = 10, offset: int | None = 0, db: Session = Depends(get_db)):
    try:
        stmt = text("SELECT * FROM items WHERE name LIKE :query OR description LIKE :query OR sku LIKE :query LIMIT :limit OFFSET :offset")
        items = db.execute(stmt, {"query": f"%{search_item.search_query}%", "limit": limit, "offset": offset}).fetchall()
        return {"items": [dict(item._mapping) for item in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search items: {str(e)}")