# app/models/task.py
from sqlalchemy.orm import relationship
from app.db import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey

#model do DB taska
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="todo")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)

    #relacja z tabelka userow
    user = relationship("User", back_populates="tasks")
    #relacja z tabelka projektow
    project = relationship("Project", back_populates="tasks")
