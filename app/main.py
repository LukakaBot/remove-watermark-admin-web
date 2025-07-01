from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.router.main import api_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3301",
    "http://192.168.1.191:3301",
]


def generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.SERVICE_PROJECT_NAME,
    openapi_url=f"{settings.SERVICE_API_PREFIX}/openapi.json",
    generate_unique_id_function=generate_unique_id,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # expose_headers=["*"],
)

app.include_router(api_router, prefix=settings.SERVICE_API_PREFIX)
