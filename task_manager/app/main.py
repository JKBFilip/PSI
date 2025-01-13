from fastapi import FastAPI
from app.routers import users, projects, tasks
from app.db import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Przekazuje kontrolę do serwera FastAPI, gdy aplikacja jest uruchomiona

app = FastAPI(lifespan=lifespan)

# Rejestracja routerów
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
