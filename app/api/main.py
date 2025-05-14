from fastapi import APIRouter
from app.api.endpoints import douyin


api_router = APIRouter()


api_router.include_router(douyin.router)
