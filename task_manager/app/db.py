# app/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#asynchroniczna baza danych
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
#asynchroniczny silnik
engine = create_async_engine(DATABASE_URL, future=True, echo=False)
#tworzenie sesji
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

#funkcja do uzyskania sesji DB
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
