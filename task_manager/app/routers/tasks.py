from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import AsyncSessionLocal
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services.tasks_service import create_task, get_task_by_id, get_tasks, update_task, delete_task

import logging

# Ustawienia loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Dependency: Funkcja do uzyskania asynchronicznej sesji bazy danych
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# POST: Tworzenie nowego taska
@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_new_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    logger.info("Tworzenie nowego taska")
    try:
        new_task = await create_task(db=db, task=task)
        return new_task
    except Exception as e:
        logger.error(f"Blad podczas tworzenia taska: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# GET: Pobieranie taska po ID
@router.get("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Pobieranie taska o ID: {task_id}")
    db_task = await get_task_by_id(db, task_id=task_id)
    if not db_task:
        logger.warning(f"Task o ID {task_id} nie znaleziony")
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# GET: Pobieranie wszystkich tasków
@router.get("/", response_model=list[TaskOut], status_code=status.HTTP_200_OK)
async def read_tasks(db: AsyncSession = Depends(get_db)):
    logger.info("Pobieranie wszystkich taskow")
    try:
        tasks = await get_tasks(db)
        return tasks
    except Exception as e:
        logger.error(f"Blad podczas pobierania taskow: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# PUT: Aktualizacja istniejącego taska
@router.put("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def update_existing_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Aktualizacja taska o ID: {task_id}")
    updated_task = await update_task(db=db, task_id=task_id, task=task)
    if not updated_task:
        logger.warning(f"Task o ID {task_id} nie znaleziony do aktualizacji")
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# DELETE: Usuwanie istniejącego taska
@router.delete("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Usuwanie taska o ID: {task_id}")
    deleted_task = await delete_task(db=db, task_id=task_id)
    if not deleted_task:
        logger.warning(f"Task o ID {task_id} nie znaleziony do usuniecia")
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
