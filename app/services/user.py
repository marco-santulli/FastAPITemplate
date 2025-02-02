import logging
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserCreateInternal, UserUpdate, UserSearchParams

log = logging.getLogger(__name__)

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    log.debug(f"Fetching user with ID: {user_id}")
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    log.debug(f"Fetching user with email: {email}")
    return db.query(User).filter(User.email == email).first()

def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search_params: Optional[UserSearchParams] = None
) -> Tuple[List[User], int]:
    """
    Get users with optional search parameters.
    Returns tuple of (users, total_count)
    """
    query = db.query(User)
    
    if search_params:
        if search_params.email:
            query = query.filter(User.email.ilike(f"%{search_params.email}%"))
        if search_params.full_name:
            query = query.filter(User.full_name.ilike(f"%{search_params.full_name}%"))
        if search_params.is_active is not None:
            query = query.filter(User.is_active == search_params.is_active)
    
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    
    return users, total

def create_user(db: Session, user_in: UserCreate | UserCreateInternal) -> User:
    """Create new user."""
    log.info(f"Creating new user with email: {user_in.email}")
    data = user_in.model_dump()
    if 'password' in data:
        data['hashed_password'] = get_password_hash(data.pop('password'))
    
    db_user = User(**data)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        log.info(f"Successfully created user with ID: {db_user.id}")
        return db_user
    except Exception as e:
        log.error(f"Error creating user: {str(e)}")
        db.rollback()
        raise

def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    """Update user details."""
    log.info(f"Updating user with ID: {user.id}")
    update_data = user_in.model_dump(exclude_unset=True)
    
    if update_data.get("password"):
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password

    for field, value in update_data.items():
        setattr(user, field, value)

    try:
        db.commit()
        db.refresh(user)
        log.info(f"Successfully updated user with ID: {user.id}")
        return user
    except Exception as e:
        log.error(f"Error updating user: {str(e)}")
        db.rollback()
        raise

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user by email and password."""
    user = get_user_by_email(db, email)
    if not user:
        log.warning(f"Authentication failed: User with email {email} not found")
        return None
    if not verify_password(password, user.hashed_password):
        log.warning(f"Authentication failed: Invalid password for user {email}")
        return None
    return user