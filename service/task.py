from dataclasses import dataclass

from exception import TaskNotFound
from repository import TaskRepository, CacheTask
from schema import TaskCreateShema
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

    def create_task(self, body: TaskCreateShema, user_id: int)-> SchemaTask:
        task_id = self.task_repository.create_task(body, user_id)
        task = self.task_repository.get_task(task_id)
        return SchemaTask.model_validate(task)

    def update_task_name(self, task_id: int, name: str, user_id: int)-> SchemaTask:
        task = self.task_repository.get_user_task(user_id, task_id)
        if not task:
            raise TaskNotFound
        user_task = self.task_repository.edit_task(task_id, name)
        return SchemaTask.model_validate(user_task)

    def delete_task(self, task_id: int, user_id: int)-> SchemaTask:
        task = self.task_repository.get_user_task(user_id, task_id)
        if not task:
            raise TaskNotFound
        user_task = self.task_repository.delete_task(task_id)
        return SchemaTask.model_validate(user_task)


