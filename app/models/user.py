
from sqlalchemy import Column, Integer, String
from app.models.database import Base

class User(Base):
    __tablename__ = "t_user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
