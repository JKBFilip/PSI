# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.users_service import (
    create_user, get_all_users, update_user, delete_user, get_user_by_id
)

#router dla endpointów userow
router = APIRouter(prefix="/users", tags=["Users"])

#endpoint do tworzenia userow
@router.post("/", response_model=UserResponse)
async def create_new_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_user(db=db, user_data=user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

#endpoint do pobierania listy userow
@router.get("/", response_model=list[UserResponse])
async def get_users_list(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db=db)

#endpoint do pobierania userow po id
@router.get("/users/{user_id}")
async def get_user_by_Id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#endpoint do aktualizowania userow
@router.put("/{user_id}", response_model=UserResponse)
async def update_user_data(user_id: int, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await update_user(db=db, user_id=user_id, user_data=user_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

#endpoint do usuwania userow
@router.delete("/{user_id}")
async def delete_user_data(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await delete_user(db=db, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
