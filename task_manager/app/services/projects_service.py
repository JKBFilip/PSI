from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.projects import Project
from app.schemas.projects import ProjectCreate, ProjectUpdate
from fastapi import HTTPException


#tworzenie projektu
async def create_project(db: AsyncSession, project_data: ProjectCreate):
    new_project = Project(name=project_data.name, description=project_data.description)
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)  # Upewnia się, że `id` projektu zostanie uzupełnione
    return new_project


#edytowanie
async def update_project(db: AsyncSession, project_id: int, project_data: ProjectUpdate):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.name = project_data.name
    project.description = project_data.description
    await db.commit()
    await db.refresh(project)
    return project


#usuwanie
async def delete_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await db.delete(project)
    await db.commit()
    return {"detail": "Project deleted successfully"}


#pobieranie wszystkich
async def get_all_projects(db: AsyncSession):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return projects


#pobieranie jednego po ID
async def get_project_by_id(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
