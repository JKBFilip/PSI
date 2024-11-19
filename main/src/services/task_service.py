from typing import List
from src.domains.task import Task
from src.repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task: Task) -> Task:
        return self.repository.add_task(task)

    def get_all_tasks(self) -> List[Task]:
        return self.repository.list_tasks()