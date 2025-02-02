import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.core.config import settings
from app.api.v1.api import api_router

log = logging.getLogger(__name__)

def create_application() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "persistAuthorization": True
        }
    )

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=settings.PROJECT_NAME,
            version="1.0.0",
            description="FastAPI template with JWT authentication",
            routes=app.routes,
        )

        # Custom security scheme
        openapi_schema["components"] = {
            "securitySchemes": {
                "Bearer": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "description": "Enter: **'Bearer &lt;JWT&gt;'** where JWT is the access token"
                }
            }
        }

        # Apply security globally to all routes
        openapi_schema["security"] = [{"Bearer": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app

app = create_application()

@app.on_event("startup")
async def startup_event():
    log.info("Starting up FastAPI application")

@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down FastAPI application")