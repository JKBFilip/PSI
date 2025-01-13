# app/routers/projects.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.projects_service import create_project, update_project, delete_project, get_all_projects, get_project_by_id
from app.db import get_db
from typing import List

router = APIRouter(prefix="/projects", tags=["Projects"])

# Tworzenie projektu
@router.post("/", response_model=ProjectResponse)
async def create_new_project(project_data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    return await create_project(db=db, project_data=project_data)  # Dodano await

# Edycja projektu
@router.put("/{project_id}", response_model=ProjectResponse)
async def update_existing_project(project_id: int, project_data: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    return await update_project(db=db, project_id=project_id, project_data=project_data)

# Usunięcie projektu
@router.delete("/{project_id}")
async def delete_existing_project(project_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_project(db=db, project_id=project_id)

# Pobranie wszystkich projektów
@router.get("/", response_model=List[ProjectResponse])
async def get_all_projects_list(db: AsyncSession = Depends(get_db)):
    return await get_all_projects(db=db)

# Pobranie projektu po ID
@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    return await get_project_by_id(db=db, project_id=project_id)
