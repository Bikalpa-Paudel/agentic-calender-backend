# from src.db.base import Base
from sqlalchemy.orm import declarative_base
from sqlalchemy import String, Column, Integer, TIMESTAMP, func

Base = declarative_base()

class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(265), nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
