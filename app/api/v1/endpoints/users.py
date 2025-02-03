import logging
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, oauth2_scheme  # Move oauth2_scheme to security.py
from app.services import (
    get_user_by_id, get_user_by_email, create_user, update_user,
    authenticate_user, get_users
)
from app.schemas.user import (
    User, UserCreate, UserUpdate, Token, UserSearchParams, PaginatedResponse
)

log = logging.getLogger(__name__)
router = APIRouter()

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            log.warning("JWT token missing 'sub' claim")
            raise credentials_exception
    except JWTError as e:
        log.error(f"JWT token validation error: {str(e)}")
        raise credentials_exception

    user = get_user_by_id(db, int(user_id))
    if user is None:
        log.warning(f"User with ID {user_id} not found")
        raise credentials_exception
    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Check if current user is superuser."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges"
        )
    return current_user

@router.post("/register", 
             response_model=User,
             status_code=status.HTTP_201_CREATED,
             summary="Register a new user",
             description="Create a new user account with the provided details.")
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """Register a new user."""
    user = get_user_by_email(db, email=user_in.email)
    if user:
        log.warning(f"Registration failed: Email {user_in.email} already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    try:
        user = create_user(db, user_in)
        log.info(f"Successfully registered user with ID: {user.id}")
        return user
    except Exception as e:
        log.error(f"Error during user registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user",
        )

@router.post("/login",
             response_model=Token,
             summary="Login to get access token",
             description="""
             Login with email and password to get JWT token.
             Use the token in the 'Authorize' button at the top of this page.
             """)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get JWT access token.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me",
            response_model=User,
            summary="Get current user",
            description="Get details of currently logged in user",
            dependencies=[Depends(oauth2_scheme)])
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user.
    """
    return current_user

@router.put("/me",
            response_model=User,
            summary="Update current user",
            description="Update information for the currently logged in user",
            dependencies=[Depends(oauth2_scheme)])
async def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update own user.
    """
    user = update_user(db, current_user, user_in)
    return user

@router.get("/",
            response_model=PaginatedResponse,
            summary="List users",
            description="Get list of users. Only available to superusers.",
            dependencies=[Depends(oauth2_scheme)])
async def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search_params: UserSearchParams = Depends(),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Retrieve users. Only superusers can access this endpoint.
    """
    users, total = get_users(db, skip=skip, limit=limit, search_params=search_params)
    return {
        "items": users,
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit
    }