
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.models.database import SessionLocal
from app.models.user import User
from app.utils.security import verify_password, get_password_hash
from app.routers import user

# Constants for JWT
SECRET_KEY = "supersecretkey"  # Replace with a secure secret
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define log format
)
logger = logging.getLogger(__name__)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Dependency to get the database session
def get_db():
    logger.info('Entering get_db')
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    pass
# Create JWT Token
    logger.info('Entering create_access_token')
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    pass
# Authenticate user and generate token
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info('Entering login')
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
    pass
# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    logger.info('Entering get_current_user')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    pass
# Include routes with token authentication
app.include_router(
    user.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)
    pass
# Add security schema for Swagger
@app.on_event("startup")
def customize_openapi():
    logger.info('Entering customize_openapi')
    if not app.openapi_schema:
        app.openapi_schema = app.openapi()
    app.openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Use the /login endpoint to get a JWT token."
        }
    }
    for path, methods in app.openapi_schema["paths"].items():
        for method in methods:
            methods[method]["security"] = [{"bearerAuth": []}]
