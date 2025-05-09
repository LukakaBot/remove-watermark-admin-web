from fastapi import APIRouter
from app.api.routes import douyin


api_router = APIRouter()


api_router.include_router(douyin.router)
