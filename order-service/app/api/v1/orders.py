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

@router.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        one = db.execute(text("SELECT 1")).scalar()
        version = db.execute(text("SELECT version()")).scalar()
        return {"db_check": one, "db_version": version}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database check failed: {str(e)}")