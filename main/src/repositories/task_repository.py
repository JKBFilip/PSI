from typing import List, Optional
from src.domains.task import Task

class TaskRepository:
    def __init__(self):
        self._tasks = [] 

    def add_task(self, task: Task) -> Task:
        task.id = len(self._tasks) + 1
        self._tasks.append(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((task for task in self._tasks if task.id == task_id), None)

    def list_tasks(self) -> List[Task]:
        return self._tasks
