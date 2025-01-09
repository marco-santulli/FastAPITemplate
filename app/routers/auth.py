
from logging import getLogger

logger = getLogger(__name__)


from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import UserCreate, Token
from app.services.user_service import authenticate_user, create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    token = authenticate_user(user)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
