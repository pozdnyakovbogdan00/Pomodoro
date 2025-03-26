from fastapi import APIRouter, Depends
from typing import Annotated

from repository import UserRepository
from schema.user import UserLoginShema, UserCreateShema
from service.user import UserService
from dependency import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserLoginShema | None)
async def create_user(body: UserCreateShema, user_service: Annotated[UserService, Depends(get_user_service)]) :
    return user_service.create_user(body.username, body.password)