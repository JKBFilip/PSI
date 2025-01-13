from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import HTTPException


# Tworzenie użytkownika
async def create_user(db: AsyncSession, user_data: UserCreate):
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# Pobranie wszystkich użytkowników
async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


# Pobranie użytkownika po ID
async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Aktualizacja użytkownika
async def update_user(db: AsyncSession, user_id: int, user_data: UserCreate):
    user = await get_user_by_id(db, user_id)
    user.name = user_data.name
    user.email = user_data.email
    await db.commit()
    await db.refresh(user)
    return user


# Usunięcie użytkownika
async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted successfully"}
