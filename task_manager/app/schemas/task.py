# app/schemas/task.py
from pydantic import BaseModel
from app.schemas.projects import ProjectResponse
from app.schemas.user import UserResponse

#schemat podstawowy
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str | None = "todo"

#schemat do tworzenia projektu
class TaskCreate(TaskBase):
    pass
#schemat do updatow
class TaskUpdate(TaskBase):
    pass
#schemat do zwracania info
class TaskResponse(TaskBase):
    id: int
    user: UserResponse | None = None  #pelne dane usera
    project: ProjectResponse | None = None  #pelne dane projektu

    class Config:
        from_attributes = True
