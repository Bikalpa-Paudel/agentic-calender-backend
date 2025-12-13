# from src.db.base import Base
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, Column, Integer, TIMESTAMP, func, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(265), nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    picture = Column(String(256), nullable=True)
    provider = Column(String(256), nullable=False)
    access_token=Column(String(256), nullable=False)
    refresh_token=Column(String(256), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    integrations = relationship("Ingegrations", back_populates="user")

class Ingegrations(Base):
    __tablename__ = 'integrations'
    id = Column(Integer,  primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at  = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="integrations")