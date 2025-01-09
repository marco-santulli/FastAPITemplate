
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.services.user_service import (
    create_user_service,
    get_user_service,
    update_user_service,
    delete_user_service,
)
from app.models.user import User

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(payload, db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_service(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return update_user_service(user_id, payload, db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    delete_user_service(user_id, db)
    return {"message": "User deleted successfully"}
