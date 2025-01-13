from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse
from app.services.users_service import create_user, get_all_users, get_user_by_id, update_user, delete_user
from app.db import get_db
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

# Tworzenie użytkownika
@router.post("/", response_model=UserResponse)
async def create_new_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db=db, user_data=user_data)

# Pobranie wszystkich użytkowników
@router.get("/", response_model=List[UserResponse])
async def get_users_list(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db=db)

# Pobranie użytkownika po ID
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(db=db, user_id=user_id)

# Aktualizacja użytkownika
@router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user(user_id: int, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await update_user(db=db, user_id=user_id, user_data=user_data)

# Usunięcie użytkownika
@router.delete("/{user_id}")
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_user(db=db, user_id=user_id)
