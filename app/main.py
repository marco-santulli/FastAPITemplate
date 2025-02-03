import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.api.v1.api import api_router

log = logging.getLogger(__name__)

def create_application() -> FastAPI:
    """Create FastAPI application."""
    log.info(f"Creating FastAPI application with name: {settings.PROJECT_NAME}")
    log.info(f"API prefix: {settings.API_V1_PREFIX}")
    log.info(f"Auth token URL: {settings.AUTH_TOKEN_URL}")
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="REST API with JWT Authentication",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    )

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app

app = create_application()

@app.on_event("startup")
async def startup_event():
    log.info("Starting up FastAPI application")
    # Print out all settings for debugging (except sensitive ones)
    log.info(f"Project Name: {settings.PROJECT_NAME}")
    log.info(f"API Prefix: {settings.API_V1_PREFIX}")
    log.info(f"Auth Token URL: {settings.AUTH_TOKEN_URL}")

@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down FastAPI application")