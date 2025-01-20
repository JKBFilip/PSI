# app/schemas/user.py
from pydantic import BaseModel, EmailStr

#schemat podstawowy
class UserBase(BaseModel):
    name: str
    email: EmailStr

#schemat do tworzenia usera
class UserCreate(UserBase):
    password: str

#schemat do wyswietlania id przy zwracanych zapytaniach fastapi
class UserResponse(UserBase):
    id: int

    #konwersja obiektow na schemat Pydantic
    class Config:
        from_attributes = True
