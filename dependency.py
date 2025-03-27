from fastapi.params import Security
from fastapi.security import OAuth2PasswordBearer

from cache import get_redis_connection
from database.accessor import get_db_session
from exception import TokenExpired, TokenNotCorrect
from repository import TaskRepository, CacheTask, UserRepository
from service import TaskService
from service.auth import AuthService
from service.user import UserService
from sqlalchemy.orm import Session
from fastapi import Request, Depends, security, HTTPException

from settings import Settings

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

def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository, settings=Settings())

def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
)-> UserService | None:
    return UserService(user_repository=user_repository, auth_service=auth_service)

reusable_oauth2 = security.HTTPBearer()

def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)
    ) -> int | None:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired:
        raise HTTPException(status_code=403, detail="Token expired")
    except TokenNotCorrect:
        raise HTTPException(status_code=403, detail="Token not correct")

    return user_id