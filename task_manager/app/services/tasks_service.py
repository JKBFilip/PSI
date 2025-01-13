from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.task import Task
from app.models.user import User
from app.models.projects import Project
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException


# Tworzenie zadania
async def create_task(db: AsyncSession, task_data: TaskCreate):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


# Edycja zadania
async def update_task(db: AsyncSession, task_id: int, task_data: TaskUpdate):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status
    task.user_id = task_data.user_id
    task.project_id = task_data.project_id
    await db.commit()
    await db.refresh(task)
    return task


# Usuwanie zadania
async def delete_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return {"detail": "Task deleted successfully"}


# Pobranie wszystkich zadań
async def get_all_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return tasks


# Pobranie zadania po ID
async def get_task_by_id(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Przypisanie zadania do użytkownika
async def assign_task_to_user(db: AsyncSession, task_id: int, user_id: int):
    task = await get_task_by_id(db, task_id)
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    task.user_id = user_id
    await db.commit()
    await db.refresh(task)
    return task


# Przypisanie zadania do projektu
async def assign_task_to_project(db: AsyncSession, task_id: int, project_id: int):
    task = await get_task_by_id(db, task_id)
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    task.project_id = project_id
    await db.commit()
    await db.refresh(task)
    return task


# Zmiana statusu zadania
async def update_task_status(db: AsyncSession, task_id: int, status: str):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Aktualizacja statusu
    task.status = status
    await db.commit()
    await db.refresh(task)
    return task