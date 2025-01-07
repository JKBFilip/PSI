from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.base import Base

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Tworzenie silnika bazy danych
engine = create_async_engine(DATABASE_URL, echo=True)

# Tworzenie asynchronicznej sesji
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Funkcja inicjalizująca bazę danych
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
