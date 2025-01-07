import logging
from app.models.projects import Project
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Inicjalizacja loggera
logger = logging.getLogger(__name__)


async def create_project(db: AsyncSession, project_data):
    try:
        # Sprawdzanie, czy menedżer projektu (project_manager_id) istnieje
        project_manager_exists = await db.execute(
            select(Project).filter(Project.id == project_data.project_manager_id)
        )
        if not project_manager_exists.scalar():
            logger.error(f"Project manager with ID {project_data.project_manager_id} does not exist.")
            raise ValueError(f"Project manager with ID {project_data.project_manager_id} does not exist.")

        # Tworzenie nowego projektu
        db_project = Project(
            name=project_data.name,
            description=project_data.description,
            start_date=project_data.start_date,
            end_date=project_data.end_date,
            project_manager_id=project_data.project_manager_id,
        )

        db.add(db_project)
        await db.commit()
        await db.refresh(db_project)  # Załaduj obiekt z powrotem po zapisaniu

        logger.info(f"Project created successfully with ID {db_project.id}")
        return db_project

    except Exception as e:
        logger.error(f"Error while creating project: {e}")
        raise
