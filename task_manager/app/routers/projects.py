from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import AsyncSessionLocal
from app.schemas.projects import ProjectCreate, ProjectOut
from app.services.projects_service import create_project

router = APIRouter()

# Dependency: Funkcja do uzyskania asynchronicznej sesji bazy danych
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@router.post("/projects/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_new_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_project = await create_project(db=db, project=project)
        return new_project
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating project")
