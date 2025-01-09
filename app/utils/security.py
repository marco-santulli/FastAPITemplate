
from passlib.context import CryptContext

# Configure Passlib to use bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    logger.info('Entering get_password_hash')
def get_password_hash(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    logger.info('Entering verify_password')
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)
