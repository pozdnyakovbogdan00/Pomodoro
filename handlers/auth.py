
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from exception import UserNotFoundException, UserNotCorrectPasswordException
from schema.user import UserLoginShema, UserCreateShema
from service.auth import AuthService
from dependency import get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginShema | None)
async def login(body: UserCreateShema, auth_service: Annotated[AuthService, Depends(get_auth_service)]) :
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)


