from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    role: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str  # Hasło podczas tworzenia użytkownika

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
