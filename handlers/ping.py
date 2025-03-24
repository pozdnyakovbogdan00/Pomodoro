from fastapi import APIRouter
from settings import Settings

router = APIRouter(prefix="/ping", tags=["ping"])

@router.get("/get_ping")
async def get_ping():
    settings = Settings()
    return {"message": settings.GOOGLE_TOKEN_ID}

@router.post("/set_ping")
async def set_ping():
    return {"ping": "pong"}