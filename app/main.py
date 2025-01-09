
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.user import User
from app.utils.security import verify_password
from app.routers import user

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

# Add authentication security to all routes
app.include_router(
    user.router, 
    prefix="/users", 
    tags=["users"], 
    dependencies=[Depends(authenticate)]
)

# Add the security scheme to Swagger
@app.on_event("startup")
def customize_openapi():
    if not app.openapi_schema:
        app.openapi_schema = app.openapi()
    app.openapi_schema["components"]["securitySchemes"] = {
        "basicAuth": {"type": "http", "scheme": "basic"}
    }
    for path, methods in app.openapi_schema["paths"].items():
        for method in methods:
            methods[method]["security"] = [{"basicAuth": []}]
