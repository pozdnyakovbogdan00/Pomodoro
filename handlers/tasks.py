from fastapi import APIRouter, Depends
from starlette import status
from schema.task import Task as SchemaTask
from repository import TaskRepository, CacheTask
from typing import Annotated
from dependency import get_task_service, get_tasks_repository
from service import TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/all", response_model=list[SchemaTask])
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)]
        ):
    return task_service.get_tasks()


@router.post("/", response_model=SchemaTask)
async def create_task(task: SchemaTask, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    task_repository.create_task(task)
    return task

@router.patch("/{task_id}", status_code=status.HTTP_200_OK)
async def patch_task(task_id: int, name: str, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    result = task_repository.edit_task(task_id, name)
    return result

@router.delete("/{task_id}")
async def delete_task(task_id: int, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    result = task_repository.delete_task(task_id)
    return result

@router.get("/{category_name}")
async def get_task_by_category(category_name: str, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    result = task_repository.get_task_by_category(category_name)
    return result