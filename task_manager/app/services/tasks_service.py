from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut  # Dodaj TaskUpdate
from app.models.projects import Project  # Zaimportowanie modelu Project
from app.models.user import User  # Zaimportowanie modelu User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

logger = logging.getLogger(__name__)

# Funkcja do tworzenia zadania
async def create_task(db: AsyncSession, task_data: TaskCreate):  # task_data jest typu TaskCreate
    try:
        # Sprawdzanie, czy projekt istnieje
        project_exists = await db.execute(select(Project).filter(Project.id == task_data.project_id))
        user_exists = await db.execute(select(User).filter(User.id == task_data.assigned_user_id))

        if not project_exists.scalar():
            logger.error(f"Project with id {task_data.project_id} does not exist.")
            raise ValueError(f"Project with id {task_data.project_id} does not exist.")

        if not user_exists.scalar():
            logger.error(f"User with id {task_data.assigned_user_id} does not exist.")
            raise ValueError(f"User with id {task_data.assigned_user_id} does not exist.")

        # Tworzenie nowego zadania
        db_task = Task(
            name=task_data.name,
            description=task_data.description,
            status=task_data.status,
            start_date=task_data.start_date,
            end_date=task_data.end_date,
            project_id=task_data.project_id,
            assigned_user_id=task_data.assigned_user_id
        )

        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)  # Załaduj obiekt z powrotem po zapisaniu

        logger.info(f"Task created successfully with ID {db_task.id}")
        return db_task

    except Exception as e:
        logger.error(f"Error while creating task: {e}")
        raise

# Pobranie zadania po ID
async def get_task_by_id(db: AsyncSession, task_id: int):
    try:
        result = await db.execute(select(Task).filter(Task.id == task_id))
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error while fetching task with ID {task_id}: {e}")
        raise

# Pobranie wszystkich zadań
async def get_tasks(db: AsyncSession):
    try:
        result = await db.execute(select(Task))
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Error while fetching tasks: {e}")
        raise

# Aktualizacja zadania
async def update_task(db: AsyncSession, task_id: int, task_data: TaskUpdate):  # task_data to teraz TaskUpdate
    try:
        task = await get_task_by_id(db, task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found.")

        task.name = task_data.name
        task.description = task_data.description
        task.status = task_data.status
        task.start_date = task_data.start_date
        task.end_date = task_data.end_date

        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task
    except Exception as e:
        logger.error(f"Error while updating task {task_id}: {e}")
        raise

# Usuwanie zadania
async def delete_task(db: AsyncSession, task_id: int):
    try:
        task = await get_task_by_id(db, task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found.")

        await db.delete(task)
        await db.commit()
        return task
    except Exception as e:
        logger.error(f"Error while deleting task {task_id}: {e}")
        raise
