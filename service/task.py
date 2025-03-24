from dataclasses import dataclass

from repository import TaskRepository, CacheTask
from schema.task import Task as SchemaTask

@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheTask

    def get_tasks(self):
        if task := self.task_cache.get_tasks():
            return task
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [SchemaTask.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks
