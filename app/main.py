
from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="FastAPI Template Project", version="1.0.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
