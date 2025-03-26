from fastapi import Depends

from cache import get_redis_connection
from database.accessor import get_db_session
from repository import TaskRepository, CacheTask, UserRepository
from service import TaskService
from service.auth import AuthService
from service.user import UserService
from sqlalchemy.orm import Session


def get_tasks_repository(db_session: Session = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session)

def get_tasks_cache_repository() -> CacheTask:
    redis_connection = get_redis_connection()
    return CacheTask(redis_connection)

def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache_repository: CacheTask = Depends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(task_repository, task_cache_repository)

def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository | None:
    return UserRepository(db_session=db_session)

def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
)-> UserService | None:
    return UserService(user_repository=user_repository)

def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository)