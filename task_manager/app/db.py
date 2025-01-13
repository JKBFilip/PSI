# app/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Asynchroniczna wersja URL bazy danych SQLite
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Tworzenie asynchronicznego silnika
engine = create_async_engine(DATABASE_URL, future=True, echo=False)

# Tworzenie asynchronicznej sesji
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Funkcja do uzyskiwania sesji bazy danych
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
