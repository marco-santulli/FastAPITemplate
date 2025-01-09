
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.user import User
from app.utils.security import verify_password

app = FastAPI()

security = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate(credentials: HTTPBasicCredentials, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

@app.middleware("http")
async def auth_middleware(request, call_next):
    if request.url.path in ["/docs", "/redoc"] or request.url.path.startswith("/users"):
        auth = HTTPBasicCredentials(
            username=request.headers.get("username", ""),
            password=request.headers.get("password", ""),
        )
        authenticate(auth, next(get_db()))
    response = await call_next(request)
    return response
