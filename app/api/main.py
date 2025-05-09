from fastapi import APIRouter
from app.api.routes import douyin
from app.api.routes import kuaishou


api_router = APIRouter()


api_router.include_router(douyin.router)
api_router.include_router(kuaishou.router)
