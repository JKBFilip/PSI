# app/schemas/project.py
from pydantic import BaseModel
#bazowy schemat
class ProjectBase(BaseModel):
    name: str
    description: str | None = None
#schemat do tworzenia
class ProjectCreate(ProjectBase):
    pass
#schemat do updatow
class ProjectUpdate(ProjectBase):
    pass
#schemat do zwracania
class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True
