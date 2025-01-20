# app/models/project.py
from sqlalchemy.orm import relationship
from app.db import Base
from sqlalchemy import Column, Integer, String, Text

#model projektow do DB
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    #relacja do tabelki task
    tasks = relationship("Task", back_populates="project")
