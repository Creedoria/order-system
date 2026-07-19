from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.user_model import User
from app.api.schemas.user_schema import UserCreate, UserLogin, TokenResponse, UserResponse
from app.core.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/get-users")
def get_users(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        users = db.query(User).all()
        return {"results": {"users": [{"id": user.id, "full_name": user.full_name, "email": user.email} for user in users]}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")
  
@router.post("/create-user")
def add_user(user: UserCreate, db: Session = Depends(get_db)) -> None:
    try:
        existing = db.query(User).filter(User.email == user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed = hash_password(user.password)
        db_user = User(full_name=user.full_name, email=user.email, hashed_password=hashed)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User added successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Something went wrong while adding the user: {str(e)}")

@router.get("/get-user-by-id/{user_id}")
def get_users_by_id(user_id : int , db : Session = Depends(get_db)):
    existing = db.query(User).filter(User.id == user_id).first()
    if not existing:
        return HTTPException(status_code=404, message = "No Data Found")
    return { "results" : {existing }}
