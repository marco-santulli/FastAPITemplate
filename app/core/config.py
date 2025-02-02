import logging
from typing import List
from pydantic_settings import BaseSettings
from pydantic import EmailStr, validator

log = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str
    API_V1_PREFIX: str
    
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str]
    
    # Database settings
    DB_TYPE: str  # postgresql, mysql, or sqlite
    DB_USER: str = ""  # Optional for SQLite
    DB_PASSWORD: str = ""  # Optional for SQLite
    DB_HOST: str = ""  # Optional for SQLite
    DB_PORT: str = ""  # Optional for SQLite
    DB_NAME: str
    DB_ECHO_LOG: bool = False  # Whether to log SQL queries
    
    # Initial superuser settings
    INITIAL_SUPERUSER_EMAIL: EmailStr
    INITIAL_SUPERUSER_PASSWORD: str
    
    # Optional settings
    LOG_LEVEL: str = "INFO"
    RATE_LIMIT_PER_MINUTE: int = 100

    @validator("DB_TYPE")
    def validate_db_type(cls, v):
        allowed_dbs = ["postgresql", "mysql", "sqlite"]
        if v.lower() not in allowed_dbs:
            raise ValueError(f"Database type must be one of {allowed_dbs}")
        return v.lower()

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL based on settings."""
        if self.DB_TYPE == "sqlite":
            return f"sqlite:///{self.DB_NAME}"
        elif self.DB_TYPE == "mysql":
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:  # postgresql
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True

# Initialize settings
settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

log.info("Settings loaded successfully")