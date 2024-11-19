from fastapi import FastAPI, Depends
from src.services.task_service import TaskService
from src.repositories.task_repository import TaskRepository
from src.domains.task import Task

app = FastAPI()

repository = TaskRepository()
service = TaskService(repository)

@app.post("/tasks/")
def create_task(task: Task):
    return service.create_task(task)

@app.get("/tasks/")
def list_tasks():
    return service.get_all_tasks()
