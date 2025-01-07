from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    project_manager_id: int

class ProjectCreate(ProjectBase):
    pass  # Można dodać dodatkowe walidacje, ale na razie kopiujemy to samo

class ProjectOut(ProjectBase):
    id: int

    class Config:
        from_attributes = True
