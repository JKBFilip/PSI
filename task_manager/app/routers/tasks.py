# app/routers/tasks.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.tasks_service import (
    create_task,
    update_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    assign_task_to_user,
    assign_task_to_project,
    update_task_status
)
from app.db import get_db
from typing import List

#router na endpointy taskow
router = APIRouter(prefix="/tasks", tags=["Tasks"])

#tworzenie taska
@router.post("/", response_model=TaskResponse)
async def create_new_task(task_data: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await create_task(db=db, task_data=task_data)

#edycja taska
@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(task_id: int, task_data: TaskUpdate, db: AsyncSession = Depends(get_db)):
    return await update_task(db=db, task_id=task_id, task_data=task_data)

#usuwanie taska po ID
@router.delete("/{task_id}")
async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_task(db=db, task_id=task_id)

#pobieranie taskow wszystkich
@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks_list(db: AsyncSession = Depends(get_db)):
    return await get_all_tasks(db=db)

#pobieranie jednego po ID
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    return await get_task_by_id(db=db, task_id=task_id)

#przypisanie taska do usera
@router.put("/{task_id}/assign-user/{user_id}", response_model=TaskResponse)
async def assign_user_to_task(task_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    return await assign_task_to_user(db=db, task_id=task_id, user_id=user_id)

#przypisanie taska do projektu
@router.put("/{task_id}/assign-project/{project_id}", response_model=TaskResponse)
async def assign_project_to_task(task_id: int, project_id: int, db: AsyncSession = Depends(get_db)):
    return await assign_task_to_project(db=db, task_id=task_id, project_id=project_id)

#zmiana statusu (string)
@router.put("/{task_id}/status/")
async def change_task_status(task_id: int, status: str, db: AsyncSession = Depends(get_db)):
    return await update_task_status(db=db, task_id=task_id, status=status)
