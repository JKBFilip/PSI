from typing import Optional
from pydantic import BaseModel

class Task(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    status: str  # Możliwe wartości: "todo", "in_progress", "done"
    assignee_id: Optional[int]
    project_id: Optional[int]
