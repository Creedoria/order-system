from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("/get-users")
def get_users(db: Session = Depends(get_db)):
    # Logic to retrieve users from the database
    users = db.query().all()
    return users