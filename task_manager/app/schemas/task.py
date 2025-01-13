# app/schemas/task.py
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str | None = "todo"
    user_id: int | None = None  # ID przypisanego użytkownika
    project_id: int | None = None  # ID przypisanego projektu

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True
