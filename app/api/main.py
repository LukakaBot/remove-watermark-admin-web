from fastapi import APIRouter
from app.api.endpoints import douyin
from app.api.endpoints import kuaishou


api_router = APIRouter()


api_router.include_router(douyin.router)
api_router.include_router(kuaishou.router)
