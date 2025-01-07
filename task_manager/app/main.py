from fastapi import FastAPI
from app.routers import tasks, users, projects
from app.db import init_db
import logging

# Ustawienia loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicjalizacja aplikacji
app = FastAPI(title="Task Manager API")

# Inicjalizacja bazy danych
@app.on_event("startup")
async def startup():
    try:
        await init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing the database: {e}")

# Rejestracja routerów
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Task Manager API!"}
