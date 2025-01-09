
from app.models.user import User
from app.core.security import create_access_token, verify_password
from app.models.database import SessionLocal
from app.schemas.user_schema import UserCreate

def authenticate_user(user: UserCreate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user and verify_password(user.password, db_user.hashed_password):
        return create_access_token({"sub": db_user.email})
    return None
