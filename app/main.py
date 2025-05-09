from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.api.main import api_router
from app.core.config import settings


def generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.SERVICE_PROJECT_NAME,
    openapi_url=f"{settings.SERVICE_API_PREFIX}/openapi.json",
    generate_unique_id_function=generate_unique_id,
)


app.include_router(api_router, prefix=settings.SERVICE_API_PREFIX)
