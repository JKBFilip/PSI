# app/services/users_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate


async def create_user(db: AsyncSession, user_data: UserCreate):
    #walidacja czy nie powiela sie email
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise ValueError("User with this email already exists.")

    #tworzenie uzytkownika
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

#wyswietlanie uzytkownikow wszystkich
async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

#wyswietlanie po ID
async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise ValueError("User not found.")
    return user

#aktualizacja danych
async def update_user(db: AsyncSession, user_id: int, user_data: UserCreate):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise ValueError("User not found.")

    user.name = user_data.name
    user.email = user_data.email
    user.password = user_data.password
    await db.commit()      #przepchanie danych a nizej odswiezenie DB
    await db.refresh(user)
    return user

#usuwanie
async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise ValueError("User not found.")

    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}

