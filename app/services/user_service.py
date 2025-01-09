
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.utils.security import get_password_hash
from typing import List, Optional

def create_user_service(user_data: UserCreate, db: Session):
    if user_data.hashed_password:
        hashed_password = user_data.hashed_password
    else:
        hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_service(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()

def list_users_service(db: Session, email: Optional[str], full_name: Optional[str], limit: int, offset: int) -> List[User]:
    query = db.query(User)
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if full_name:
        query = query.filter(User.full_name.ilike(f"%{full_name}%"))
    return query.offset(offset).limit(limit).all()

def update_user_service(user_id: int, user_data: UserUpdate, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_data.email:
        user.email = user_data.email
    if user_data.full_name:
        user.full_name = user_data.full_name
    if user_data.password:
        user.hashed_password = get_password_hash(user_data.password)
    db.commit()
    db.refresh(user)
    return user

def delete_user_service(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
