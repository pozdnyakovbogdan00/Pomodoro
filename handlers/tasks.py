

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from exception import TaskNotFound
from schema import TaskCreateShema
from schema.task import Task as SchemaTask
from repository import TaskRepository, CacheTask
from typing import Annotated
from dependency import get_task_service, get_tasks_repository, get_request_user_id
from service import TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/all", response_model=list[SchemaTask])
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)]
        ):
    return task_service.get_tasks()


@router.post("/", response_model=SchemaTask)
async def create_task(
        body: TaskCreateShema,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
):
    task = task_service.create_task(body, user_id)
    return task

@router.patch("/{task_id}", status_code=status.HTTP_200_OK)
async def patch_task(
        task_id: int,
        name: str,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
):
    result = task_service.update_task_name(task_id, name, user_id)
    return result

@router.delete("/{task_id}")
async def delete_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
):
    try:
        result = task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return result

@router.get("/{category_name}")
async def get_task_by_category(category_name: str, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    result = task_repository.get_task_by_category(category_name)
    return result