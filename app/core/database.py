import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from typing import Dict
from .config import settings

log = logging.getLogger(__name__)

# Database-specific configuration
DB_CONFIG: Dict[str, Dict] = {
    "sqlite": {
        "pool_size": None,  # SQLite doesn't support pooling
        "max_overflow": None,
        "connect_args": {"check_same_thread": False}
    },
    "postgresql": {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
        "connect_args": {}
    },
    "mysql": {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
        "connect_args": {}
    }
}

def get_engine_config():
    """Get database-specific engine configuration."""
    db_type = settings.DB_TYPE.lower()
    if db_type not in DB_CONFIG:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    config = DB_CONFIG[db_type].copy()
    
    # Use QueuePool for databases that support it
    if config["pool_size"] is not None:
        config["poolclass"] = QueuePool
    
    return config

# Create database engine with appropriate configuration
try:
    engine_config = get_engine_config()
    connect_args = engine_config.pop("connect_args", {})
    
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        echo=settings.DB_ECHO_LOG,  # SQL query logging
        **engine_config
    )
    log.info(f"Database engine created successfully for {settings.DB_TYPE}")
except Exception as e:
    log.error(f"Error creating database engine: {str(e)}")
    raise

# Create sessionmaker with the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

def get_db():
    """
    Get database session with automatic cleanup.
    To be used as a FastAPI dependency.
    """
    db = SessionLocal()
    try:
        log.debug("Creating new database session")
        yield db
    finally:
        log.debug("Closing database session")
        db.close()