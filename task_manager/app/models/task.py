# app/models/task.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="todo")  # Status może mieć wartości np. "todo", "in_progress", "done"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # Przypisanie do użytkownika
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)  # Przypisanie do projektu
