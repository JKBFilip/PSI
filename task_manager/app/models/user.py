# app/models/user.py
from sqlalchemy.orm import relationship
from app.db import Base
from sqlalchemy import Column, Integer, String

#model usera do bazy danych
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    #relacja z tabela taskow
    tasks = relationship("Task", back_populates="user")
