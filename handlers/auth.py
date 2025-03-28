
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
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

@router.get(
    "/login/google"
)
async def login_google(
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)

@router.get(
    "/google"
)
async def google_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    return auth_service.google_auth(code=code)



