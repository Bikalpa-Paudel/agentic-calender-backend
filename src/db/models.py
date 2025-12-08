# from src.db.base import Base
from sqlalchemy.orm import declarative_base
from sqlalchemy import String, Column, Integer

Base = declarative_base()

class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(265), nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
