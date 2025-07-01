from fastapi import APIRouter
from app.router.endpoints import douyin


api_router = APIRouter()


api_router.include_router(douyin.router)
