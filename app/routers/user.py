
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import SessionLocal
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.services.user_service import (
    create_user_service,
    get_user_service,
    update_user_service,
    delete_user_service,
    list_users_service,
)
from app.models.user import User

router = APIRouter()

# Dependency to get the database session
def get_db():
    logger.info('Entering get_db')
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    logger.info('Entering create_user')
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(payload, db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    logger.info('Entering get_user')
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_service(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
def list_users(
    logger.info('Entering list_users')
def list_users(
    db: Session = Depends(get_db),
    email: Optional[str] = Query(None, description="Filter by email"),
    full_name: Optional[str] = Query(None, description="Filter by full name"),
    limit: int = Query(10, ge=1, le=100, description="Number of users to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):
    return list_users_service(db, email=email, full_name=full_name, limit=limit, offset=offset)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    logger.info('Entering update_user')
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return update_user_service(user_id, payload, db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    logger.info('Entering delete_user')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    delete_user_service(user_id, db)
    return {"message": "User deleted successfully"}
