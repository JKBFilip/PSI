from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
import enum
from app.models.projects import Project  # Importujemy Project tutaj

class TaskStatus(str, enum.Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.NEW)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_user_id = Column(Integer, ForeignKey("users.id"))

    # Relacje
    project = relationship("Project", back_populates="tasks")
    assigned_user = relationship("User", back_populates="tasks")
