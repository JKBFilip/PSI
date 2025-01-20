from fastapi import FastAPI
from app.routers import users, projects, tasks
from app.db import engine, Base
from contextlib import asynccontextmanager
import logging

#ustawienia logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  #przekazuje kontrole do fastApi

app = FastAPI(lifespan=lifespan)

#rejestrowanie routerow
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
