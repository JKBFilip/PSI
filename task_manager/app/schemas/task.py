from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

# Status zadania (TaskStatus)
class TaskStatus(str, Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

# Bazowy schemat dla Task
class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.NEW
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    project_id: int
    assigned_user_id: int

# Schemat do tworzenia Task
class TaskCreate(TaskBase):
    pass  # Używamy dokładnie tego samego schematu co w TaskBase, ale dedykowane do tworzenia

# Schemat do aktualizacji Task
class TaskUpdate(TaskBase):
    pass  # Możemy użyć tego samego schematu, ale z dodatkowymi opcjami

# Schemat dla odpowiedzi na zapytanie o Task
class TaskOut(TaskBase):
    id: int  # ID zadania, które będzie zwrócone w odpowiedzi

    class Config:
        from_attributes = True  # Ważne, aby FastAPI mogło konwertować z SQLAlchemy na Pydantic
